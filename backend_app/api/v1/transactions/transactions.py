from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...schemas import Transaction, TransactionCreate, TransactionStatus, SignedRequest, UserInDB
from ...core import transaction_processor
from ...database.database import get_db
from ...main import get_current_user # Dependency to get current user
from ...security_manager import verify_signature # ADDED
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
def create_new_transaction(
    request: SignedRequest[TransactionCreate], # MODIFIED: Expects SignedRequest
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Initiate a new financial transaction, verified by user's asymmetric signature.
    The request body must be a SignedRequest containing TransactionCreate payload.
    """
    if not current_user.public_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no public key registered for signing operations. Please register a key first."
        )

    try:
        # Verify the signature against the user's registered public key
        is_valid = verify_signature(
            public_key_pem=current_user.public_key,
            signed_data_b64=request.signed_payload,
            signature_b64=request.signature,
            nonce_store=request.payload.nonce # Pass nonce for replay check
        )
        if not is_valid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature or replay attack detected.")
    except Exception as e:
        logger.error(f"Signature verification failed for transaction: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Signature verification failed: {e}")

    # Extract the actual TransactionCreate object from the payload
    transaction_data = request.payload.data

    # In a real app, you'd also verify current_user owns/controls transaction_data.from_agent_id
    from ...core.agent_manager import get_agent
    from_agent = get_agent(db, transaction_data.from_agent_id)
    if not from_agent or from_agent.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to initiate transactions from this agent.")

    db_transaction = transaction_processor.process_transaction(db=db, transaction=transaction_data)
    if not db_transaction:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction failed to process due to internal error or insufficient funds.")
    return db_transaction

@router.get("/{transaction_id}", response_model=Transaction)
def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    """Retrieve details of a specific transaction."""
    db_transaction = transaction_processor.get_transaction(db, transaction_id=transaction_id)
    # Basic authorization: check if current_user is involved in the transaction
    # Ensure relationships are loaded if needed for .from_agent.owner_id
    if not db_transaction or \
       (db_transaction.from_agent.owner_id != current_user.id and db_transaction.to_agent.owner_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found or not authorized")
    return db_transaction

@router.get("/", response_model=List[Transaction])
def read_all_transactions(
    skip: int = 0,
    limit: int = 100,
    status_filter: TransactionStatus = None,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    """Retrieve a list of all transactions for agents owned by the current user."""
    transactions = transaction_processor.get_transactions_for_user_agents(
        db, owner_id=current_user.id, skip=skip, limit=limit, status_filter=status_filter
    )
    return transactions

# No PUT/DELETE for transactions in most financial systems (immutability)