from nessie_api.models import Action

from nessie_platform.plugin_manager import PluginManager
from nessie_platform.plugin_dto import PluginDTO
from nessie_platform.context import make_context
from nessie_platform.workspace_manager import WorkspaceManager
import nessie_platform.constants as constants
from nessie_platform.actions import platform_plugin

class Platform:
    def __init__(self):
        self.plugin_manager = PluginManager()
        self.workspace_manager = WorkspaceManager()
        self.plugin_manager.discover_plugins()
        self.plugin_manager.register_plugin(platform_plugin())
        self.plugin_manager.check_deps()

    def get_plugins(self, action_name: str) -> list[PluginDTO]:
        plugins = self.plugin_manager.get_available_plugins(action_name)
        return [PluginDTO(plugin.name, plugin.setup_requires) for plugin in plugins]

    def perform_action(self, action_name: str, payload: dict, plugin_name: str | None = None) -> str:
        if plugin_name:
            plugin = self.plugin_manager.get_specific_plugin(plugin_name, action_name)
        else:
            plugin = self.plugin_manager.get_plugin(action_name)

        action = Action(name=action_name, payload=payload)
        plugin.handle(action, self._get_context())
        return self._ui()

    def index(self) -> str:
        return self._ui()

    def _ui(self) -> str:
        ui_plugin = self.plugin_manager.get_plugin(constants.RENDER_UI, False)
        return ui_plugin.handle(Action(constants.RENDER_UI, {}), self._get_context())


    def _get_context(self):
        return make_context(self.plugin_manager, self.workspace_manager)