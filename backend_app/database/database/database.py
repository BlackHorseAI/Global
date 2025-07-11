from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    public_key = Column(Text, nullable=True) # For user's RSA public key
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

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    from_agent_id = Column(Integer, ForeignKey("agents.id"))
    to_agent_id = Column(Integer, ForeignKey("agents.id"))
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())