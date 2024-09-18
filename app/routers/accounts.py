from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Account, AccountResponse, AccountStats
from app import crud

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"]
)

@router.post("/", response_model=AccountResponse)
def create_account(account_data: Account, db: Session = Depends(get_db)):
    new_user = crud.create_user(
        db=db,
        name=account_data.name,
        email=account_data.email,
        hashed_password=account_data.password,
        initial_balance=account_data.initial_balance
    )
    return new_user

@router.get("/stats/{account_id}", response_model=AccountStats)
def get_account_stats(account_id: int, db: Session = Depends(get_db)):
    stats = crud.get_account_stats(db, account_id=account_id)
    if stats is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return stats


