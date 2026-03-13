from typing import Any

from nessie_api.models.plugin import SetupRequirementType


class PluginDTO:
    def __init__(self, name: str, setup: dict[str, SetupRequirementType]):
        self.name = name
        self.requirements = setup

    def  to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "requirements": {
                key: value.value for key, value in self.requirements.items()
            },
        }