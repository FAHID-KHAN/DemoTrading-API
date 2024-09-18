FastAPI Trading API Documentation
Overview
This API is a demo trading system built using FastAPI. It supports the following core functionalities:

User account management (create account).
Buy and sell assets.
Retrieve transaction history.
Fetch account statistics.
The API can be used as a backend for a simple trading platform, and it includes endpoints for managing accounts, performing trades, and viewing account balances.

Endpoints
1. Create Account
Endpoint: POST /users/
Description: Creates a new user account with an initial balance.
Request Body:
json
Copy code
{
  "name": "string",
  "email": "string",
  "balance": 0.0
}
Response:
json
Copy code
{
  "name": "string",
  "email": "string",
  "balance": 0.0
}
Status Codes:
201 Created: The user was successfully created.
400 Bad Request: Invalid input.
2. Buy or Sell Assets
Endpoint: POST /transactions/
Description: Executes a buy or sell transaction for a specific asset.
Request Body:
json
Copy code
{
  "account_id": "string",
  "asset": "string",
  "quantity": 0.0,
  "price_per_unit": 0.0,
  "transaction_type": "buy" or "sell"
}
Response:
json
Copy code
{
  "account_id": "string",
  "transaction_id": "string",
  "total_amount": 0.0
}
Status Codes:
200 OK: The transaction was executed successfully.
400 Bad Request: Invalid input (e.g., insufficient balance for buy).
404 Not Found: Account not found.
3. Get Transaction History
Endpoint: GET /transactions/
Description: Retrieves a list of all transactions made by the user.
Response:
json
Copy code
[
  {
    "account_id": "string",
    "transaction_id": "string",
    "asset": "string",
    "quantity": 0.0,
    "price_per_unit": 0.0,
    "transaction_type": "buy" or "sell",
    "total_amount": 0.0
  }
]
Status Codes:
200 OK: Returns a list of transactions.
404 Not Found: No transactions found.
4. Check Account Balance
Endpoint: GET /users/{user_id}/balance/
Description: Retrieves the current balance of a specific user.
Response:
json
Copy code
{
  "balance": 0.0
}
Status Codes:
200 OK: Balance fetched successfully.
404 Not Found: User not found.
5. Get Account Stats
Endpoint: GET /users/{user_id}/stats/
Description: Retrieves detailed statistics about the account, including the total balance and asset holdings.
Response:
json
Copy code
{
  "balance": 0.0,
  "total_assets": 0.0
}
Status Codes:
200 OK: Statistics retrieved successfully.
404 Not Found: User not found.
Error Handling
400 Bad Request: This error occurs when the request contains invalid data (e.g., invalid account ID, insufficient balance for a purchase).
404 Not Found: This error occurs when a resource (e.g., a user or transaction) is not found.
Usage
This API can be used by frontend clients such as web or mobile applications to manage user accounts and transactions on a trading platform. Here's a typical usage flow:

Create a user account by sending a POST request to /users/.
Buy or sell assets by sending a POST request to /transactions/.
Check the account balance using a GET request to /users/{user_id}/balance/.
Get transaction history using a GET request to /transactions/.
Get detailed account statistics using a GET request to /users/{user_id}/stats/.