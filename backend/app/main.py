from fastapi import Depends, FastAPI

from app.db import get_conn

app = FastAPI(title = "Ledger Lite")


@app.get("/")
def root(conn=Depends(get_conn)):
    conn.execute("SELECT 1")
    return{"message": "Home Page"}


@app.get("/health")
def health(conn=Depends(get_conn)):
    conn.execute("SELECT 1")
    return{"message": "ok"}

@app.get("/accounts")
def accounts(conn=Depends(get_conn)):
    conn.execute("SELECT 1")
    return{"message": "ok"}
