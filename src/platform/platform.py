from collections import defaultdict

from api import Plugin
from api.plugin import Action, NoAvailablePluginError


class Platform:

    class UnsatisfiedDependencyError(ValueError):
        pass

    plugins: dict[str, list[Plugin]]
    verbose: bool

    PLUGIN_PRIORITIZATION = "PluginPrioritization"

    def __init__(self, plugins: list[Plugin] = [], verbose: bool = False) -> None:
        self.plugins: dict[str, list[Plugin]] = defaultdict(list)
        self.verbose = verbose

        for plugin in plugins:
            for action in plugin.provided_actions:
                self.plugins[action].append(plugin)

    def check_deps(self) -> None:
        """Check for unsatisfied dependencies among registered plugins.
        Raises:
            Platform.UnsatisfiedDependencyError: If there are unsatisfied dependencies.
        """
        unsatisfied_deps = self.get_unsatisfied_deps()
        if unsatisfied_deps:
            messages = []
            for dep, dependents in unsatisfied_deps.items():
                messages.append(f"Unsatisfied dependency '{dep}' required by {', '.join(dependents)}")
            raise Platform.UnsatisfiedDependencyError("; ".join(messages))

    def get_unsatisfied_deps(self) -> dict[str, list[str]] | None:
        """Check for unsatisfied dependencies among registered plugins.
        Returns:
            dict[str, list[str]] | None: Mapping of unsatisfied dependency to list of plugin names that require it, or None if all dependencies are satisfied.
        """
        unsatisfied_deps: dict[str, list[str]] = {}
        for plugins in self.plugins.values():
            for plugin in plugins:
                for dependency in plugin.requires:
                    if dependency not in self.plugins:
                        unsatisfied_deps.setdefault(dependency, []).append(plugin.name)
        return unsatisfied_deps if unsatisfied_deps else None

    def register_plugin(self, plugin: Plugin) -> None:
        """
        Register a plugin to the platform.
        Args:
            plugin (Plugin): The plugin to register.
        """
        for action in plugin.provided_actions:
            self.plugins[action].append(plugin)

        if self.verbose:
            print(
                f"Registered plugin: {plugin.name} for actions: {plugin.provided_actions}"
            )

    def get_specific_plugin(self, plugin_name: str, action_name: str) -> Plugin:
        """
        Get a specific plugin by name.
        Args:
            plugin_name (str): The name of the plugin.
            action_name (str): The name of the action the plugin should handle.
        Returns:
            Plugin: The plugin with the given name that can handle the specified action.
        Raises:
            NoAvailablePluginError: If no plugin with the given name for the specified action is available.
        """

        for plugin in self.plugins.get(action_name, []):
            if plugin.name == plugin_name:
                return plugin

        raise NoAvailablePluginError(f"No plugin with name {plugin_name} for action {action_name} is available.")

    def get_plugin_names(self, action_name: str | None = None) -> list[str]:
        """
        Get plugin names that can handle an action.

        Args:
            action_name (str | None): The name of the action. If None, return
            plugin names for all registered actions.

        Returns:
            list[str]: A list of plugin names.
        """

        actions = [action_name] if action_name else self.plugins
        return [plugin.name for action in actions for plugin in self.plugins.get(action, [])]

    def get_plugin(self, action_name: str, prioritization: bool = True) -> Plugin:
        """
        Get a plugin for the given action name.
        If prioritization is enabled, use the prioritization plugin to select the best plugin.
        Otherwise, return the first available plugin.
        Args:
            action_name (str): The name of the action.
            priritization (bool): Whether to use prioritization.
        Returns:
            Plugin: The selected plugin.
        Raises:
            NoAvailablePluginError: If no plugin is available for the action.
        """

        if not prioritization:
            try:
                return self.plugins.get(action_name, [])[0]
            except IndexError as e:
                raise NoAvailablePluginError(
                    f"No plugin for action {action_name} is available."
                ) from e

        return self._get_priority_plugin(action_name)

    def _get_priority_plugin(self, action_name: str) -> Plugin:
        plugins = self._get_all_plugins(action_name)

        if not plugins:
            raise NoAvailablePluginError(
                f"No plugin for action {action_name} is available."
            )
        try:
            prioritization: Plugin = self.plugins.get(self.PLUGIN_PRIORITIZATION, [])[0]
            priority_plugin = prioritization.handle(
                action=Action(name=self.PLUGIN_PRIORITIZATION, payload=plugins)
            )
            return priority_plugin
        except IndexError:
            return plugins[0]

    def _get_all_plugins(self, action_name: str) -> list[Plugin]:
        return self.plugins.get(action_name, [])
