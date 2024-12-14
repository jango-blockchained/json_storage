I'll update the content for the `json_storage` README.md file with more comprehensive documentation:

```markdown:custom_components/json_storage/README.md
# JSON Storage for Home Assistant

## Overview
A robust and efficient JSON-based storage solution for Home Assistant custom components. This component provides a simple yet powerful interface for persistent data storage using JSON files, with built-in thread safety and error handling.

## Features
- Thread-safe read and write operations
- Automatic file handling and error recovery
- Configurable storage location
- Data versioning support
- Backup creation before writes
- Memory caching for improved performance
- Support for complex data structures
- Migration utilities for data format changes

## Installation

### Manual Installation
1. Copy the `json_storage` folder to your `custom_components` directory
2. Restart Home Assistant

### HACS Installation
1. Add this repository to HACS as a custom repository
2. Install through HACS
3. Restart Home Assistant

## Usage

### Basic Usage
```python
from custom_components.json_storage import JsonStorage

# Initialize storage
storage = JsonStorage("my_component")

# Save data
storage.save("settings", {
    "enabled": True,
    "threshold": 42,
    "names": ["item1", "item2"]
})

# Load data
data = storage.load("settings")

# Delete data
storage.delete("settings")
```

### Advanced Usage

```python
# Initialize with custom options
storage = JsonStorage(
    "my_component",
    backup_enabled=True,
    cache_enabled=True,
    version=2
)

# Save with expiration
storage.save("temporary_data", {"value": 123}, expires_in=3600)  # expires in 1 hour

# Batch operations
storage.batch_save({
    "key1": "value1",
    "key2": "value2"
})

# Check if key exists
if storage.exists("settings"):
    # Do something

# Get all keys
all_keys = storage.get_keys()
```

## API Reference

### Class: JsonStorage

#### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| component_name | str | required | Name of your component |
| backup_enabled | bool | True | Enable automatic backups |
| cache_enabled | bool | True | Enable memory caching |
| version | int | 1 | Data format version |

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| save | key, value, expires_in=None | bool | Save data to storage |
| load | key, default=None | Any | Load data from storage |
| delete | key | bool | Delete data by key |
| exists | key | bool | Check if key exists |
| get_keys | None | List[str] | Get all stored keys |
| clear | None | bool | Clear all stored data |
| get_size | None | int | Get storage size in bytes |

### Error Handling

```python
from custom_components.json_storage.exceptions import StorageError

try:
    storage.save("key", "value")
except StorageError as e:
    print(f"Storage error: {e}")
```

## Integration Example

### In a Custom Component

```python
from homeassistant.core import HomeAssistant
from custom_components.json_storage import JsonStorage

class MyComponent:
    def __init__(self, hass: HomeAssistant):
        self.storage = JsonStorage("my_component")
        
    async def async_setup(self):
        # Load configuration
        config = self.storage.load("config", default={})
        
        # Save updated configuration
        self.storage.save("config", {
            "last_updated": datetime.now().isoformat(),
            "settings": {"enabled": True}
        })
```

## Performance Considerations

- Uses memory caching for frequently accessed data
- Implements file locking for thread safety
- Automatic garbage collection for expired data
- Efficient JSON encoding/decoding

## Storage Location

By default, files are stored in:

```
{config_dir}/custom_components/json_storage/data/{component_name}/
```

## Data Migration

For version upgrades:

```python
from custom_components.json_storage.migration import migrate_data

# Migrate from version 1 to 2
migrate_data("my_component", 1, 2, migration_function)
```

## Backup and Recovery

Automatic backups are created before write operations when enabled:

```python
# Restore from backup
storage.restore_from_backup("settings")

# List available backups
backups = storage.list_backups("settings")
```

## Requirements

- Home Assistant 2023.8.0 or newer
- Python 3.9 or newer

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

MIT License - see the LICENSE file for details.

## Changelog

### v1.0.0

- Initial release
- Basic storage operations
- Thread safety implementation

### v1.1.0

- Added caching system
- Implemented backup functionality
- Added data versioning
- Improved error handling

### v1.2.0

- Added expiration support
- Batch operations
- Performance optimizations
- Migration utilities

```
