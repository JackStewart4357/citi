from fastapi import Depends, FastAPI, HTTPException
from typing import Literal
from pydantic import BaseModel, Field
from app.db import get_conn

app = FastAPI(title = "Ledger Lite")


class AccountCreate(BaseModel): 
    owner_name: str = Field(min_length=1, max_length=100)
    currency: Literal["GBP","USD","EUR"]

@app.post("/accounts")
def createAccount(account: AccountCreate, conn=Depends(get_conn)):
    row = conn.execute(
        "INSERT INTO account (owner_name, currency) VALUES (%s, %s) RETURNING *", (account.owner_name, account.currency)
    ).fetchone()
    return row

@app.get("/accounts/{account_id}")
def get_account(account_id: int, conn=Depends(get_conn)):
    row = conn.execute(
        "SELECT id, owner_name, currency, balance, created_at FROM account WHERE id = %s", (account_id,),
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail = f"Account id {account_id} not found")
    return row

@app.get("/accounts")
def get_all_accounts(conn=Depends(get_conn)):
    rows = conn.execute(
        "SELECT * FROM account"
    ).fetchall()
    return rows


@app.get("/")
def root(conn=Depends(get_conn)):
    conn.execute("SELECT 1")
    return{"message": "Home Page"}


@app.get("/health")
def health(conn=Depends(get_conn)):
    conn.execute("SELECT 1")
    return{"message": "ok"}
