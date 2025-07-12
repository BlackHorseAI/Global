from core.identity.agent import Agent

class BoardOfMembers:
    """Represents the Board, responsible for operational and economic proposals."""
    def __init__(self):
        self.members = [Agent(f"Board Member #{i+1}", "Board") for i in range(100)]

class EthicsCouncil:
    """Represents the Ethics Council, responsible for social and ethical oversight."""
    def __init__(self):
        self.members = [Agent(f"Ethics Member #{i+1}", "Ethics") for i in range(100)]

class CapitalMarketsAuthority:
    """Represents the CMA, responsible for vetting public asset offerings."""
    def __init__(self):
        self.members = [Agent(f"CMA Member #{i+1}", "CMA") for i in range(100)]

class ArbitrationCouncil:
    """Represents the Arbitration Council, the network's 'Supreme Court'."""
    def __init__(self):
        self.members = [Agent(f"Arbiter #{i+1}", "Arbitration") for i in range(15)]