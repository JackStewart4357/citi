from pathlib import Path

import psycopg
import pytest

from app.db import DATABASE_URL

SEED_FILE = Path(__file__).parent.parent / "db" / "seed.sql"


@pytest.fixture(autouse=True)
def reset_database():
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute("TRUNCATE btransaction, account RESTART IDENTITY")
        conn.execute(SEED_FILE.read_text())