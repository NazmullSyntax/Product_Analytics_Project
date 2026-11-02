-- ============================================================
-- REVENUE ANALYTICS QUERIES
-- ============================================================

-- 1. Overall Business KPIs
SELECT 
    ROUND(SUM("TotalAmount")::numeric, 2) AS total_revenue,
    COUNT(DISTINCT "Invoice") AS total_orders,
    COUNT(DISTINCT "CustomerID") AS total_customers,
    SUM("Quantity") AS total_units_sold,
    ROUND((SUM("TotalAmount") / COUNT(DISTINCT "Invoice"))::numeric, 2) AS avg_order_value
FROM retail_transactions;

-- 2. Monthly Revenue Trend (Line chart for dashboard)
SELECT 
    DATE_TRUNC('month', "InvoiceDate")::date AS month,
    ROUND(SUM("TotalAmount")::numeric, 2) AS monthly_revenue,
    COUNT(DISTINCT "Invoice") AS orders
FROM retail_transactions
GROUP BY DATE_TRUNC('month', "InvoiceDate")
ORDER BY month;

-- 3. Daily Revenue Trend (Last 30 days)
SELECT 
    "InvoiceDate"::date AS day,
    ROUND(SUM("TotalAmount")::numeric, 2) AS daily_revenue
FROM retail_transactions
GROUP BY "InvoiceDate"::date
ORDER BY day DESC
LIMIT 30;

-- 4. Revenue by Country (Top 10)
SELECT 
    "Country",
    COUNT(DISTINCT "CustomerID") AS customers,
    ROUND(SUM("TotalAmount")::numeric, 2) AS country_revenue
FROM retail_transactions
GROUP BY "Country"
ORDER BY country_revenue DESC
LIMIT 10;

-- 5. Year-over-Year Growth
SELECT 
    EXTRACT(YEAR FROM "InvoiceDate") AS year,
    ROUND(SUM("TotalAmount")::numeric, 2) AS revenue
FROM retail_transactions
GROUP BY EXTRACT(YEAR FROM "InvoiceDate")
ORDER BY year;