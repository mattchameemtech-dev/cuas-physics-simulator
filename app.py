import streamlit as st
import numpy as np
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Kinetic C-UAS Physics Simulator",
    page_icon="🛡️",
    layout="wide"
)

# App Title & Header
st.title("🛡️ Kinetic C-UAS Ballistic Physics Simulator")
st.markdown("""
This interactive tool allows you to evaluate spatial hit probabilities and ballistic curves 
by dynamic variable manipulation. Adjust the inputs in the sidebar to see real-time updates.
""")

# --- SIDEBAR INPUTS ---
st.sidebar.header("🎯 Engagement Variables")

# Target Velocity (converting typical drone operational speeds)
target_speed_kmh = st.sidebar.slider(
    "Target Speed (km/h)", 
    min_value=5, 
    max_value=150, 
    value=70, 
    step=5,
    help="Speed of the incoming threat (e.g., FPV kamikaze quadcopter)."
)
target_speed_ms = target_speed_kmh / 3.6

# Projectile Mass Matrix Configuration
projectile_weight = st.sidebar.slider(
    "Projectile Weight (grams)", 
    min_value=0.1, 
    max_value=10.0, 
    value=0.5, 
    step=0.1,
    help="Mass profile of an individual sub-projectile round variant."
)

# Lead-Angle Tracking Error Bounds
tracking_error_mrad = st.sidebar.slider(
    "Angular Tracking Error (mrad)", 
    min_value=0.0, 
    max_value=15.0, 
    value=2.5, 
    step=0.1,
    help="Human or optical system angular lead tracking error bounds."
)

# Ammunition & Engagement Range Constraints
st.sidebar.header("⚙️ System Constraints")
projectile_count = st.sidebar.number_input("Projectile Count (Burst/Array)", min_value=1, max_value=24, value=8)
max_range = st.sidebar.slider("Maximum Evaluation Range (meters)", min_value=10, max_value=100, value=50, step=5)

# --- DUMMY PHYSICS SIMULATION ENGINE ---
# Replace this math block with your core kinetic/ballistic equations
def calculate_hit_probability(speed, weight, error, range_axis):
    # Dummy placeholder scaling curves capturing downrange decay impacted by target speed and tracking error
    decay_factor = 0.01 * (1.0 + (speed * 0.02) + (error * 0.15)) / (weight ** 0.2)
    pk_curve = np.exp(-decay_factor * range_axis) * 100
    # Cap limits realistically
    return np.clip(pk_curve, 0.0, 100.0)

# Generate Range Domain data points
ranges = np.linspace(5, max_range, 50)
pk_values = calculate_hit_probability(target_speed_ms, projectile_weight, tracking_error_mrad, ranges)

# Prepare DataFrame for rendering
chart_data = pd.DataFrame({
    'Distance (meters)': ranges,
    'Probability of Kill (Pk %)': pk_values
})

# --- MAIN DASHBOARD INTERFACE ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Active Configuration Metrics")
    
    # Clean Metric Matrix Output Displays
    st.metric(label="Target Speed", value=f"{target_speed_kmh} km/h", delta=f"{target_speed_ms:.2f} m/s")
    st.metric(label="Sub-Projectile Mass Profile", value=f"{projectile_weight} g")
    st.metric(label="System Angular Tracking Error", value=f"{tracking_error_mrad} mrad")
    st.metric(label="Total Volumetric Projectile Array", value=f"{projectile_count} rounds")

with col2:
    st.subheader("📈 Probability Curve Downrange")
    
    # Dynamic Line Chart Plotting
    st.line_chart(
        chart_data, 
        x='Distance (meters)', 
        y='Probability of Kill (Pk %)', 
        use_container_width=True
    )

# Summary Output Data Table Toggle
with st.expander("🔍 View Raw Parametric Simulation Data Matrix"):
    st.dataframe(chart_data.style.format({'Distance (meters)': '{:.1f}', 'Probability of Kill (Pk %)': '{:.2f}%'}), use_container_width=True)
