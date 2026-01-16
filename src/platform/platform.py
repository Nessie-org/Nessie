from collections import defaultdict

from api import Plugin


class Platform:

    def __init__(self, plugins: list[Plugin] = []):
        self.plugins: dict[str, Plugin] = defaultdict(list)
        for plugin in plugins:
            for action in plugin.provided_actions:
                self.plugins[action].append(plugin)

    def register_plugin(self, plugin: Plugin) -> None:
        for action in plugin.provided_actions:
            self.plugins[action].append(plugin)
