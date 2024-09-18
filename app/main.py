from fastapi import FastAPI
from app.routers import accounts,transactions

app = FastAPI()

app.include_router(accounts.router)
app.include_router(transactions.router)


#root endpoint 
@app.get("/")
async def root():
    return {"message": "Welcome to Demo Trading API" }



