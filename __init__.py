"""The JSON Storage integration."""
import logging
import json
import os
from typing import Dict, Any

from homeassistant.core import HomeAssistant, Event
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DOMAIN,
    EVENT_JSON_DO,
    ACTION_INIT,
    ACTION_DELETE,
    ACTION_INSERT,
    ACTION_SORT,
    CONF_STORAGE_PATH,
    DEFAULT_STORAGE_PATH,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up JSON Storage from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    storage_path = entry.data.get(CONF_STORAGE_PATH, DEFAULT_STORAGE_PATH)
    
    # Ensure storage file exists
    if not os.path.exists(storage_path):
        with open(storage_path, 'w') as f:
            json.dump({}, f)

    async def handle_json_do(event: Event) -> None:
        """Handle JSON manipulation events."""
        path = event.data.get('path')
        todo = event.data.get('todo')
        
        if not path or not todo:
            _LOGGER.error("Missing required parameters in JSON_DO event")
            return

        try:
            with open(storage_path, 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
                
                if todo == ACTION_INIT:
                    _create_path(data, path)
                elif todo == ACTION_DELETE:
                    _delete_path(data, path, event.data.get('keep'))
                elif todo == ACTION_INSERT:
                    _insert_data(data, path, event.data.get('value'))
                elif todo == ACTION_SORT:
                    _sort_data(data, path, event.data.get('sort_by'), 
                             event.data.get('sort_to', 'asc'))
                else:
                    _LOGGER.error(f"Unknown action: {todo}")
                    return
                
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
        
        except Exception as e:
            _LOGGER.error(f"JSON manipulation error: {str(e)}")

    hass.bus.async_listen(EVENT_JSON_DO, handle_json_do)
    
    # Store the cleanup function
    hass.data[DOMAIN][entry.entry_id] = lambda: hass.bus.async_remove_listener(
        EVENT_JSON_DO, handle_json_do
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := True:
        # Call cleanup function
        cleanup = hass.data[DOMAIN].pop(entry.entry_id)
        cleanup()

    return unload_ok

def _create_path(data: Dict[str, Any], path: str) -> None:
    """Create a new path in the JSON structure."""
    parts = path.split('.')
    current = data
    for part in parts[:-1]:
        current = current.setdefault(part, {})
    if parts[-1] not in current:
        current[parts[-1]] = {}

def _delete_path(data: Dict[str, Any], path: str, keep: int | None = None) -> None:
    """Delete a path or keep N sub-nodes."""
    parts = path.split('.')
    current = data
    for part in parts[:-1]:
        if part not in current:
            return
        current = current[part]
    
    if parts[-1] not in current:
        return
        
    if keep is not None and isinstance(current[parts[-1]], list):
        current[parts[-1]] = current[parts[-1]][:keep]
    else:
        del current[parts[-1]]

def _insert_data(data: Dict[str, Any], path: str, value: Any) -> None:
    """Insert data at a specific path."""
    if value is None:
        _LOGGER.error("Cannot insert None value")
        return
        
    parts = path.split('.')
    current = data
    for part in parts[:-1]:
        current = current.setdefault(part, {})
    current[parts[-1]] = value

def _sort_data(data: Dict[str, Any], path: str, sort_by: str, sort_to: str = 'asc') -> None:
    """Sort data at a specific path."""
    parts = path.split('.')
    current = data
    for part in parts[:-1]:
        if part not in current:
            return
        current = current[part]
    
    if parts[-1] not in current or not isinstance(current[parts[-1]], list):
        return
        
    try:
        current[parts[-1]] = sorted(
            current[parts[-1]],
            key=lambda x: x.get(sort_by) if isinstance(x, dict) else x,
            reverse=(sort_to.lower() == 'desc')
        )
    except Exception as e:
        _LOGGER.error(f"Error sorting data: {str(e)}") 