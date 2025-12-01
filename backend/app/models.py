from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    accounts: List["BankAccount"] = Relationship(back_populates="owner")

class BankAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    provider_account_id: str  # id from your MockBank API
    name: Optional[str] = None
    balance: float = 0.0

    owner: Optional[User] = Relationship(back_populates="accounts")
    transactions: List["Transaction"] = Relationship(back_populates="account")

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: Optional[int] = Field(default=None, foreign_key="bankaccount.id")
    provider_txn_id: Optional[str] = None
    amount: float
    date: datetime
    description: Optional[str] = None
    category: Optional[str] = None

    account: Optional[BankAccount] = Relationship(back_populates="transactions")

class Budget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    category: str
    amount: float
    period: str = "monthly"
