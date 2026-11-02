import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_kpis, get_monthly_revenue, get_top_products, get_country_revenue
from styles import inject_css

st.set_page_config(page_title="Executive Overview", page_icon="📊", layout="wide")
inject_css()

st.markdown('<div class="page-title">📊 Executive Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">High-level business KPIs from 2009-2011</div>', unsafe_allow_html=True)

# ============ KPI CARDS ============
kpis = get_kpis().iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Revenue", f"£{kpis['total_revenue']:,.0f}")
with col2:
    st.metric("📦 Total Orders", f"{kpis['total_orders']:,}")
with col3:
    st.metric("👥 Total Customers", f"{kpis['total_customers']:,}")
with col4:
    st.metric("💵 Avg Order Value", f"£{kpis['aov']:,.2f}")

st.markdown("---")

# ============ MONTHLY REVENUE ============
st.markdown("### 📈 Monthly Revenue Trend")
df_monthly = get_monthly_revenue()
df_monthly['month'] = df_monthly['month'].astype(str)

fig = px.line(
    df_monthly, x='month', y='revenue', markers=True,
    color_discrete_sequence=['#FF4B8B'],
    labels={'revenue': 'Revenue (£)', 'month': 'Month'}
)
fig.update_traces(line=dict(width=3))
fig.update_layout(
    plot_bgcolor='white', paper_bgcolor='white',
    height=400, margin=dict(l=20, r=20, t=20, b=20),
    hovermode='x unified'
)
st.plotly_chart(fig, use_container_width=True)

# ============ TOP PRODUCTS + COUNTRY ============
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏆 Top 10 Products by Revenue")
    df_top = get_top_products(limit=10)
    fig = px.bar(
        df_top, x='revenue', y='Description', orientation='h',
        color='revenue', color_continuous_scale='RdPu',
        labels={'revenue': 'Revenue (£)', 'Description': ''}
    )
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', height=400,
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🌍 Revenue by Country (Top 10)")
    df_country = get_country_revenue()
    fig = px.pie(
        df_country, values='revenue', names='Country',
        color_discrete_sequence=px.colors.sequential.RdPu_r, hole=0.4
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)