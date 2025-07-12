# core/governance/dao.py
import json
from config.settings import DAO_CONSTITUTION
from core.identity.agent import Agent


class DAO:
    """Manages the governance and economy based on its locked constitution."""

    def __init__(self):
        self._constitution = DAO_CONSTITUTION
        self.treasury_axm = self._constitution["economics"]["treasury_allocation"]
        self.proposals = []
        self.candidates = []
        self.founder_relinquished_control = True  # Set to True based on constitution

    def submit_proposal(self, proposer_agent: Agent, title: str):
        """Receives a proposal, enforcing submission rules."""
        if not proposer_agent.is_verified:
            return False, "Proposal submission requires a fully verified account."

        proposal = {"proposer_id": proposer_agent.agent_id, "title": title}
        self.proposals.append(proposal)
        return True, f"Proposal '{title}' submitted for review."

    def get_constitution_as_json(self) -> str:
        return json.dumps(self._constitution, sort_keys=True, indent=2)