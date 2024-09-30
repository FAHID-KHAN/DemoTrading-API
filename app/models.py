from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel
from typing import List

# SQLAlchemy base
Base = declarative_base()

# SQLAlchemy Models

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)  # Add password to store the hashed password
    balance = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="account")
    daily_balances = relationship("DailyBalance", back_populates="account")


class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    asset = Column(String)
    quantity = Column(Float)
    price_per_unit = Column(Float)
    transaction_type = Column(String)
    total_amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    account = relationship("Account", back_populates="transactions")


class DailyBalance(Base):
    __tablename__ = 'daily_balances'
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    balance = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    
    # Fix the relationship by using a string reference to 'Account'
    account = relationship("Account", back_populates="daily_balances")

# Pydantic Models

# Rename to avoid conflict with SQLAlchemy model
class AccountCreate(BaseModel):
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
    daily_gain_loss: float
    weekly_gain_loss: float
    monthly_gain_loss: float
    drawdown: float
    standard_deviation: float
    volatility: float

    class Config:
        orm_mode = True