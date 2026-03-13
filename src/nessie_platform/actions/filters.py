from nessie_api.models import Action, FilterExpression
from nessie_api.protocols import Context
import nessie_platform.constants as constants

def apply_filters(action: "Action", context: "Context"):
    index = context.get_active_workspace_index()
    if index is None:
        return
    filter_action = Action(constants.FILTER_GRAPH, {
        "filters": context.get_active_filters_at(index),
        "graph": context.get_full_graph_at(index),
    })
    context.perform_action(filter_action)

def add_filter(action: "Action", context: "Context"):
    filter_expression = action.payload.get("filter")
    if not isinstance(filter_expression, FilterExpression):
        filter_expression = FilterExpression.from_json(filter_expression)
    index = context.get_active_workspace_index()
    if index is None:
        return
    context.add_filter_at(index, filter_expression)
    apply_filters_action = Action(constants.APPLY_FILTERS, {})
    context.perform_action(apply_filters_action)


def remove_filter(action: "Action", context: "Context"):
    filter_expression = action.payload.get("filter")
    if not isinstance(filter_expression, FilterExpression):
        filter_expression = FilterExpression.from_json(filter_expression)
    index = context.get_active_workspace_index()
    if index is None:
        return
    context.remove_filter_at(index, filter_expression)
    apply_filters_action = Action(constants.APPLY_FILTERS, {})
    context.perform_action(apply_filters_action)

def clear_filters(action: "Action", context: "Context"):
    index = context.get_active_workspace_index()
    if index is None:
        return
    context.clear_filters_at(index)
    graph = context.get_full_graph_at(index)
    context.set_graph_at(index, graph)