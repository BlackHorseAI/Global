from sqlalchemy.orm import Session
import logging

# Modular imports from the project structure
from ..database import models
from ..schemas import UserCreate
from ..security_manager import get_password_hash

logger = logging.getLogger(__name__)

def get_user_by_username(db: Session, username: str):
    """Retrieves a single user from the database by their username."""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: UserCreate):
    """Creates a new user, hashes their password, and saves it to the database."""
    # Hash the password before storing it
    hashed_password = get_password_hash(user.password)
    
    # Create the new User database model instance
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        email=user.email,
        public_key=user.public_key
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"User '{user.username}' created successfully.")
    return db_user