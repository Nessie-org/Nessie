from nessie_api.models import Action
from nessie_api.protocols import Context

import nessie_platform.constants as constants


def switch_workspace(action: "Action", context: "Context"):
    index = action.payload.get("index", None)
    if index is None:
        return
    if index < 0 or index >= context.get_workspace_count():
        return
    context.set_active_workspace_index(index)

def close_workspace(action: "Action", context: "Context"):
    index = action.payload.get("index", None)
    if index is None:
        return
    if index < 0 or index >= context.get_workspace_count():
        return
    context.close_workspace_at(index)

def open_workspace(action: "Action", context: "Context"):
    ds_name = action.payload.get("plugin", None)
    if ds_name is None:
        return

    load_action = Action(constants.LOAD_GRAPH, action.payload.get("payload", {}))
    graph = context.perform_action(load_action, ds_name)
    context.add_workspace(graph)