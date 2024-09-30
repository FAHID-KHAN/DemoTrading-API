from sqlalchemy.orm import Session
from app.models import Account, Transaction
from datetime import datetime
from passlib.context import CryptContext

# Setup password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, name: str, email: str, password: str, initial_balance: float):
    """
    Create a new user account with an initial balance and hashed password.
    """
    hashed_password = pwd_context.hash(password)  # Hash the password
    new_account = Account(
        name=name,
        email=email,
        password=hashed_password,  # Store the hashed password
        balance=initial_balance  # Set initial balance
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


def buy_asset(db: Session, account_id: int, asset: str, quantity: float, price_per_unit: float):
    """
    Perform a buy transaction. Deduct the total cost from the account balance.
    """
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        return None  # Handle error or raise an exception as needed

    total_cost = quantity * price_per_unit
    if account.balance < total_cost:
        raise ValueError("Insufficient balance")  # Raise an error if insufficient balance

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
    """
    Perform a sell transaction. Add the total revenue to the account balance.
    """
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        return None  # Handle error or raise an exception as needed

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
    """
    Retrieve the transaction history for the given account.
    """
    return db.query(Transaction).filter(Transaction.account_id == account_id).all()


def get_account_stats(db: Session, account_id: int):
    """
    Get the current balance and total asset value of an account.
    """
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        return None  # Handle error or raise an exception as needed

    # Get all buy transactions to calculate total assets owned
    transactions = db.query(Transaction).filter(Transaction.account_id == account_id, Transaction.transaction_type == "buy").all()
    total_assets = sum(t.quantity * t.price_per_unit for t in transactions)

    return {
        "balance": account.balance,
        "total_assets": total_assets
    }
