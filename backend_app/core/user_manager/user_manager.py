from sqlalchemy.orm import Session
from ..database import models
from ..schemas import UserCreate
from ..security_manager import get_password_hash
import logging

logger = logging.getLogger(__name__)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        email=user.email,
        public_key=user.public_key
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User '{user.username}' created.")
    return db_user