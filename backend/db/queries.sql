-- 1. All GBP accounts, highest balance first.

SELECT owner_name, type
FROM account
WHERE type = 'GBP'
ORDER BY balance DESC;

-- 2. All transactions for account 1, newest first
SELECT account_id, type, amount, created_at
FROM btransaction
WHERE account_id = 1
ORDER BY created_at DESC;

-- 3. Each owner name with their number of transactions.
SELECT a.owner_name, COUNT(b.id) AS number_of_transactions
FROM account a
JOIN btransaction b ON a.id = b.account_id
GROUP BY a.owner_name
ORDER BY number_of_transactions DESC;

-- 4. Total deposited per account (type deposit only).

SELECT SUM(amount), type, account_id
FROM btransaction b WHERE type = 'deposit'
GROUP BY b.type, account_id;

-- 5. Owners who have never sent or received a transfer

SELECT owner_name
FROM account
WHERE id NOT IN (
    SELECT account_id
    FROM btransaction
    WHERE type = 'transfer_in' OR type = 'transfer_out'
);

-- 6. The largest single transaction amount per account

SELECT MAX(amount), account_id
FROM btransaction
GROUP BY account_id
ORDER BY account_id ASC;
