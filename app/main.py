from fastapi import FastAPI
from app.routers import accounts, transactions

app = FastAPI()

# Include the routers for accounts and transactions
app.include_router(accounts.router)
app.include_router(transactions.router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Demo Trading API"}




