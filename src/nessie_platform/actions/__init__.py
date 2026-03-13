from .filters import apply_filters, add_filter, remove_filter
from .workspaces import switch_workspace, close_workspace
from .visualizers import change_visualizer
from .console import add_message, clear_console
import nessie_platform.constants as constants
from nessie_api.models import plugin

@plugin("Nessie Platform")
def platform_plugin():
    handlers = {
        constants.APPLY_FILTERS: apply_filters,
        constants.ADD_FILTER: add_filter,
        constants.REMOVE_FILTER: remove_filter,
        constants.SWITCH_WORKSPACE: switch_workspace,
        constants.CLOSE_WORKSPACE: close_workspace,
        constants.CHANGE_VISUALIZER: change_visualizer,
        constants.ADD_CONSOLE_MESSAGE: add_message,
        constants.CLEAR_CONSOLE: clear_console,
    }

    requirements = {}
    setup = {}

    return {
        "handlers": handlers,
        "requires": requirements,
        "setup_requires": setup,
    }