from sqlalchemy.orm import Session
from ..database import models
from ..schemas import TransactionCreate, TransactionStatus
import logging

logger = logging.getLogger(__name__)

def get_transaction(db: Session, transaction_id: int):
    """Retrieves a single transaction by its ID."""
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def process_transaction(db: Session, transaction: TransactionCreate):
    """
    Processes a financial transaction using a double-entry accounting approach.
    This ensures that for every debit, there is a corresponding credit,
    maintaining the integrity of the ledger.
    """
    # In a high-concurrency system, these rows would be locked for update
    # to prevent race conditions. e.g., .with_for_update()
    from_agent = db.query(models.Agent).filter(models.Agent.id == transaction.from_agent_id).first()
    to_agent = db.query(models.Agent).filter(models.Agent.id == transaction.to_agent_id).first()

    if not from_agent or not to_agent:
        logger.error(f"Transaction failed: Agent not found.")
        return None

    # Verify sufficient funds
    if from_agent.balance < transaction.amount:
        logger.error(f"Transaction failed: Insufficient funds for agent {from_agent.id}.")
        # Here you might create a 'failed' transaction record
        return None

    try:
        # 1. Debit the source agent
        from_agent.balance -= transaction.amount
        
        # 2. Credit the destination agent
        to_agent.balance += transaction.amount

        # 3. Create the transaction record
        db_transaction = models.Transaction(
            from_agent_id=transaction.from_agent_id,
            to_agent_id=transaction.to_agent_id,
            amount=transaction.amount,
            status=TransactionStatus.COMPLETED,
            description=transaction.description,
            transaction_type=transaction.transaction_type
        )
        
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        logger.info(f"Transaction {db_transaction.id} completed successfully.")
        return db_transaction

    except Exception as e:
        logger.error(f"Transaction failed during processing: {e}")
        db.rollback()
        return None