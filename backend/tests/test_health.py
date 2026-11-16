from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status":"ok"}


def test_account_creation():
    response = client.post("/accounts", json={"owner_name": "Test Person", "currency": "GBP"})
    assert response.status_code == 200
    body = response.json()
    assert body["owner_name"] == "Test Person"
    assert float(body["balance"]) == 0

def test_incorrect_account_creation_currency():
    response = client.post("/accounts", json={"owner_name": "Tester Person", "currency": "ABP"})
    assert response.status_code == 422

def test_unknown_accountid():
    response = client.get("/accounts/999999999999")
    assert response.status_code == 404


def test_deposit_increases_balance():
    response = client.post("/accounts/1/deposits", json={"amount": "100.00"})
    assert response.status_code == 201
    assert response.json()["balance"] == "1450.00"
