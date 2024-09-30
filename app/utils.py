# app/utils.py

import numpy as np
from sqlalchemy.orm import Session
from app.models import DailyBalance, Account
from datetime import datetime, timedelta

def calculate_account_metrics(account_balance_history):
    """
    Function to calculate account statistics based on daily balances.
    
    account_balance_history: List of historical account balances over time.
    """
    if not account_balance_history or len(account_balance_history) < 2:
        return None, None, None, None, None, None

    daily_gain_loss = (account_balance_history[-1] - account_balance_history[-2]) / account_balance_history[-2] * 100
    weekly_gain_loss = (account_balance_history[-1] - account_balance_history[-7]) / account_balance_history[-7] * 100 if len(account_balance_history) >= 7 else None
    monthly_gain_loss = (account_balance_history[-1] - account_balance_history[-30]) / account_balance_history[-30] * 100 if len(account_balance_history) >= 30 else None

    max_balance = max(account_balance_history)
    min_balance = min(account_balance_history[account_balance_history.index(max_balance):])
    drawdown = (max_balance - min_balance) / max_balance * 100

    returns = np.diff(account_balance_history) / account_balance_history[:-1]
    standard_deviation = np.std(returns) * 100
    volatility = standard_deviation * np.sqrt(252)

    return daily_gain_loss, weekly_gain_loss, monthly_gain_loss, drawdown, standard_deviation, volatility

def save_daily_balance(account_id: int, db: Session):
    """
    Function to save daily balance for an account.
    This function should be called at the end of each day.
    """
    account = db.query(Account).filter(Account.id == account_id).first()
    
    today = datetime.utcnow().date()
    existing_balance = db.query(DailyBalance).filter(
        DailyBalance.account_id == account_id,
        DailyBalance.date == today
    ).first()

    if not existing_balance:
        daily_balance = DailyBalance(
            account_id=account_id,
            balance=account.balance,
            date=today
        )
        db.add(daily_balance)
        db.commit()

def get_daily_balances(account_id: int, db: Session):
    """
    Function to fetch daily balances for the past 30 days for a given account.
    """
    today = datetime.utcnow().date()
    thirty_days_ago = today - timedelta(days=30)

    daily_balances = db.query(DailyBalance).filter(
        DailyBalance.account_id == account_id,
        DailyBalance.date >= thirty_days_ago
    ).order_by(DailyBalance.date).all()
    
    return daily_balances
