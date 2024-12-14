"""Config flow for JSON Storage integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, DEFAULT_STORAGE_PATH, CONF_STORAGE_PATH

class JSONStorageConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JSON Storage."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, str] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title="JSON Storage",
                data={
                    CONF_STORAGE_PATH: user_input.get(
                        CONF_STORAGE_PATH, 
                        DEFAULT_STORAGE_PATH
                    )
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_STORAGE_PATH, 
                    default=DEFAULT_STORAGE_PATH
                ): str
            })
        ) 