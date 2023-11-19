--@name: transactions
SELECT * FROM transactions;

--@name: net_worth_over_time
SELECT
    date,
    SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS net_worth
FROM transactions;

--@name: accounts_over_time
SELECT
    date,
    SUM(CASE WHEN Account = 'Wallet' THEN amount ELSE 0 END) OVER (ORDER BY date) AS wallet,
    SUM(CASE WHEN Account = 'Union Bank' THEN amount ELSE 0 END) OVER (ORDER BY date) AS unionbank,
    SUM(CASE WHEN Account = 'Seabank' THEN amount ELSE 0 END) OVER (ORDER BY date) AS seabank,
    SUM(CASE WHEN Account = 'GCash' THEN amount ELSE 0 END) OVER (ORDER BY date) AS gcash,
    SUM(CASE WHEN Account = 'Maya' THEN amount ELSE 0 END) OVER (ORDER BY date) AS maya,
    SUM(CASE WHEN Account = 'GrabPay' THEN amount ELSE 0 END) OVER (ORDER BY date) AS grabpay,
    SUM(CASE WHEN Account = 'ShopeePay' THEN amount ELSE 0 END) OVER (ORDER BY date) AS shopeepay,
    SUM(CASE WHEN Account = 'Binance' THEN amount ELSE 0 END) OVER (ORDER BY date) AS binance,
    SUM(CASE WHEN Account = 'Ronin' THEN amount ELSE 0 END) OVER (ORDER BY date) AS ronin
FROM
    transactions
ORDER BY
    date;