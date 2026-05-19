-- =============================================
-- TRANSACTION ANALYSIS QUERIES
-- =============================================

-- 1. Ukupna potrošnja po korisniku
SELECT
    user_id,
    COUNT(*)            AS broj_transakcija,
    SUM(amount)         AS ukupno_potroseno,
    AVG(amount)         AS prosecna_transakcija,
    MAX(amount)         AS najveca_transakcija
FROM transactions
GROUP BY user_id
ORDER BY ukupno_potroseno DESC;

-- 2. Potrošnja po kategoriji
SELECT
    category,
    COUNT(*)        AS broj_transakcija,
    SUM(amount)     AS ukupno,
    ROUND(AVG(amount), 2) AS prosek
FROM transactions
GROUP BY category
ORDER BY ukupno DESC;

-- 3. Dnevna potrošnja (trend)
SELECT
    tx_date,
    COUNT(*)    AS broj_transakcija,
    SUM(amount) AS dnevni_ukupno
FROM transactions
GROUP BY tx_date
ORDER BY tx_date;

-- 4. Top korisnici po kategoriji
SELECT
    user_id,
    category,
    SUM(amount) AS ukupno
FROM transactions
GROUP BY user_id, category
ORDER BY user_id, ukupno DESC;

-- 5. Transakcije iznad proseka (anomalije)
SELECT *
FROM transactions
WHERE amount > (SELECT AVG(amount) FROM transactions)
ORDER BY amount DESC;