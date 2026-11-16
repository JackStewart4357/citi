from fastapi import Depends, FastAPI, HTTPException
from typing import Literal
from pydantic import BaseModel, Field
from decimal import Decimal
from app.db import get_conn
from datetime import datetime

app = FastAPI(title = "Ledger Lite")


class AmountIn(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)

class AccountCreate(BaseModel):
    owner_name: str = Field(min_length=1, max_length=50)
    currency: Literal["GBP", "USD", "EUR"]


class AccountOut(BaseModel):
    id: int
    owner_name: str
    currency: str
    balance: Decimal
    created_at: datetime

@app.post("/accounts/{account_id}/deposits", status_code=201, response_model=AccountOut)
def deposit(account_id: int, body: AmountIn, conn=Depends(get_conn)):
    account = conn.execute("UPDATE account SET balance = balance + %s WHERE id = %s " "RETURNING id, owner_name, currency, balance, created_at",(body.amount, account_id,)).fetchone()
    if account is None:
        raise HTTPException(status_code=404, detail="Account id {account_id} was not found")
    conn.execute("INSERT INTO btransaction (account_id, type, amount) VALUES (%s, 'deposit', %s)", (account_id, body.amount,),)
    return account


@app.post("/accounts", response_model=AccountOut)
def create_account(account: AccountCreate, status_code=201, conn=Depends(get_conn)):
    row = conn.execute(
        "INSERT INTO account (owner_name, currency) VALUES (%s, %s) RETURNING *",
        (account.owner_name, account.currency),
    ).fetchone()
    return row


@app.get("/accounts/{account_id}", response_model=AccountOut)
def get_account(account_id: int, conn=Depends(get_conn)):
    row = conn.execute(
        "SELECT id, owner_name, currency, balance, created_at FROM account WHERE id = %s",
        (account_id,),
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Account id {account_id} not found")
    return row


@app.get("/accounts", response_model=list[AccountOut])
def get_all_accounts(conn=Depends(get_conn)):
    rows = conn.execute(
        "SELECT id, owner_name, currency, balance, created_at FROM account ORDER BY id"
    ).fetchall()
    return rows


@app.get("/")
def root(conn=Depends(get_conn)):
    conn.execute("SELECT 1")
    return{"message": "Home Page"}


@app.get("/health")
def health(conn=Depends(get_conn)):
    conn.execute("SELECT 1")
    return{"status": "ok"}
