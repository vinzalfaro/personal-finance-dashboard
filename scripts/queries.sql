--@name: transactions
SELECT * FROM transactions

--@name: net_worth_over_time
SELECT
    date,
    SUM(net_amount) OVER (ORDER BY date) AS net_worth
FROM (
    SELECT
        date,
        SUM(amount) AS net_amount
    FROM
        transactions
    GROUP BY
        date);

