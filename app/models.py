from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import List

# SQLAlchemy base
Base = declarative_base()

# SQLAlchemy Models

class User(Base):
    """
    SQLAlchemy model for storing user account information.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Transaction(Base):
    """
    SQLAlchemy model for storing asset transactions.
    """
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer)
    asset = Column(String)
    transaction_type = Column(String)
    quantity = Column(Float)
    price_per_unit = Column(Float)
    total_amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


# Pydantic Models

class Account(BaseModel):
    name: str
    email: str
    password: str
    initial_balance: float

class AccountResponse(BaseModel):
    id: int
    name: str
    balance: float
    created_at: datetime

    class Config:
        orm_mode = True

class BuySellRequest(BaseModel):
    account_id: int
    asset: str
    quantity: float
    price_per_unit: float

class TransactionResponse(BaseModel):
    id: int
    account_id: int
    asset: str
    transaction_type: str
    quantity: float
    price_per_unit: float
    total_amount: float
    timestamp: datetime

    class Config:
        orm_mode = True

class AccountStats(BaseModel):
    balance: float
    total_assets: float
