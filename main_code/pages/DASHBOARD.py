import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Plotting Charts", page_icon="📈", layout="wide")


# ---------------- Data loader
@st.cache_data
def load_dataset(path):
    return pd.read_csv(path)

path = './dataset/cleaned_housing.csv'
df = load_dataset(path)
dff = df.copy()

# ---------------- Sidebar filters
st.sidebar.markdown("### Filters (slicers)")

# map column names to variables (your dataset column names)
park_avail, amenity_lvl, prop_age, price_col, size, psqft_col, loc_col, city_col, property_col, bhk_col, furn_col = [
    'Parking_Space', 'Amenities_level', 'Age_of_Property', 'Price_in_Lakhs', 'Size_in_SqFt',
    'Price_per_SqFt', 'Locality', 'City', 'Property_Type', 'BHK', 'Furnished_Status'
]

city_filter = st.sidebar.multiselect(
    "City",
    options=sorted(dff[city_col].dropna().unique()) if city_col in dff.columns else [],
    default=[]
)
ptype_filter = st.sidebar.multiselect(
    "Property Type",
    options=sorted(dff[property_col].dropna().unique()) if property_col in dff.columns else [],
    default=[]
)
bhk_filter = st.sidebar.multiselect(
    "BHK",
    options=sorted(dff[bhk_col].dropna().unique(), key=lambda x: float(x) if str(x).replace('.','',1).isdigit() else x) if bhk_col in dff.columns else [],
    default=[]
)
furn_filter = st.sidebar.multiselect(
    "Furnishing",
    options=sorted(dff[furn_col].dropna().unique()) if furn_col in dff.columns else [],
    default=[]
)

# Range slider for property age (safe cast to int)
if prop_age in dff.columns:
    age_range = st.sidebar.slider(
        "Property Age Range",
        min_value=int(dff[prop_age].min()),
        max_value=int(dff[prop_age].max()),
        value=(int(dff[prop_age].min()), int(dff[prop_age].max()))
    )
else:
    age_range = None

# apply filters
dfc = dff.copy()
if city_filter and city_col in dfc.columns:
    dfc = dfc[dfc[city_col].isin(city_filter)]
if ptype_filter and property_col in dfc.columns:
    dfc = dfc[dfc[property_col].isin(ptype_filter)]
if bhk_filter and bhk_col in dfc.columns:
    dfc = dfc[dfc[bhk_col].isin(bhk_filter)]
if furn_filter and furn_col in dfc.columns:
    dfc = dfc[dfc[furn_col].isin(furn_filter)]
if age_range and prop_age in dfc.columns:
    dfc = dfc[dfc[prop_age].between(age_range[0], age_range[1])]

# helper safe functions
def top_n_by(col, n=10):
    if col in dfc.columns and price_col in dfc.columns:
        return dfc.groupby(col, as_index=False)[price_col].mean().sort_values(price_col, ascending=False).head(n)
    return pd.DataFrame()

# ---------- Charts

# Row 1: Avg Price by City | Avg Price per Sqft by City
c1, c2 = st.columns([1, 1], gap="large")
with c1:
    st.subheader("Avg Price by City (top 20)")
    if city_col in dfc.columns and price_col in dfc.columns:
        agg = (dfc.groupby(city_col, as_index=False)[price_col]
               .mean().sort_values(price_col, ascending=False).head(20))
        fig = px.bar(
            agg, x=city_col, y=price_col, labels={price_col: "Avg Price"},
            color=price_col, color_continuous_scale=px.colors.sequential.Viridis
        )
        fig.update_layout(margin=dict(t=30,b=10), paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)', height=560)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("City or Price column missing")

with c2:
    st.subheader("Avg Price per Sqft by City (top 20)")
    if city_col in dfc.columns and psqft_col in dfc.columns:
        agg2 = (dfc.groupby(city_col, as_index=False)[psqft_col]
                .mean().sort_values(psqft_col, ascending=False).head(20))
        fig2 = px.bar(
            agg2, x=city_col, y=psqft_col, labels={psqft_col: "Avg Price/Sqft"},
            color=psqft_col, color_continuous_scale=px.colors.sequential.Plasma
        )
        fig2.update_layout(margin=dict(t=30,b=10), paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)', height=560)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("City or Price_per_Sqft column missing")

st.markdown("---")

# Row2: Price vs Size (scatter) | Price Distribution
c3, c4 = st.columns([1, 1], gap="large")
with c3:
    st.subheader("Price vs Property Size")
    if size in dfc.columns and price_col in dfc.columns:
        fig3 = px.scatter(
            dfc, x=size, y=price_col,
            # color=property_col if property_col in dfc.columns else None,
            size=psqft_col if psqft_col in dfc.columns else None,
            hover_data=[city_col, loc_col] if (city_col in dfc.columns and loc_col in dfc.columns) else None
        )
        fig3.update_layout(margin=dict(t=30,b=10), paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)', height=560)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Size or Price column missing")

with c4:
    st.subheader("Price Distribution")
    if price_col in dfc.columns:
        fig4 = px.histogram(dfc, x=price_col)
        fig4.update_layout(margin=dict(t=30,b=10), paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)', height=560)
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Price column missing")

st.markdown("---")

# Row 3: Price by Property Type (box) | Avg Price by BHK (bar)
c5, c6 = st.columns([1, 1], gap="large")
with c5:
    st.subheader("Price by Property Type")
    if property_col in dfc.columns and price_col in dfc.columns:
        fig5 = px.box(dfc, x=property_col, y=price_col, points='outliers')
        fig5.update_layout(margin=dict(t=30,b=10), paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)', height=560)
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("Property_Type or Price missing")

with c6:
    st.subheader("Avg Price by BHK")
    if bhk_col in dfc.columns and price_col in dfc.columns:
        agg_bhk = dfc.groupby(bhk_col, as_index=False)[price_col].mean().sort_values(price_col, ascending=False)
        fig6 = px.bar(agg_bhk, x=bhk_col, y=price_col)
        fig6.update_layout(margin=dict(t=30,b=10), paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)', height=560)
        st.plotly_chart(fig6, use_container_width=True)
    else:
        st.info("BHK or Price missing")

st.markdown("---")

# Row 4: Top 10 Expensive Localities | Top 10 Affordable Localities 
c7, c8 = st.columns([1, 1], gap="large")
with c7:
    st.subheader("Top 10 Most Expensive Localities (Avg Price)")
    if loc_col in dfc.columns and price_col in dfc.columns:
        top_local = dfc.groupby(loc_col, as_index=False)[price_col].mean().sort_values(price_col, ascending=False).head(10)
        fig7 = px.bar(top_local, x=loc_col, y=price_col, color=price_col, color_continuous_scale=px.colors.sequential.Viridis)
        fig7.update_layout(margin=dict(t=30,b=10), paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)', height=560)
        st.plotly_chart(fig7, use_container_width=True)
    else:
        st.info("Locality or Price missing")

with c8:
    st.subheader("Top 10 Most Affordable Localities (Avg Price)")
    if loc_col in dfc.columns and price_col in dfc.columns:
        low_local = dfc.groupby(loc_col, as_index=False)[price_col].mean().sort_values(price_col, ascending=True).head(10)
        fig8 = px.bar(low_local, x=loc_col, y=price_col, color=price_col, color_continuous_scale=px.colors.sequential.Viridis)
        fig8.update_layout(margin=dict(t=30,b=10), paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)', height=560)
        st.plotly_chart(fig8, use_container_width=True)
    else:
        st.info("Locality or Price missing")

st.markdown("---")

# ROW 5: Price by Furnishing Status | Price by Amenities Level 
c9, c10 = st.columns([1, 1], gap="large")
with c9:
    st.subheader("Price by Furnishing Status")
    if price_col in dfc.columns and furn_col in dfc.columns:
        furn_price = dfc.groupby(furn_col, as_index=False)[price_col].mean().sort_values(price_col, ascending=False)
        fig9 = px.bar(furn_price, x=furn_col, y=price_col, color=price_col, color_continuous_scale=px.colors.sequential.Viridis)
        fig9.update_layout(margin=dict(t=30,b=10), paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)', height=560)
        st.plotly_chart(fig9, use_container_width=True)
    else:
        st.info("Furnishing or Price missing")

with c10:
    st.subheader("Price by Amenities Level")
    if amenity_lvl in dfc.columns and price_col in dfc.columns:
        amenity = dfc.groupby(amenity_lvl, as_index=False)[price_col].mean().sort_values(price_col, ascending=True)
        fig10 = px.bar(amenity, x=amenity_lvl, y=price_col, color=price_col, color_continuous_scale=px.colors.sequential.Viridis)
        fig10.update_layout(margin=dict(t=30,b=10), paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)', height=560)
        st.plotly_chart(fig10, use_container_width=True)
    else:
        st.info("Amenities or Price missing")

st.markdown("---")

# ROW 6: Price by Parking Availability | Price by Property Age Group  
c11, c12 = st.columns([1, 1], gap="large")
with c11:
    st.subheader("Price by Parking Availability")
    if park_avail in dfc.columns and price_col in dfc.columns:
        park = dfc.groupby(park_avail, as_index=False)[price_col].mean().sort_values(price_col, ascending=False)
        fig11 = px.bar(park, x=park_avail, y=price_col, color=price_col, color_continuous_scale=px.colors.sequential.Viridis)
        fig11.update_layout(margin=dict(t=30,b=10), paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)', height=560)
        st.plotly_chart(fig11, use_container_width=True)
    else:
        st.info("Parking or Price missing")

with c12:
    st.subheader("Price by Property Age Group")
    if prop_age in dfc.columns and price_col in dfc.columns:
        AGE = dfc.groupby(prop_age, as_index=False)[price_col].mean().sort_values(by=[price_col, prop_age], ascending=[False, True]).head(10)
        fig12 = px.bar(AGE, x=prop_age, y=price_col, color=price_col, color_continuous_scale=px.colors.sequential.Viridis)
        fig12.update_layout(margin=dict(t=30,b=10), paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)', height=560)
        st.plotly_chart(fig12, use_container_width=True)
    else:
        st.info("Age or Price missing")
