# 📊 Product & User Behavior Analytics Dashboard

An end-to-end data analytics and BI project analyzing **780,000+ e-commerce transactions** from 2009–2011. This project demonstrates the full data pipeline: from raw CSV to PostgreSQL, to advanced analytics, to an interactive Streamlit dashboard.

## 🎯 Overview

The Online Retail II dataset from UCI Machine Learning Repository is processed through a complete analytics pipeline to answer critical business questions:
- Who are our most valuable customers?
- Which products drive the most revenue?
- What is our customer retention rate?
- How do revenue trends change over time?

## 🗂️ Project Architecture

Raw CSV → Python Cleaning → PostgreSQL (Neon Cloud) → SQL Analytics → Streamlit Dashboard
## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Data Processing | Python, Pandas, NumPy |
| Database | PostgreSQL (Neon Cloud) |
| ORM | SQLAlchemy, psycopg |
| Visualizations | Plotly, Matplotlib |
| Dashboard | Streamlit |
| Testing | pytest |
| Version Control | Git, GitHub |

## ✨ Features

### Dashboard Pages
1. **📊 Executive Overview** — Total revenue, orders, customers, AOV, monthly trend, top products, country distribution.
2. **👥 User Analytics** — RFM segmentation (Champions, Loyal, At Risk, Lost), revenue by segment, customer scatter plot.
3. **📦 Product Analytics** — Top 20 products, Pareto principle (80/20 rule), revenue concentration.
4. **💰 Revenue Analytics** — Monthly revenue + MoM growth, country breakdown.
5. **🔁 Retention & Cohorts** — Cohort retention heatmap (Month 1/3/6).
6. **💡 Business Insights** — 10 data-driven recommendations.

### Key Business Findings
- **Champions (22.8%)** generate **68.8%** of revenue.
- **25.8%** of customers are 'Lost' (high churn risk).
- **~23%** of products drive **80%** of revenue (Pareto principle).
- UK generates **~85%** of total revenue.
- **November 2011** peak: **£1.17M** revenue (holiday season).

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL (or Neon Cloud account)
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/product-analytics-dashboard.git
cd product-analytics-dashboard

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your DATABASE_URL

# 5. Load data into database
cd src
python load_to_db.py
cd ..

# 6. Run the dashboard
streamlit run dashboard/app.py