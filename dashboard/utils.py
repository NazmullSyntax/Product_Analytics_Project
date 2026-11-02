import os
import streamlit as st
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

@st.cache_resource
def get_engine():
    """Create a cached SQLAlchemy engine."""
    return create_engine(DATABASE_URL)

@st.cache_data(ttl=600)
def run_query(query: str) -> pd.DataFrame:
    """Run a SQL query and cache the result for 10 minutes."""
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=600)
def get_kpis():
    return run_query("""
        SELECT 
            ROUND(SUM("TotalAmount")::numeric, 2) AS total_revenue,
            COUNT(DISTINCT "Invoice") AS total_orders,
            COUNT(DISTINCT "CustomerID") AS total_customers,
            SUM("Quantity") AS total_units,
            ROUND((SUM("TotalAmount") / COUNT(DISTINCT "Invoice"))::numeric, 2) AS aov
        FROM retail_transactions;
    """)

@st.cache_data(ttl=600)
def get_monthly_revenue():
    return run_query("""
        SELECT 
            DATE_TRUNC('month', "InvoiceDate")::date AS month,
            ROUND(SUM("TotalAmount")::numeric, 2) AS revenue,
            COUNT(DISTINCT "Invoice") AS orders
        FROM retail_transactions
        GROUP BY DATE_TRUNC('month', "InvoiceDate")
        ORDER BY month;
    """)

@st.cache_data(ttl=600)
def get_top_products(limit=10):
    return run_query(f"""
        SELECT 
            "Description",
            SUM("Quantity") AS units_sold,
            ROUND(SUM("TotalAmount")::numeric, 2) AS revenue
        FROM retail_transactions
        GROUP BY "Description"
        ORDER BY revenue DESC
        LIMIT {limit};
    """)

@st.cache_data(ttl=600)
def get_country_revenue():
    return run_query("""
        SELECT 
            "Country",
            ROUND(SUM("TotalAmount")::numeric, 2) AS revenue
        FROM retail_transactions
        GROUP BY "Country"
        ORDER BY revenue DESC
        LIMIT 10;
    """)

@st.cache_data(ttl=600)
def get_rfm_segments():
    return run_query("""
        WITH customer_metrics AS (
            SELECT 
                "CustomerID",
                MAX("InvoiceDate")::date AS last_purchase_date,
                COUNT(DISTINCT "Invoice") AS frequency,
                SUM("TotalAmount") AS monetary
            FROM retail_transactions
            GROUP BY "CustomerID"
        ),
        rfm AS (
            SELECT 
                "CustomerID",
                (SELECT MAX("InvoiceDate")::date FROM retail_transactions) - last_purchase_date AS recency_days,
                frequency, monetary
            FROM customer_metrics
        ),
        rfm_scores AS (
            SELECT 
                "CustomerID", recency_days, frequency, monetary,
                NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
                NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
                NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
            FROM rfm
        )
        SELECT 
            "CustomerID", recency_days, frequency,
            ROUND(monetary::numeric, 2) AS monetary,
            CASE 
                WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champion'
                WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal'
                WHEN r_score >= 4 AND f_score <= 2 THEN 'New Customer'
                WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
                WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
                ELSE 'Potential Loyalist'
            END AS segment
        FROM rfm_scores;
    """)