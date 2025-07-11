from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from ...schemas import Agent, AgentCreate, AgentUpdate, UserInDB, SignedRequest
from ...core import agent_manager, user_manager
from ...database.database import get_db
from ...main import get_current_user  # Dependency from main.py
from ...security_manager import verify_signature

router = APIRouter()


@router.post("/", response_model=Agent, status_code=status.HTTP_201_CREATED)
def create_new_agent(
        request: SignedRequest[AgentCreate],
        db: Session = Depends(get_db),
        current_user: UserInDB = Depends(get_current_user)
):
    """Create a new financial agent, verified by the user's signature."""
    if not current_user.public_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has no public key registered.")

    is_valid = verify_signature(
        public_key_pem=current_user.public_key,
        signed_data_b64=request.signed_payload,
        signature_b64=request.signature,
        nonce=request.payload.nonce,
        user_id=current_user.id
    )
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid signature or replay attack detected.")

    agent_data = request.payload.data
    return agent_manager.create_agent(db=db, agent=agent_data, owner_id=current_user.id)


@router.get("/{agent_id}", response_model=Agent)
def read_agent(agent_id: int, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    db_agent = agent_manager.get_agent(db, agent_id=agent_id)
    if not db_agent or db_agent.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return db_agent


@router.get("/", response_model=List[Agent])
def read_all_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                    current_user: UserInDB = Depends(get_current_user)):
    return agent_manager.get_agents_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)

# (Other endpoints like update and delete would follow a similar signed request pattern)