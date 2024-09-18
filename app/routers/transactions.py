from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import BuySellRequest, TransactionResponse
from typing import List
from app import crud

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.post("/buy", response_model=TransactionResponse)
def buy_asset(buy_data: BuySellRequest, db: Session = Depends(get_db)):
    transaction = crud.buy_asset(
        db=db,
        account_id=buy_data.account_id,
        asset=buy_data.asset,
        quantity=buy_data.quantity,
        price_per_unit=buy_data.price_per_unit
    )
    return transaction

@router.post("/sell", response_model=TransactionResponse)
def sell_asset(sell_data: BuySellRequest, db: Session = Depends(get_db)):
    transaction = crud.sell_asset(
        db=db,
        account_id=sell_data.account_id,
        asset=sell_data.asset,
        quantity=sell_data.quantity,
        price_per_unit=sell_data.price_per_unit
    )
    return transaction

@router.get("/history/{account_id}", response_model=List[TransactionResponse])
def get_transaction_history(account_id: int, db: Session = Depends(get_db)):
    transactions = crud.get_transaction_history(db, account_id=account_id)
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this account")
    return transactions
