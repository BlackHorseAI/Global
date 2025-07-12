# core/identity/agent.py
import uuid

class Agent:
    """Represents an anonymous participant in the economy."""
    def __init__(self, name: str, is_verified: bool = False):
        self.agent_id = str(uuid.uuid4())
        self.name = name
        self.is_verified = is_verified # Represents having Proof-of-Personhood
        self.axm_balance = 1000.0