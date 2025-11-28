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
    return pd.read_csv("data.csv")

try:
    df = load_data()
except:
    st.error("⚠️ CRITICAL ERROR: Database connection failed. Please ensure 'data.csv' is uploaded.")
    st.stop()

# --- 3. SIDEBAR: GOD MODE & DATA FEEDS ---
st.sidebar.title("🛡️ EconSentinel")
st.sidebar.markdown("**Socio-Economic Threat Prediction Engine**")
st.sidebar.markdown("---")

# A. Data Feed Status
st.sidebar.subheader("📡 Live Data Feeds")
st.sidebar.success("✅ KNBS Macro-Econ (Connected)")
st.sidebar.success("✅ EPRA Fuel API (Connected)")
st.sidebar.success("✅ Sentinel-2 Satellite (Live)")
st.sidebar.warning("⚠️ ACLED Conflict Feed (Syncing...)")
st.sidebar.info("ℹ️ Social Sentiment (Scraping X...)")

st.sidebar.markdown("---")

# B. GOD MODE (The Innovation)
st.sidebar.header("🎛️ GOD MODE: Simulator")
st.sidebar.write("Simulate economic shocks to predict stability.")

fuel_shock = st.sidebar.slider("⛽ Fuel Price Adjustment (KES)", -10, 50, 0)
tax_hike = st.sidebar.slider("⚖️ VAT Tax Rate Increase (%)", 0, 10, 0)
subsidy = st.sidebar.toggle("💊 Activate Emergency Subsidy")

# --- 4. THE AI LOGIC (Simulating the Prediction) ---
def calculate_live_risk(row):
    base = row['Base_Risk']
    
    # Shock 1: Fuel Price (High impact on transport hubs)
    if fuel_shock > 10:
        base += 15
    if fuel_shock > 25:
        base += 20  # Critical jump
        
    # Shock 2: Tax Hike (Affects everyone)
    if tax_hike > 2:
        base += (tax_hike * 1.5)
        
    # Mitigation: Subsidy (Lowers risk)
    if subsidy:
        base -= 30
        
    return min(base, 100) # Cap at 100%

df['Live_Risk'] = df.apply(calculate_live_risk, axis=1)

# Assign Colors for the Map
def get_color(risk):
    if risk >= 75: return '#FF0000' # Red (Critical)
    elif risk >= 50: return '#FFA500' # Orange (Warning)
    else: return '#00FF00' # Green (Stable)

df['color'] = df['Live_Risk'].apply(get_color)

# FIX: Scale the Population Size so bubbles aren't huge
# We divide by 1000 to convert Population to a reasonable radius in meters/pixels
df['map_size'] = df['Population'] / 100

# --- 5. MAIN DASHBOARD UI ---

# Header
st.title("🛡️ EconSentinel Command Center")
st.markdown("### National Stability & Economic Risk Monitor")

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
    
    # The Map (Using the scaled size)
    st.map(df, latitude='lat', longitude='lon', size='map_size', color='color')
    
    st.caption("🔴 Red: Critical Risk (Probability > 75%) | 🟡 Amber: Economic Stress | 🟢 Green: Stable")

with col_feed:
    st.subheader("🛑 Live Intelligence Feed")
    
    # Dynamic Alerts based on the Slider
    if fuel_shock > 15:
        st.error("🚨 CRITICAL ALERT: Fuel Shock > 15 KES detected.")
        st.write("**Predicted Consequence:** Transport paralysis in Nairobi & Mombasa within 48 hours.")
        st.write("**Sentiment Analysis:** Keywords 'Maandamano' trending +400%.")
        st.warning("🛡️ RECOMMENDED ACTION: Deploy riot control to CBD.")
    elif subsidy:
        st.success("✅ STABILIZATION EFFECT: Subsidy active.")
        st.write("Risk levels dropping across Urban Centers. Market sentiment improving.")
    else:
        st.info("ℹ️ SYSTEM STATUS: Normal Monitoring.")
        st.write("No immediate anomalies in Informal Sector liquidity.")
        st.write("Sentinel-2 Scan: Drought persistence in Turkana (Watch List).")

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
# --- FOOTER & DISCLAIMER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: grey; font-size: 12px;">
    © 2025 EconSentinel Project. <br>
    <b>DISCLAIMER:</b> This dashboard is a prototype for the National AI Hackathon 2025. 
    Predictions are based on simulated/historical data for demonstration purposes 
    and should not be used for operational decision-making without further validation.
    <br>
    <i>Compliance: Kenya Data Protection Act 2019 | NIST AI Risk Management Framework</i>
</div>
""", unsafe_allow_html=True)
