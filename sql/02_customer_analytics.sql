-- ============================================================
-- CUSTOMER ANALYTICS QUERIES
-- ============================================================

-- 1. Customer Segments (RFM-like)
SELECT 
    "CustomerID",
    ROUND(SUM("TotalAmount")::numeric, 2) AS total_spent,
    COUNT(DISTINCT "Invoice") AS total_orders,
    MAX("InvoiceDate")::date AS last_purchase
FROM retail_transactions
GROUP BY "CustomerID"
ORDER BY total_spent DESC
LIMIT 20;

-- 2. Top 20 Customers by Revenue
SELECT 
    "CustomerID",
    ROUND(SUM("TotalAmount")::numeric, 2) AS revenue,
    COUNT(DISTINCT "Invoice") AS orders,
    ROUND((SUM("TotalAmount") / COUNT(DISTINCT "Invoice"))::numeric, 2) AS avg_order_value
FROM retail_transactions
GROUP BY "CustomerID"
ORDER BY revenue DESC
LIMIT 20;

-- 3. New vs Returning Customers (monthly)
WITH first_purchase AS (
    SELECT 
        "CustomerID",
        MIN("InvoiceDate") AS first_date
    FROM retail_transactions
    GROUP BY "CustomerID"
)
SELECT 
    DATE_TRUNC('month', t."InvoiceDate")::date AS month,
    COUNT(DISTINCT CASE WHEN t."InvoiceDate" = fp.first_date THEN t."CustomerID" END) AS new_customers,
    COUNT(DISTINCT CASE WHEN t."InvoiceDate" > fp.first_date THEN t."CustomerID" END) AS returning_customers
FROM retail_transactions t
JOIN first_purchase fp ON t."CustomerID" = fp."CustomerID"
GROUP BY DATE_TRUNC('month', t."InvoiceDate")
ORDER BY month;

-- 4. Customer Retention Cohort
WITH first_purchase AS (
    SELECT 
        "CustomerID",
        DATE_TRUNC('month', MIN("InvoiceDate"))::date AS cohort_month
    FROM retail_transactions
    GROUP BY "CustomerID"
)
SELECT 
    fp.cohort_month,
    COUNT(DISTINCT fp."CustomerID") AS cohort_size,
    COUNT(DISTINCT CASE WHEN DATE_TRUNC('month', t."InvoiceDate") = fp.cohort_month + INTERVAL '1 month' THEN t."CustomerID" END) AS month_1_retained,
    COUNT(DISTINCT CASE WHEN DATE_TRUNC('month', t."InvoiceDate") = fp.cohort_month + INTERVAL '3 month' THEN t."CustomerID" END) AS month_3_retained
FROM first_purchase fp
LEFT JOIN retail_transactions t ON fp."CustomerID" = t."CustomerID"
GROUP BY fp.cohort_month
ORDER BY fp.cohort_month;