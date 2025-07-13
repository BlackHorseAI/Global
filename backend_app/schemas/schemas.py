from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Generic, TypeVar
from datetime import datetime, timezone
import uuid

PayloadData = TypeVar('PayloadData')


class UserBase(BaseModel):
    username: str = Field(..., min_length=3)
    public_key: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserInDB(UserBase):
    id: int

    class Config: from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class AgentCreate(BaseModel):
    name: str = Field(..., min_length=2)


class Agent(AgentCreate):
    id: int
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