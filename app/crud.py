from sqlalchemy.orm import Session
from app.models import User, Transaction
from datetime import datetime

def create_user(db: Session, name: str, email: str, hashed_password: str, initial_balance: float):
    new_user = User(
        name=name,
        email=email,
        hashed_password=hashed_password,
        balance=initial_balance,
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def buy_asset(db: Session, account_id: int, asset: str, quantity: float, price_per_unit: float):
    account = db.query(User).filter(User.id == account_id).first()
    total_cost = quantity * price_per_unit
    account.balance -= total_cost

    transaction = Transaction(
        account_id=account_id,
        asset=asset,
        transaction_type="buy",
        quantity=quantity,
        price_per_unit=price_per_unit,
        total_amount=total_cost,
        timestamp=datetime.utcnow()
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def sell_asset(db: Session, account_id: int, asset: str, quantity: float, price_per_unit: float):
    account = db.query(User).filter(User.id == account_id).first()
    total_revenue = quantity * price_per_unit
    account.balance += total_revenue

    transaction = Transaction(
        account_id=account_id,
        asset=asset,
        transaction_type="sell",
        quantity=quantity,
        price_per_unit=price_per_unit,
        total_amount=total_revenue,
        timestamp=datetime.utcnow()
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def get_transaction_history(db: Session, account_id: int):
    return db.query(Transaction).filter(Transaction.account_id == account_id).all()

def get_account_stats(db: Session, account_id: int):
    account = db.query(User).filter(User.id == account_id).first()
    if not account:
        return None

    transactions = db.query(Transaction).filter(Transaction.account_id == account_id, Transaction.transaction_type == "buy").all()
    total_assets = sum(t.quantity * t.price_per_unit for t in transactions)

    return {
        "balance": account.balance,
        "total_assets": total_assets
    }

