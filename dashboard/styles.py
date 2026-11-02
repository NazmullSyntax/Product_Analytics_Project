import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    /* Main container */
    .main {
        background-color: #F5F5F7;
    }

    /* KPI Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9F9FB 100%);
        border: 1px solid #E5E5EA;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    div[data-testid="stMetric"] label {
        color: #6E6E73;
        font-weight: 500;
        font-size: 14px;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #1D1D1F;
        font-size: 32px;
        font-weight: 700;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F9F0F5 100%);
        border-right: 1px solid #F0F0F2;
    }

    /* Header */
    h1 {
        color: #1D1D1F;
        font-weight: 800;
    }

    h2 {
        color: #1D1D1F;
        font-weight: 700;
        margin-top: 20px;
    }

    h3 {
        color: #FF4B8B;
        font-weight: 600;
    }

    /* Page title */
    .page-title {
        font-size: 32px;
        font-weight: 800;
        color: #1D1D1F;
        margin-bottom: 8px;
    }

    .page-subtitle {
        color: #6E6E73;
        font-size: 15px;
        margin-bottom: 24px;
    }

    /* Hide default Streamlit menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)