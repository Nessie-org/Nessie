# Platform Plugin System

A lightweight Python framework for managing and prioritizing plugins that provide various actions. This system allows registering multiple plugins, retrieving them by action, and optionally selecting the best plugin using a prioritization strategy.

## Features

- Register plugins dynamically.
- Retrieve plugins by action name.
- Optional plugin prioritization using a dedicated prioritization plugin.
- Verbose mode for logging plugin registrations.

## Usage

### Initialize Platform

```python
from api import Plugin
from platform_module import Platform  # replace with actual module name

platform = Platform(plugins=[plugin1, plugin2], verbose=True)
```

### Register a Plugin

```python
platform.register_plugin(plugin3)
```

### Get a Plugin for an Action

```python
try:
    plugin = platform.get_plugin("some_action")
    result = plugin.handle(action)
except NoAvailablePluginError:
    print("No plugin available for this action.")
```

### Disable Prioritization

```python
plugin = platform.get_plugin("some_action", priritization=False)
```

## Plugin Prioritization

The system uses a special action `"PluginPrioritization"` to select the best plugin among multiple candidates. If no prioritization plugin is registered, the first available plugin is used by default.

## List of Action names

### `Source_Python`

Sourcing a graph from a Python module.  
Payload of structure: `file_location: str`  
Returns: `Graph`

## Exceptions

- `NoAvailablePluginError` – Raised when no plugin is available for a requested action.
