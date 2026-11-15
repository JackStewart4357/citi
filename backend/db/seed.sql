
INSERT INTO account (owner_name, type) VALUES ('Aoife Byrne', 'GBP');
INSERT INTO account (owner_name, type) VALUES ('Marcus Chen', 'GBP');
INSERT INTO account (owner_name, type) VALUES ('Priya Nair', 'USD');
INSERT INTO account (owner_name, type) VALUES ('Tomas Keller', 'EUR');


INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (1, 'deposit', 1500, '2026-10-01');
INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (2, 'deposit', 800, '2026-10-01');
INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (3, 'deposit', 2500, '2026-10-02');
INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (4, 'deposit', 600, '2026-10-03');
INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (1, 'withdrawal', 200, '2026-10-10');
INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (1, 'transfer_out', 300, '2026-10-14');
INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (2, 'transfer_in', 300, '2026-10-14');
INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (3, 'withdrawal', 450.5, '2026-10-20');
INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (2, 'withdrawal', 120.25, '2026-11-02');
INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (1, 'deposit', 250, '2026-11-05');
INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (2, 'transfer_out', 100, '2026-11-09');
INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (1, 'transfer_in', 100, '2026-11-09');
INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (4, 'withdrawal', 75, '2026-11-11');
INSERT INTO btransaction (account_id, type, amount, created_at) VALUES (3, 'deposit', 1000, '2026-11-12');

UPDATE account a
SET balance = (
    SELECT COALESCE(SUM(CASE WHEN t.type IN ('deposit', 'transfer_in') THEN t.amount ELSE -t.amount END), 0)
    FROM btransaction t
    WHERE t.account_ID = a.id
);