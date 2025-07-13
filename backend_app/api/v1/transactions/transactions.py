from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Modular imports from the project structure
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
    """
    Initiate a new financial transaction, verified by the user's asymmetric signature.
    """
    # 1. Check if user has a key registered for signing
    if not current_user.public_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no public key registered for signing operations."
        )

    # 2. Verify the cryptographic signature
    is_valid = verify_signature(
        public_key_pem=current_user.public_key,
        signed_data_b64=request.signed_payload,
        signature_b64=request.signature,
        nonce=request.payload.nonce,
        user_id=current_user.id
    )
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature or replay attack detected."
        )
        
    transaction_data = request.payload.data
    
    # 3. Verify authorization (user owns the 'from' agent)
    from_agent = agent_manager.get_agent(db, transaction_data.from_agent_id)
    if not from_agent or from_agent.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to initiate transactions from this agent."
        )
        
    # 4. Process the transaction if all checks pass
    db_transaction = transaction_processor.process_transaction(db=db, transaction=transaction_data)
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction failed processing (e.g., insufficient funds)."
        )
    return db_transaction

@router.get("/{transaction_id}", response_model=Transaction)
def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    """Retrieve a specific transaction if the current user is a party to it."""
    db_transaction = transaction_processor.get_transaction(db, transaction_id=transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    
    # Authorization check
    from_agent_owner_id = db_transaction.from_agent.owner_id
    to_agent_owner_id = db_transaction.to_agent.owner_id
    if current_user.id not in [from_agent_owner_id, to_agent_owner_id]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this transaction.")

    return db_transaction