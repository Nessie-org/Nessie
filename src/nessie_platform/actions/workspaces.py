from nessie_api.models import Action
from nessie_api.protocols import Context


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