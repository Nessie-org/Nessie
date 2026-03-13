from typing import Any

from nessie_api.models import Workspace, Action, ConsoleMessage, FilterExpression, Graph
from nessie_api.protocols import Context

from nessie_platform.plugin_manager import PluginManager
from nessie_platform.workspace_manager import WorkspaceManager

import nessie_platform.constants as constants


def make_context(plugin_manager: PluginManager, workspace_manger: WorkspaceManager) -> "Context":
    class InnerContext(Context):
        """
            Context protocol that provides methods available to the plugin to change
            the shared environment.
            """

        ################## WORKSPACE ##################

        def get_workspace_count(self) -> int:
            """Total number of workspaces. Must be ≥ 1."""
            return len(workspace_manger)

        def get_active_workspace_index(self) -> int | None:
            """
            Index of a currently open (and active) workspace.
            Must be within ``[0, get_workspace_count())``.
            """
            return workspace_manger.active_workspace_index

        def set_active_workspace_index(self, index: int) -> None:
            """
            Sets the active workspace to the one at *index*.
            Must be within ``[0, get_workspace_count())``.
            """
            workspace_manger.active_workspace_index = index

        def add_workspace(self, graph: "Graph") -> None:
            """
            Adds a new workspace with the given graph.
            """
            workspace = Workspace(graph)
            visualizer_plugin = plugin_manager.get_plugin(constants.VISUALIZE_GRAPH, False)
            workspace.visualiser_name = visualizer_plugin.name
            workspace_manger.add_workspace(workspace)

        def close_workspace_at(self, index: int) -> None:
            """
            Closes the workspace at *index*.
            Must be within ``[0, get_workspace_count())``.
            """
            workspace_manger.remove_workspace_by_index(index)

        ################## GRAPHS ##################

        def get_graph_at(self, index: int) -> "Graph":
            """
            Returns the current graph displayed at *index*.
            This graph already has all the filters applied
            """
            return workspace_manger[index].current_graph

        def get_full_graph_at(self, index: int) -> "Graph":
            """
            Returns the full graph at *index* without any filters applied.
            """
            return workspace_manger[index].source_graph

        def set_graph_at(self, index: int, graph: "Graph") -> None:
            """
            Sets the graph at *index* to *graph*.
            Must be within ``[0, get_workspace_count())``.
            """
            workspace_manger[index].current_graph = graph

        def set_full_graph_at(self, index: int, graph: "Graph") -> None:
            """
            Sets the full graph at *index* to *graph*.
            Must be within ``[0, get_workspace_count())``.
            """
            workspace_manger[index].source_graph = graph

        ################## VISUALISATION ##################

        def get_visualised_graph_at(self, index: int) -> str:
            """
            Returns the visualized graph at *index* as an HTML string.
            This is the result of the visualization plugin that is currently active for the graph at *index*.
            """
            return self.perform_action(Action(constants.VISUALIZE_GRAPH, self.get_graph_at(index)), workspace_manger[index].visualiser_name)

        def get_visualiser_name_at(self, active_index: int) -> str:
            """
            Returns the name of the visualizer plugin that is currently active for the graph at *index*.
            """
            return workspace_manger[active_index].visualiser_name or "Nessie Graph Explorer"

        def set_visualiser_at(self, index: int, visualiser_name: str) -> None:
            """
            Sets the visualizer plugin for the graph at *index* to *visualiser_name*.
            Must be within ``[0, get_workspace_count())``.
            """
            workspace_manger[index].visualiser_name = visualiser_name

        ################## FILTERS ##################

        def get_active_filters_at(self, index: int) -> list:
            """
            Return a list of currently active filters from the graph at *index*.
            """
            return workspace_manger[index].active_filters

        def add_filter_at(self, index: int, filter_expression: "FilterExpression") -> None:
            """
            Adds a new filter to the graph at *index*.
            Must be within ``[0, get_workspace_count())``.
            """
            workspace_manger[index].add_filter(filter_expression)

        def remove_filter_at(self, index: int, filter_expression: "FilterExpression") -> None:
            """
            Removes a filter from the graph at *index*.
            Must be within ``[0, get_workspace_count())``.
            """
            workspace_manger[index].remove_filter(filter_expression)

        def clear_filters_at(self, index: int) -> None:
            """
            Clears all filters from the graph at *index*.
            Must be within ``[0, get_workspace_count())``.
            """
            workspace_manger[index].clear_filters()

        ################ SEARCH ##################

        def get_search_at(self, index: int) -> str:
            """
            Returns the current search query for the graph at *index*.
            Default: empty string.
            """
            if index < 0 or index >= self.get_workspace_count():
                raise IndexError("Workspace index out of range")
            return workspace_manger[index].search_query
        
        def set_search_at(self, index: int, query: str) -> None:
            """
            Sets the search query for the graph at *index* to *query*.
            Must be within ``[0, get_workspace_count())``.
            """
            if index < 0 or index >= self.get_workspace_count():
                raise IndexError("Workspace index out of range")
            workspace_manger[index].search_query = query

        ################ CONSOLE ##################

        def get_console_messages_at(self, index: int) -> list:
            """
            Returns a list of console messages from the graph at *index*.
            """
            return workspace_manger[index].console_messages

        def add_console_message_at(self, index: int, message: "ConsoleMessage") -> None:
            """
            Adds a new console message to the workspace at *index*.
            Must be within ``[0, get_workspace_count())``.
            """
            workspace_manger[index].add_console_message(message)

        def clear_console_messages_at(self, index: int) -> None:
            """
            Clears all console messages from the workspace at *index*.
            Must be within ``[0, get_workspace_count())``.
            """
            workspace_manger[index].clear_console_messages()

        ################## ACTIONS ##################

        def perform_action(self, action: "Action", plugin_name: str | None = None) -> Any:
            """
            Performs the given action in the shared environment.
            If *plugin_name* is provided, the action is performed only by that plugin
            (implicit intent), otherwise any plugin that supports the action can perform it (explicit intent).
            """
            if plugin_name:
                plugin = plugin_manager.get_specific_plugin(plugin_name, action.name)
            else:
                plugin = plugin_manager.get_plugin(action.name)
            return plugin.handle(action, self)
    return InnerContext()