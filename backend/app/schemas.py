from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str

class BankAccountLink(BaseModel):
    provider_account_id: str
    name: Optional[str] = None

class TransactionIn(BaseModel):
    account_id: int
    amount: float
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None

    model_config = {"from_attributes": True}

class TransactionOut(TransactionIn):
    id: int
    provider_txn_id: Optional[str] = None
    account_id: int
