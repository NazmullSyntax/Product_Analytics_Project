import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import run_query
from styles import inject_css

st.set_page_config(page_title="Retention", page_icon="🔁", layout="wide")
inject_css()

st.markdown('<div class="page-title">🔁 Customer Retention & Cohorts</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">How well do we keep customers coming back?</div>', unsafe_allow_html=True)

df_cohort = run_query("""
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
    COUNT(DISTINCT CASE WHEN DATE_TRUNC('month', t."InvoiceDate") = fp.cohort_month + INTERVAL '1 month' THEN t."CustomerID" END) AS month_1,
    COUNT(DISTINCT CASE WHEN DATE_TRUNC('month', t."InvoiceDate") = fp.cohort_month + INTERVAL '3 month' THEN t."CustomerID" END) AS month_3,
    COUNT(DISTINCT CASE WHEN DATE_TRUNC('month', t."InvoiceDate") = fp.cohort_month + INTERVAL '6 month' THEN t."CustomerID" END) AS month_6
FROM first_purchase fp
LEFT JOIN retail_transactions t ON fp."CustomerID" = t."CustomerID"
GROUP BY fp.cohort_month
ORDER BY fp.cohort_month;
""")

df_cohort['Month 1 %'] = (df_cohort['month_1'] / df_cohort['cohort_size'] * 100).round(1)
df_cohort['Month 3 %'] = (df_cohort['month_3'] / df_cohort['cohort_size'] * 100).round(1)
df_cohort['Month 6 %'] = (df_cohort['month_6'] / df_cohort['cohort_size'] * 100).round(1)
df_cohort['cohort_month'] = df_cohort['cohort_month'].astype(str)

st.markdown("### 📊 Cohort Retention Heatmap")
fig = px.imshow(
    df_cohort[['Month 1 %', 'Month 3 %', 'Month 6 %']].values.T,
    x=df_cohort['cohort_month'],
    y=['Month 1', 'Month 3', 'Month 6'],
    color_continuous_scale='RdPu',
    text_auto=True,
    labels=dict(x="Cohort Month", y="Retention Period", color="Retention %")
)
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

st.download_button(
    label="📥 Download Cohort Data (CSV)",
    data=df_cohort.to_csv(index=False).encode('utf-8'),
    file_name='cohort_retention.csv',
    mime='text/csv',
)