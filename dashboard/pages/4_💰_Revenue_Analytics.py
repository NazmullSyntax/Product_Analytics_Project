import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_monthly_revenue, get_country_revenue
from styles import inject_css

st.set_page_config(page_title="Revenue Analytics", page_icon="💰", layout="wide")
inject_css()

st.markdown('<div class="page-title">💰 Revenue Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Trends, growth, and geographic breakdown</div>', unsafe_allow_html=True)

df_monthly = get_monthly_revenue()
df_monthly['month'] = df_monthly['month'].astype(str)

st.markdown("### 📈 Monthly Revenue & MoM Growth")
fig = go.Figure()
fig.add_trace(go.Bar(x=df_monthly['month'], y=df_monthly['revenue'], name='Revenue', marker_color='#FFB6C1'))
fig.add_trace(go.Scatter(
    x=df_monthly['month'], 
    y=df_monthly['revenue'].pct_change() * 100, 
    name='MoM Growth %', 
    yaxis='y2', 
    line=dict(color='#FF4B8B', width=3)
))
fig.update_layout(
    height=450,
    yaxis=dict(title='Revenue (£)'),
    yaxis2=dict(title='MoM Growth %', overlaying='y', side='right'),
    hovermode='x unified'
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("### 🌍 Country Breakdown")

df_country = get_country_revenue()
fig = px.pie(
    df_country, values='revenue', names='Country', hole=0.4,
    color_discrete_sequence=px.colors.sequential.RdPu_r
)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

st.download_button(
    label="📥 Download Revenue Data (CSV)",
    data=df_monthly.to_csv(index=False).encode('utf-8'),
    file_name='revenue_trends.csv',
    mime='text/csv',
)