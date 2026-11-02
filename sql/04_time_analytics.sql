-- ============================================================
-- TIME-BASED ANALYTICS QUERIES
-- ============================================================

-- 1. Revenue by Day of Week
SELECT 
    TO_CHAR("InvoiceDate", 'Day') AS day_of_week,
    EXTRACT(DOW FROM "InvoiceDate") AS dow_num,
    ROUND(SUM("TotalAmount")::numeric, 2) AS total_revenue
FROM retail_transactions
GROUP BY day_of_week, dow_num
ORDER BY dow_num;

-- 2. Revenue by Hour of Day
SELECT 
    EXTRACT(HOUR FROM "InvoiceDate") AS hour,
    ROUND(SUM("TotalAmount")::numeric, 2) AS revenue,
    COUNT(DISTINCT "Invoice") AS orders
FROM retail_transactions
GROUP BY hour
ORDER BY hour;

-- 3. Month-over-Month Growth (window function)
WITH monthly_revenue AS (
    SELECT 
        DATE_TRUNC('month', "InvoiceDate")::date AS month,
        SUM("TotalAmount") AS revenue
    FROM retail_transactions
    GROUP BY DATE_TRUNC('month', "InvoiceDate")
)
SELECT 
    month,
    ROUND(revenue::numeric, 2) AS revenue,
    ROUND(LAG(revenue) OVER (ORDER BY month)::numeric, 2) AS prev_month,
    ROUND(((revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month) * 100)::numeric, 2) AS mom_growth_pct
FROM monthly_revenue
ORDER BY month;