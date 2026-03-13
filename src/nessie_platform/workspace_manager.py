from nessie_api.models import Workspace


class WorkspaceManager:
    def __init__(self):
        self._workspaces: list[Workspace] = []
        self._active_workspace_index: int | None = None

    def add_workspace(self, workspace: Workspace):
        self._workspaces.append(workspace)
        self._active_workspace_index = len(self._workspaces) - 1

    @property
    def active_workspace_index(self) -> int:
        return self._active_workspace_index

    @active_workspace_index.setter
    def active_workspace_index(self, index: int):
        if index >= len(self._workspaces) or index < 0:
            raise IndexError
        self._active_workspace_index = index

    def remove_workspace_by_index(self, index: int):
        if index >= len(self._workspaces) or index < 0:
            raise IndexError
        self._workspaces.pop(index)
        self._active_workspace_index = len(self._workspaces) - 1 if len(self._workspaces) > 0 else None

    def __len__(self) -> int:
        return len(self._workspaces)

    def __getitem__(self, key: int) -> Workspace:
        if not isinstance(key, int):
            raise TypeError("Key must be an integer")
        if key >= len(self._workspaces) or key < 0:
            raise IndexError(f"Index of bounds. Got: {key} but there are {len(self._workspaces)} workspaces")
        return self._workspaces[key]

