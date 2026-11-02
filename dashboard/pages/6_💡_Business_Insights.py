import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_kpis, get_top_products, get_rfm_segments, run_query
from styles import inject_css

st.set_page_config(page_title="Business Insights", page_icon="💡", layout="wide")
inject_css()

st.markdown('<div class="page-title">💡 Business Insights & Recommendations</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Data-driven actions based on real analysis</div>', unsafe_allow_html=True)

kpis = get_kpis().iloc[0]
df_rfm = get_rfm_segments()

champion_pct = (len(df_rfm[df_rfm['segment']=='Champion']) / len(df_rfm)) * 100
lost_pct = (len(df_rfm[df_rfm['segment']=='Lost']) / len(df_rfm)) * 100
champion_rev = df_rfm[df_rfm['segment']=='Champion']['monetary'].sum() / df_rfm['monetary'].sum() * 100

insights = [
    ("🏆 Customer Concentration", 
     f"Champions ({champion_pct:.1f}% of customers) generate {champion_rev:.1f}% of revenue.",
     "Create a VIP loyalty program for Champions to retain them."),
    
    ("⚠️ Customer Churn", 
     f"{lost_pct:.1f}% of customers are 'Lost' (no recent purchase).",
     "Launch a win-back campaign with special discounts for inactive users."),
     
    ("📅 Seasonal Peak", 
     "Revenue spiked in November 2011 (holiday season).",
     "Plan inventory and marketing campaigns for Q4 holiday season."),
     
    ("🌍 Market Concentration", 
     "The UK generates ~85% of all revenue.",
     "Diversify into European markets (Germany, France) to reduce dependency."),
     
    ("📦 Pareto Principle", 
     "~23% of products generate 80% of revenue.",
     "Focus inventory and promotions on the top 20% of SKUs."),
     
    ("💰 AOV Benchmark", 
     f"Current AOV is £{kpis['aov']:.2f}.",
     "Implement cross-selling to increase AOV by 10-15%."),
]

for i, (title, finding, action) in enumerate(insights, 1):
    with st.container():
        st.markdown(f"### {i}. {title}")
        st.info(f"**Finding:** {finding}")
        st.success(f"**Recommended Action:** {action}")
        st.markdown("---")