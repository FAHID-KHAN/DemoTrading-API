from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

from app.models import AccountCreate, AccountResponse, AccountStats ,Account # Use Pydantic models
from app import crud
from app.utils import calculate_account_metrics, get_daily_balances


router = APIRouter(
    prefix="/accounts",
    tags=["accounts"]
)

@router.post("/", response_model=AccountResponse)  # Return the Pydantic model
def create_account(account_data: AccountCreate, db: Session = Depends(get_db)):  # Accept Pydantic model as input
    new_user = crud.create_user(
        db=db,
        name=account_data.name,
        email=account_data.email,
        password=account_data.password,
        initial_balance=account_data.initial_balance
    )
    return new_user

@router.get("/stats/{account_id}", response_model=AccountStats)
def get_account_stats(account_id: int, db: Session = Depends(get_db)):
    # Fetch the account
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Fetch the daily balances from the database
    daily_balances = get_daily_balances(account_id, db)
    
    # Ensure there is enough data to calculate the statistics
    if len(daily_balances) < 2:
        return {
            "balance": account.balance,
            "total_assets": account.total_assets,
            "daily_gain_loss": None,
            "weekly_gain_loss": None,
            "monthly_gain_loss": None,
            "drawdown": None,
            "standard_deviation": None,
            "volatility": None
        }
    
    # Extract balance history from daily balances
    balance_history = [balance.balance for balance in daily_balances]
    
    # Calculate metrics (gain/loss, drawdown, standard deviation, volatility)
    daily_gain_loss, weekly_gain_loss, monthly_gain_loss, drawdown, standard_deviation, volatility = calculate_account_metrics(balance_history)
    
    # Return the account statistics
    return {
        "balance": account.balance,
        "total_assets": account.total_assets,
        "daily_gain_loss": daily_gain_loss,
        "weekly_gain_loss": weekly_gain_loss,
        "monthly_gain_loss": monthly_gain_loss,
        "drawdown": drawdown,
        "standard_deviation": standard_deviation,
        "volatility": volatility
    }
