import streamlit as st
from styles import inject_css

st.set_page_config(
    page_title="Product & User Behavior Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()

# Welcome page (default)
st.markdown('<div class="page-title">📊 Product & User Behavior Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">End-to-End Data Analytics Dashboard • PostgreSQL + Streamlit</div>', unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🎯 Project Overview")
    st.write("""
    This dashboard analyzes **780,000+ real transactions** from an online retail business (2009–2011). 
    It provides insights into customer behavior, product performance, revenue trends, and retention patterns.
    """)

with col2:
    st.markdown("### 🗂️ Navigation")
    st.write("""
    Use the **sidebar** to navigate between pages:
    - 📊 Executive Overview
    - 👥 User Analytics
    - 📦 Product Analytics
    - 💰 Revenue Analytics
    - 🔁 Retention & Cohorts
    - 💡 Business Insights
    """)

with col3:
    st.markdown("### ⚙️ Tech Stack")
    st.write("""
    - **Database:** PostgreSQL (Neon Cloud)
    - **Data Processing:** Python, Pandas, SQLAlchemy
    - **Visualizations:** Plotly, Matplotlib
    - **Dashboard:** Streamlit
    """)

st.markdown("---")
st.info("💡 **Tip:** Start with the **Executive Overview** page for high-level KPIs.")