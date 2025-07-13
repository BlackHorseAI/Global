import json
from config.settings import DAO_CONSTITUTION
from core.identity.agent import Agent


class DAO:
    """
    Manages the governance and economy of the network based on its locked constitution.
    """

    def __init__(self):
        self._constitution = DAO_CONSTITUTION

        # Initialize funds based on constitutional allocations
        self.treasury_axm: float = self._constitution["economics"]["treasury_allocation"]
        self.investment_fund_axm: float = self._constitution["economics"]["investment_fund_allocation"]
        self.legal_defense_fund_axm: float = self._constitution["economics"]["legal_defense_fund_allocation"]

        # This would be populated by election results
        self.board_of_members = []
        self.ethics_council = []
        self.cma = []

        self.proposals = []

    def get_constitution_as_json(self) -> str:
        """Serializes the constitution for display and hashing."""
        return json.dumps(self._constitution, sort_keys=True, indent=2)

    def collect_transaction_fee(self, agent: Agent):
        """A conceptual function for collecting the standard network transaction fee."""
        fee = self._constitution["economics"]["transaction_fee"]
        if agent.axm_balance < fee:
            raise Exception(f"Agent {agent.name} has insufficient balance for transaction fee.")
        agent.axm_balance -= fee
        self.treasury_axm += fee