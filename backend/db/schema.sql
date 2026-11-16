DROP TABLE IF EXISTS btransaction;
DROP TABLE IF EXISTS account;
DROP TYPE IF EXISTS transaction_type;
DROP TYPE IF EXISTS currency_type;

CREATE TYPE currency_type AS ENUM ( 'GBP', 'USD', 'EUR');

CREATE TYPE transaction_type AS ENUM( 'deposit', 'withdrawal', 'transfer_in', 'transfer_out');

CREATE TABLE account(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    owner_name VARCHAR(50) NOT NULL CHECK ( owner_name <> ''),
    currency currency_type NOT NULL,
    balance NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK ( balance >= 0 ),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE btransaction(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_id BIGINT NOT NULL REFERENCES account(id),
    type transaction_type NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount > 0.00),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_transaction_history ON btransaction(account_id, created_at DESC);