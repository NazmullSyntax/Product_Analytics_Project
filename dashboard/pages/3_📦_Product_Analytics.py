import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_top_products, run_query
from styles import inject_css

st.set_page_config(page_title="Product Analytics", page_icon="📦", layout="wide")
inject_css()

st.markdown('<div class="page-title">📦 Product Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Top performers and Pareto analysis</div>', unsafe_allow_html=True)

# Top products
df_top = get_top_products(limit=20)

st.markdown("### 🏆 Top 20 Products by Revenue")
fig = px.bar(
    df_top, x='revenue', y='Description', orientation='h',
    color='revenue', color_continuous_scale='RdPu',
    labels={'revenue': 'Revenue (£)', 'Description': ''}
)
fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Pareto Query
st.markdown("---")
st.markdown("### 📊 Pareto Principle (80/20 Rule)")

df_pareto = run_query("""
WITH product_revenue AS (
    SELECT "Description", SUM("TotalAmount") AS revenue
    FROM retail_transactions
    GROUP BY "Description"
    HAVING SUM("TotalAmount") > 0
),
ranked AS (
    SELECT 
        revenue,
        SUM(revenue) OVER (ORDER BY revenue DESC) AS cumulative_revenue,
        SUM(revenue) OVER () AS total_revenue,
        ROW_NUMBER() OVER (ORDER BY revenue DESC) AS rnk,
        COUNT(*) OVER () AS total_products
    FROM product_revenue
)
SELECT 
    rnk,
    ROUND(revenue::numeric, 2) AS revenue,
    ROUND((cumulative_revenue / total_revenue * 100)::numeric, 2) AS cumulative_pct
FROM ranked
ORDER BY rnk;
""")

fig = px.line(
    df_pareto, x='rnk', y='cumulative_pct', 
    labels={'rnk': 'Product Rank', 'cumulative_pct': 'Cumulative Revenue %'},
    color_discrete_sequence=['#FF4B8B']
)
fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="80% threshold")
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

st.download_button(
    label="📥 Download Top 50 Products (CSV)",
    data=df_top.to_csv(index=False).encode('utf-8'),
    file_name='top_products.csv',
    mime='text/csv',
)