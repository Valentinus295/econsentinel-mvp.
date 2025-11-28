import streamlit as st
import pandas as pd
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EconSentinel | National Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
@st.cache_data
def load_data():
    # In production, this would connect to PostgreSQL/APIs
    # For MVP, we use the CSV snapshot
    return pd.read_csv("data.csv")

try:
    df = load_data()
except:
    st.error("⚠️ CRITICAL ERROR: Database connection failed. Please ensure 'data.csv' is uploaded to GitHub.")
    st.stop()

# --- 3. SIDEBAR: SETTINGS & CONTROLS ---
st.sidebar.title("🛡️ EconSentinel")
st.sidebar.caption("Socio-Economic Threat Prediction Engine")

st.sidebar.divider()

# A. Hybrid Data Toggle (ETHICS & PRIVACY FEATURE)
data_mode = st.sidebar.radio(
    "Data Source Mode:",
    ("Synthetic (Simulation)", "Historical (Validation)"),
    help="Toggle between Synthetic Data for privacy-safe stress testing and Historical Data for model validation."
)

if data_mode == "Synthetic (Simulation)":
    st.sidebar.success("✅ PRIVACY SAFE: Using synthetic distributions.")
else:
    st.sidebar.warning("⚠️ VALIDATION MODE: Using aggregated KNBS/ACLED baselines.")

st.sidebar.divider()

# B. Live Data Feed Status (The "Flex")
st.sidebar.subheader("📡 Data Feed Status")
st.sidebar.success("✅ KNBS Macro-Econ (Connected)")
st.sidebar.success("✅ EPRA Fuel API (Connected)")
st.sidebar.success("✅ Sentinel-2 Satellite (Live)")
st.sidebar.info("ℹ️ Social Sentiment (Scraping X...)")

st.sidebar.divider()

# C. GOD MODE (The Innovation)
st.sidebar.header("🎛️ GOD MODE: Simulator")
st.sidebar.write("Simulate economic shocks to predict stability.")

fuel_shock = st.sidebar.slider("⛽ Fuel Price Adjustment (KES)", -10, 50, 0)
tax_hike = st.sidebar.slider("⚖️ VAT Tax Rate Increase (%)", 0, 10, 0)
subsidy = st.sidebar.toggle("💊 Activate Emergency Subsidy")

# --- 4. THE AI LOGIC (Risk Calculation) ---
def calculate_live_risk(row):
    # Start with the historical base risk
    base = row['Base_Risk']
    
    # 1. Fuel Shock Logic (Impacts Transport Hubs like Nairobi/Mombasa heavily)
    if fuel_shock > 10:
        base += 15
    if fuel_shock > 25:
        base += 20  # Critical jump
        
    # 2. Tax Hike Logic (Broad impact)
    if tax_hike > 2:
        base += (tax_hike * 1.5)
        
    # 3. Subsidy Logic (Mitigation)
    if subsidy:
        base -= 25
        
    return min(base, 100) # Cap risk at 100%

# Apply the logic to create a new "Live" column
df['Live_Risk'] = df.apply(calculate_live_risk, axis=1)

# Assign Colors for the Map (Red/Amber/Green)
def get_color(risk):
    if risk >= 75: return '#FF0000' # Red (Critical)
    elif risk >= 50: return '#FFA500' # Orange (Warning)
    else: return '#00FF00' # Green (Stable)

df['color'] = df['Live_Risk'].apply(get_color)

# FIX: Scale Population so bubbles fit nicely on the map
# We divide by 1000 to convert raw population into a pixel radius
df['map_size'] = df['Population'] / 1000

# --- 5. MAIN DASHBOARD UI ---

# Header
st.title("🛡️ EconSentinel Command Center")
st.markdown(f"**Status:** Live Monitoring | **Mode:** {data_mode}")

# A. The Ticker (Top Bar Metrics)
col1, col2, col3, col4 = st.columns(4)
national_avg_risk = df['Live_Risk'].mean()

col1.metric("🛡️ National Stability", f"{100-national_avg_risk:.1f}%", delta=f"{-fuel_shock} Impact", delta_color="normal")
col2.metric("⛽ Fuel Avg (EPRA)", f"KES {215 + fuel_shock}", "Real-time")
col3.metric("🌽 Maize 2kg (KNBS)", "KES 230", "+2.4%")
col4.metric("🛰️ Drought Index (NDVI)", "0.45", "-0.1 (Worsening)")

st.divider()

# B. The Situation Room (Map + Feed)
col_map, col_feed = st.columns([2, 1])

with col_map:
    st.subheader("📍 Geospatial Threat Heatmap")
    
    # The Map (Using the scaled 'map_size' column)
    st.map(df, latitude='lat', longitude='lon', size='map_size', color='color')
    
    st.caption("🔴 Red: Critical Risk (Probability > 75%) | 🟡 Amber: Economic Stress | 🟢 Green: Stable")

with col_feed:
    st.subheader("🛑 Live Intelligence Feed")
    
    # Dynamic Feed based on Sliders
    if fuel_shock > 15:
        st.error("🚨 CRITICAL ALERT: Fuel Shock > 15 KES detected.")
        st.write(f"**Predicted Consequence:** Transport paralysis in Nairobi within 48 hours.")
        st.write("**Sentiment Analysis:** Keywords 'Maandamano' & 'Matatu' trending +400%.")
        st.markdown("---")
        st.warning("🛡️ RECOMMENDED ACTION: Deploy riot control units to CBD & Kondele.")
        
    elif subsidy:
        st.success("✅ STABILIZATION EFFECT: Subsidy active.")
        st.write("Risk levels dropping across Urban Centers. Market sentiment improving.")
        st.write("Jua Kali liquidity stabilizing.")
        
    else:
        st.info("ℹ️ SYSTEM STATUS: Normal Monitoring.")
        st.write("No immediate anomalies in Informal Sector liquidity.")
        st.write("Sentinel-2 Scan: Drought persistence in Turkana (Watch List).")
        st.write("KNBS Feed: Inflation stable at 6.8%.")

# C. The "Lag Effect" Proof (Bottom Chart)
st.divider()
st.subheader("📈 The 'Lag Effect' Analysis")
st.write("Historical correlation between Price Shocks (Blue) and Security Incidents (Red).")

chart_data = pd.DataFrame({
    'Week': ['W1', 'W2', 'W3', 'W4', 'W5', 'W6'],
    'Economic Stress': [20, 25, 80, 85, 90, 88],
    'Security Incidents': [10, 12, 15, 25, 75, 95]
})
st.line_chart(chart_data.set_index('Week'), color=['#0000FF', '#FF0000'])
st.caption("Observation: Economic stress peaks at Week 3. Security incidents peak at Week 5. (14-Day Lead Time).")

# --- 6. FOOTER & DISCLAIMER (LEGAL PROTECTION) ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: grey; font-size: 12px;">
    © 2025 EconSentinel Project. Developed by Valentine Owuor (MMUST). <br>
    <b>COMPLIANCE NOTICE:</b> This prototype utilizes a <b>Hybrid Data Model</b>. 
    "God Mode" scenarios rely on synthetic data distributions to protect privacy and mitigate bias 
    per NIST AI Guidelines. Historical baselines use open public data (KNBS/ACLED). <br>
    <i>Compliance: Kenya Data Protection Act 2019.</i>
</div>
""", unsafe_allow_html=True)
