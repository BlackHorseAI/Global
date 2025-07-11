from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...schemas import Transaction, TransactionCreate, SignedRequest, UserInDB
from ...core import transaction_processor, agent_manager
from ...database.database import get_db
from ...main import get_current_user
from ...security_manager import verify_signature

router = APIRouter()

@router.post("/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
def create_new_transaction(
    request: SignedRequest[TransactionCreate],
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    """Initiate a new financial transaction, verified by the user's signature."""
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature or replay attack detected.")
        
    transaction_data = request.payload.data
    
    # Authorization check: Does the current user own the 'from' agent?
    from_agent = agent_manager.get_agent(db, transaction_data.from_agent_id)
    if not from_agent or from_agent.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to transact from this agent.")
        
    db_transaction = transaction_processor.process_transaction(db=db, transaction=transaction_data)
    if not db_transaction:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction failed processing.")
    return db_transaction

# (Other transaction endpoints like get would follow here)