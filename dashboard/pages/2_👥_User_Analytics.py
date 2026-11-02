import streamlit as st
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_rfm_segments
from styles import inject_css

st.set_page_config(page_title="User Analytics", page_icon="👥", layout="wide")
inject_css()

st.markdown('<div class="page-title">👥 User Analytics & Segmentation</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">RFM Analysis (Recency, Frequency, Monetary)</div>', unsafe_allow_html=True)

# Load RFM data
df_rfm = get_rfm_segments()

# Top-level metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Customers", f"{len(df_rfm):,}")
with col2:
    champions = len(df_rfm[df_rfm['segment'] == 'Champion'])
    st.metric("🏆 Champions", f"{champions:,}")
with col3:
    lost = len(df_rfm[df_rfm['segment'] == 'Lost'])
    st.metric("⚠️ Lost Customers", f"{lost:,}", delta="-25.8%", delta_color="inverse")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Customer Distribution by Segment")
    segment_counts = df_rfm['segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    fig = px.pie(
        segment_counts, values='Count', names='Segment', hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdPu_r
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 💰 Revenue by Segment")
    segment_rev = df_rfm.groupby('segment')['monetary'].sum().reset_index()
    segment_rev = segment_rev.sort_values('monetary', ascending=True)
    fig = px.bar(
        segment_rev, x='monetary', y='segment', orientation='h',
        color='monetary', color_continuous_scale='RdPu',
        labels={'monetary': 'Total Revenue (£)', 'segment': ''}
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# RFM Scatter
st.markdown("### 🎯 RFM Scatter Plot (Frequency vs Monetary)")
fig = px.scatter(
    df_rfm.sample(min(2000, len(df_rfm))), 
    x='frequency', y='monetary', 
    size='monetary', color='segment',
    hover_data=['CustomerID', 'recency_days'],
    labels={'frequency': 'Number of Orders', 'monetary': 'Total Spent (£)'},
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# Download button
st.download_button(
    label="📥 Download Full RFM Data (CSV)",
    data=df_rfm.to_csv(index=False).encode('utf-8'),
    file_name='rfm_segments.csv',
    mime='text/csv',
)