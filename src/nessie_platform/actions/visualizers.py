from nessie_api.models import Action
from nessie_api.protocols import Context


def change_visualizer(action: "Action", contex: "Context"):
    name = action.payload.get("visualizer_name", None)
    if name is None:
        return
    index = contex.get_active_workspace_index()
    if index is None:
        return
    contex.set_visualiser_at(index, name)