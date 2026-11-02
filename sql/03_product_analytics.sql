-- ============================================================
-- PRODUCT ANALYTICS QUERIES
-- ============================================================

-- 1. Top 20 Best-Selling Products by Revenue
SELECT 
    "StockCode",
    "Description",
    SUM("Quantity") AS units_sold,
    ROUND(SUM("TotalAmount")::numeric, 2) AS revenue
FROM retail_transactions
GROUP BY "StockCode", "Description"
ORDER BY revenue DESC
LIMIT 20;

-- 2. Bottom 20 Products (Low Performers)
SELECT 
    "StockCode",
    "Description",
    SUM("Quantity") AS units_sold,
    ROUND(SUM("TotalAmount")::numeric, 2) AS revenue
FROM retail_transactions
GROUP BY "StockCode", "Description"
HAVING SUM("Quantity") > 0
ORDER BY revenue ASC
LIMIT 20;

-- 3. Products by Unique Customers (Popularity)
SELECT 
    "StockCode",
    "Description",
    COUNT(DISTINCT "CustomerID") AS unique_customers,
    ROUND(SUM("TotalAmount")::numeric, 2) AS revenue
FROM retail_transactions
GROUP BY "StockCode", "Description"
ORDER BY unique_customers DESC
LIMIT 20;

-- 4. AOV per Product
SELECT 
    "StockCode",
    "Description",
    COUNT(DISTINCT "Invoice") AS orders_containing,
    ROUND((SUM("TotalAmount") / COUNT(DISTINCT "Invoice"))::numeric, 2) AS avg_order_value
FROM retail_transactions
GROUP BY "StockCode", "Description"
HAVING COUNT(DISTINCT "Invoice") > 50
ORDER BY avg_order_value DESC
LIMIT 20;