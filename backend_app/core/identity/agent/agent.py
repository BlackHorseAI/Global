# core/identity/agent.py
import uuid

class Agent:
    """Represents a participant in the economy."""
    def __init__(self, name: str, is_founder: bool = False):
        self.agent_id = str(uuid.uuid4())
        self.name = name
        self.is_founder = is_founder