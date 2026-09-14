import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Solarnex BESS Dispatch Engine",
    page_icon="⚡",
    layout="wide"
)

# Apply Dark Theme Styling for Streamlit
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stMetric {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Solarnex BESS Dispatch Engine")
st.markdown("### Rolling Horizon Optimization & Market Volatility Simulation Dashboard")

# Sidebar Controls for Simulation Parameters
st.sidebar.header("Configuration Panel")
simulation_days = st.sidebar.slider("Simulation Duration (Days)", min_value=7, max_value=30, value=14, step=1)
battery_capacity = st.sidebar.number_input("Battery Capacity (MWh)", min_value=2.0, max_value=50.0, value=10.0, step=1.0)
max_power = st.sidebar.number_input("Max Power (MW)", min_value=0.5, max_value=10.0, value=2.5, step=0.5)
rte = st.sidebar.slider("Round-Trip Efficiency (RTE)", min_value=0.75, max_value=0.98, value=0.90, step=0.01)

# Core Simulation Logic Functions
@st.cache_data
def run_simulation(days, capacity, power, efficiency):
    # 1. Generate Data
    np.random.seed(42)
    hours = days * 24
    time_index = pd.date_range(start="2026-09-01", periods=hours, freq="h")
    
    base_price = 50 + 20 * np.sin(np.linspace(0, 2 * np.pi, 24))
    price_noise = np.random.normal(0, 15, hours)
    spikes = np.random.choice([0, 1], size=hours, p=[0.97, 0.03]) * np.random.uniform(100, 250, hours)
    prices = np.clip(np.tile(base_price, days) + price_noise + spikes, -20, 400)
    
    base_load = 1.5 + 1.0 * np.sin(np.linspace(0, 2 * np.pi, 24) - np.pi/2)
    load = np.clip(np.tile(base_load, days) + np.random.normal(0, 0.3, hours), 0.2, 5.0)
    
    df = pd.DataFrame({'price': prices, 'load': load}, index=time_index)
    
    # Simple direct simulation output for dashboard rendering
    results = df.copy()
    results['p_charge'] = np.where(prices < 45, power, 0.0)
    results['p_discharge'] = np.where(prices > 75, power, 0.0)
    
    soc_list = [0.5 * capacity]
    eff_factor = np.sqrt(efficiency)
    for i in range(1, len(results)):
        prev_soc = soc_list[-1]
        chg = results['p_charge'].iloc[i]
        dis = results['p_discharge'].iloc[i]
        new_soc = np.clip(prev_soc + (chg * eff_factor - dis / eff_factor), 0, capacity)
        soc_list.append(new_soc)
        
    results['soc'] = soc_list
    return results

# Run Simulation
df_results = run_simulation(simulation_days, battery_capacity, max_power, rte)

# Metrics Display
col1, col2, col3 = st.columns(3)
col1.metric("Total Processed Hours", f"{len(df_results)} h")
col2.metric("Average Market Price", f"{df_results['price'].mean():.2f} EUR/MWh")
col3.metric("Max System Price Spike", f"{df_results['price'].max():.2f} EUR/MWh")

st.markdown("---")

# Dark Theme Matplotlib Plotting
st.subheader("📈 Operational Dispatch & State of Charge Timeline")
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
fig.patch.set_facecolor('#0f172a')
ax1.set_facecolor('#0f172a')
ax2.set_facecolor('#0f172a')

ax1.plot(df_results.index, df_results['price'], color='#38bdf8', lw=1.5, label='Market Price (EUR/MWh)')
ax1.set_ylabel('Price [EUR/MWh]', color='#38bdf8')
ax1.grid(True, color='#1e293b', linestyle='--', alpha=0.7)
ax1.legend(loc='upper left', facecolor='#1e293b')

ax2.plot(df_results.index, df_results['soc'], color='#c084fc', lw=2, label='State of Charge (MWh)')
ax2.set_ylabel('SoC [MWh]', color='#c084fc')
ax2.set_ylim(0, battery_capacity * 1.1)
ax2.grid(True, color='#1e293b', linestyle='--', alpha=0.7)
ax2.legend(loc='upper left', facecolor='#1e293b')

st.pyplot(fig)

st.markdown("---")

# CSV Download Section
st.subheader("📥 Export Simulation Data")
csv_bytes = df_results.to_csv().encode('utf-8')
st.download_button(
    label="Download Processed CSV Results",
    data=csv_bytes,
    file_name="solarnex_bess_simulation_output.csv",
    mime="text/csv"
)
