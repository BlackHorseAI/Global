import uuid
from dataclasses import dataclass, field
from core.identity.agent import Agent

@dataclass
class VerifiableCredential:
    """
    Represents a signed claim about a subject (an Agent).
    Designed to support multiple signatures for enhanced security.
    """
    claim: dict
    signatures: list[dict] = field(default_factory=list) # e.g., [{"issuer_id": "...", "signature": "..."}]

class IssuerAuthority:
    """A conceptual, trusted entity that can issue and sign Verifiable Credentials."""
    def __init__(self, name: str):
        self.issuer_id = str(uuid.uuid4())
        self.name = name

    def issue_signature(self, agent: Agent, claim: dict) -> dict:
        """
        Creates a cryptographic signature attesting to a claim about an agent.
        In a real system, this would involve using the issuer's private key.
        """
        # Create a representation of the data to be signed
        message = f"{agent.agent_id}:{json.dumps(claim, sort_keys=True)}"
        
        # Simulate a cryptographic signature
        simulated_signature = f"signed({hash(message)})"

        return {
            "issuer_id": self.issuer_id,
            "signature": simulated_signature
        }

    def issue_credential(self, agent: Agent, claim: dict) -> VerifiableCredential:
        """Issues a new credential with this authority's signature."""
        signature = self.issue_signature(agent, claim)
        return VerifiableCredential(claim=claim, signatures=[signature])