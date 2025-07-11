from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Generic, TypeVar
from datetime import datetime, timezone
from enum import Enum
import uuid

PayloadData = TypeVar('PayloadData')


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    public_key: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserInDB(UserBase):
    id: int

    class Config: from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class AgentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class AgentCreate(AgentBase):
    initial_balance: float = 0.0


class Agent(AgentBase):
    id: int
    balance: float
    owner_id: int

    class Config: from_attributes = True


class SignedPayload(BaseModel, Generic[PayloadData]):
    data: PayloadData
    nonce: str = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config: arbitrary_types_allowed = True


class SignedRequest(BaseModel, Generic[PayloadData]):
    signed_payload: str
    signature: str
    payload: SignedPayload[PayloadData]