--@name: transactions
SELECT * FROM transactions;

--@name: net_worth_over_time
SELECT
    date,
    SUM(amount) OVER (ORDER BY date) AS net_worth
FROM 
    transactions;

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

--@name: amount_over_time
SELECT
    date,
    SUM(amount) OVER (ORDER BY date) AS net_worth,
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

--@name: expenses_per_category
SELECT
    category,
    ROUND(ABS(SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END))::numeric) as expenses
FROM
    transactions
GROUP BY
    category
HAVING
    SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) <> 0
ORDER BY
	expenses DESC;

--@name: income_per_category
SELECT
    category,
    ROUND(ABS(SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END))::numeric) as income
FROM
    transactions
GROUP BY
    category
HAVING
    SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) <> 0
ORDER BY
	income DESC;