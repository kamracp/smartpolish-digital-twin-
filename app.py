import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")

# ------------------ CLEAN UI ------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------ LOGIN ------------------
st.title("🔐 SmartPolish Login")

password = st.text_input("Enter Password", type="password")

if password != "kamra123":
    st.warning("Please enter correct password to continue")
    st.stop()

# ------------------ TITLE ------------------
st.title("💎 SmartPolish AI - Digital Twin System")

# ------------------ SIDEBAR ------------------
st.sidebar.title("🎛 Process Control")

tile_area = st.sidebar.slider("Tile Size (m²)", 0.5, 3.0, 1.0, step=0.1)
surface = st.sidebar.radio("Surface", ["DG", "GVT"])
pressure = st.sidebar.slider("Pressure (bar)", 2.0, 6.0, 4.0)

# ------------------ SIZE LOGIC ------------------
if tile_area < 0.9:
    size = "600x1200"
    base_speed = 16.0
    removal = 22
elif tile_area < 1.6:
    size = "800x1600"
    base_speed = 11.0
    removal = 22
elif tile_area < 2.2:
    size = "1200x1200"
    base_speed = 8.0
    removal = 20
else:
    size = "1200x2400"
    base_speed = 8.0
    removal = 26

production = 7500

# ------------------ SPEED ------------------
speed = st.sidebar.slider(
    "Line Speed (m/min)",
    float(base_speed * 0.7),
    float(base_speed * 1.3),
    float(base_speed),
    step=0.1
)

st.sidebar.info(f"""
Detected Size: {size}  
Base Speed: {base_speed}  
Material Removal: {removal} mm
""")

# ------------------ DATA MODEL ------------------
np.random.seed(42)

base_load = 30 + removal
speed_factor = base_speed / speed
surface_factor = 1.2 if surface == "DG" else 1.0
pressure_factor = pressure / 4

profile = np.linspace(1.3, 0.7, 24)

amps = base_load * speed_factor * surface_factor * pressure_factor * profile
amps += np.random.normal(0, 2, 24)
amps = np.clip(amps, 20, 70)

# ------------------ KPI ------------------
total_kw = np.sum(amps) * 1.1
energy = (total_kw * 24) / production

# ------------------ KPI DISPLAY ------------------
st.markdown("## 📊 Live KPI")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Power (kW)", round(total_kw, 0))
c2.metric("Energy/m²", round(energy, 2))
c3.metric("Speed", round(speed, 1))
c4.metric("Pressure", pressure)

# ------------------ LOAD GRAPH ------------------
st.markdown("## ⚙️ Head Load Profile")

df = pd.DataFrame({
    "Head": range(1, 25),
    "Amps": amps
})

st.bar_chart(df.set_index("Head"))

# ------------------ SMART INSIGHTS ------------------
st.markdown("## 🚨 Smart Insights")

avg_amp = np.mean(amps)
insights = []

for i, val in enumerate(amps):
    if val < avg_amp * 0.75:
        insights.append(f"Head {i+1}: Abrasive worn")
    elif val > avg_amp * 1.3:
        insights.append(f"Head {i+1}: Overload")

if speed > base_speed * 1.2:
    insights.append("High speed → poor polishing quality")

if speed < base_speed * 0.8:
    insights.append("Low speed → high energy")

if pressure < 3.5:
    insights.append("Low pressure → poor finish")

if pressure > 5:
    insights.append("High pressure → abrasive wear")

if energy > 1.2:
    loss = (energy - 1.2) * production * 8.5
    insights.append(f"Energy loss approx ₹{int(loss)}/day")

if not insights:
    st.success("System Optimized")
else:
    for i in insights[:6]:
        st.warning(i)

# ------------------ HEAD HEALTH BULLET UI ------------------
st.markdown("## 🎯 Head-wise Abrasive Health")

cols = st.columns(6)

for i, val in enumerate(amps):

    health = (val / avg_amp) * 100

    if health < 70:
        color = "🔴"
        status = "Worn Out"
    elif health < 90:
        color = "🟡"
        status = "Weak"
    else:
        color = "🟢"
        status = "Healthy"

    cols[i % 6].markdown(f"""
    {color}  
    **Head {i+1}**  
    {status}
    """)

# ------------------ MACHINE SCORE ------------------
st.markdown("## 🏥 Machine Score")

score = 100 - len(insights) * 5
score = max(60, min(100, score))

st.progress(score)
st.write(f"Machine Score: {score}%")
