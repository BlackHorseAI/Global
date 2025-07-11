from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text # Added Text for longer keys
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base # Import Base from local database.py

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    public_key = Column(Text, nullable=True) # ADDED: To store user's PEM-encoded public key
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    agents = relationship("Agent", back_populates="owner")

class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    balance = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="agents")
    # Relationships for transactions (an agent can be 'from' or 'to')
    sent_transactions = relationship("Transaction", foreign_keys="[Transaction.from_agent_id]", back_populates="from_agent")
    received_transactions = relationship("Transaction", foreign_keys="[Transaction.to_agent_id]", back_populates="to_agent")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    from_agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    to_agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False) # e.g., 'transfer', 'deposit', 'withdrawal'
    status = Column(String, nullable=False) # e.g., 'pending', 'completed', 'failed', 'rejected'
    description = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    from_agent = relationship("Agent", foreign_keys=[from_agent_id], back_populates="sent_transactions")
    to_agent = relationship("Agent", foreign_keys=[to_agent_id], back_populates="received_transactions")