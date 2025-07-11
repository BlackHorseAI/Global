# core/governance/dao.py
import json
from config.settings import DAO_CONSTITUTION

class DAO:
    """Manages the governance and economy based on its locked constitution."""
    def __init__(self):
        self._constitution = DAO_CONSTITUTION

    def get_constitution_as_json(self) -> str:
        """Serializes the constitution for display."""
        return json.dumps(self._constitution, sort_keys=True, indent=2)