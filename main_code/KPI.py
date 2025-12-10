import streamlit as st 
import pandas as pd
import base64
from pathlib import Path
import plotly.express as px

# ---------------- Page Config ----------------
st.set_page_config(layout='wide', page_title='Housing Dashboard')

st.sidebar.success("ALL Dashboards")

px.defaults.template = "plotly_dark"

# ---------------- Load Data ----------------
@st.cache_data
def load_dataset(path):
    return pd.read_csv(path)

path = './dataset/cleaned_housing.csv'
df = load_dataset(path)
dff = df.copy()

# ---------------- KPI Page Title ----------------
st.title("📊 Key Performance Indicators (KPI)")

# ---------------- UPDATED BIG KPI CSS ----------------
css_kpis = """
<style>

.kpi-row {
    position: relative;
    z-index: 2;
    display: flex;
    flex-wrap: wrap;
    gap: 22px;
    margin-bottom: 22px;
    padding-top: 12px;
}

/* Bigger KPI card */
.kpi-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03));
    border-radius: 18px;
    padding: 26px 30px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.55);
    border: 1px solid rgba(255,255,255,0.08);

    flex: 1 1 calc(25% - 22px);     /* 4 per row */
    max-width: calc(25% - 22px);
    min-height: 160px;

    box-sizing: border-box;
}

.kpi-title {
    color: #d3d6da;
    font-size: 16px;
    opacity: 0.9;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.kpi-value {
    font-weight: 800;
    font-size: 42px;
    color: #ffffff;
    margin-bottom: 6px;
    line-height: 1.1;
}

.kpi-sub {
    color: #b8c0cc;
    font-size: 15px;
    margin-top: 8px;
}

/* Accent colors */
.accent-1 { color: #FFB86B; }
.accent-2 { color: #7BE495; }
.accent-3 { color: #6EC1FF; }
.accent-4 { color: #D39BFF; }
.accent-5 { color: #FFD39B; }
.accent-6 { color: #8EF0C2; }
.accent-7 { color: #9FB3FF; }
.accent-8 { color: #C9A1FF; }

/* Responsive layout */
@media (max-width: 1100px) {
  .kpi-card {
    flex: 1 1 calc(50% - 22px);
    max-width: calc(50% - 22px);
  }
}

@media (max-width: 600px) {
  .kpi-card {
    flex: 1 1 100%;
    max-width: 100%;
  }
}

</style>
"""
st.markdown(css_kpis, unsafe_allow_html=True)

# ---------------- KPI Calculations ----------------

price_col = 'Price_in_Lakhs'
psqft_col = 'Price_per_SqFt'
size_col = 'Size_in_SqFt'
bhk_col = 'BHK'
city_col = 'City'
loc_col = 'Locality'
age_col = 'Age_of_Property'
furn_col = 'Furnished_Status'

def safe_mean(col):
    return float(dff[col].mean()) if col in dff.columns else 0.0

avg_price = int(safe_mean(price_col))
avg_psqft = round(safe_mean(psqft_col), 2)
avg_size = int(safe_mean(size_col))

mode_bhk = dff[bhk_col].mode().iloc[0] if bhk_col in dff.columns else "N/A"
total_cities = dff[city_col].nunique() if city_col in dff.columns else 0
total_localities = dff[loc_col].nunique() if loc_col in dff.columns else 0

avg_age = round(safe_mean(age_col), 1)
pct_furn = round(100 * dff[furn_col].fillna('Unk').eq('Furnished').mean(), 1) if furn_col in dff.columns else 0

# ---------------- KPI HTML ----------------
kpi_html = f"""
<div class="kpi-row">

  <div class="kpi-card">
    <div class="kpi-title">Avg Housing Price</div>
    <div class="kpi-value accent-1">{avg_price:,} Lakh</div>
  </div>

  <div class="kpi-card">
    <div class="kpi-title">Avg Price per Sqft</div>
    <div class="kpi-value accent-2">{avg_psqft}</div>
  </div>

  <div class="kpi-card">
    <div class="kpi-title">Avg Property Size</div>
    <div class="kpi-value accent-3">{avg_size} sqft</div>
  </div>

  <div class="kpi-card">
    <div class="kpi-title">Most Common BHK</div>
    <div class="kpi-value accent-4">{mode_bhk}</div>
  </div>

  <div class="kpi-card">
    <div class="kpi-title">Total Cities</div>
    <div class="kpi-value accent-5">{total_cities}</div>
  </div>

  <div class="kpi-card">
    <div class="kpi-title">Total Localities</div>
    <div class="kpi-value accent-6">{total_localities}</div>
  </div>

  <div class="kpi-card">
    <div class="kpi-title">Avg House Age</div>
    <div class="kpi-value accent-7">{avg_age} yrs</div>
  </div>

  <div class="kpi-card">
    <div class="kpi-title">% Furnished Homes</div>
    <div class="kpi-value accent-8">{pct_furn}%</div>
  </div>

</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)
