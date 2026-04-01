import streamlit as st
import numpy as np
import pandas as pd

from engine import calculate
from data_source import generate_data
from alerts import generate_alerts
from config import PROCESS_DB

st.set_page_config(layout="wide")

# ---------------- LOGIN ----------------
password = st.sidebar.text_input("Enter Password", type="password")
if password != "kamra123":
    st.warning("Enter valid password")
    st.stop()

st.title("💎 SmartPolish AI - Digital Twin")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎛 Controls")

size = st.sidebar.selectbox("Tile Size", list(PROCESS_DB.keys()))
surface = st.sidebar.radio("Surface", ["DG", "GVT"])

base_speed = PROCESS_DB[size]["speed"]
production = PROCESS_DB[size]["production"]
removal = PROCESS_DB[size]["removal"]

speed = st.sidebar.slider("Speed", base_speed*0.7, base_speed*1.3, base_speed)
pressure = st.sidebar.slider("Pressure", 2.0, 6.0, 4.0)

# ---------------- DATA ----------------
amps = generate_data(base_speed, speed, removal, surface, pressure)

# ---------------- CALC ----------------
result = calculate(amps, production)

# ---------------- KPI ----------------
st.subheader("📊 Performance")

c1, c2, c3 = st.columns(3)
c1.metric("Power (kW)", round(result["power"], 0))
c2.metric("Energy/m²", round(result["energy"], 2))
c3.metric("Efficiency", round(result["efficiency"], 1))

# ---------------- GRAPH ----------------
df = pd.DataFrame({"Head": range(1,25), "Amps": amps})
st.bar_chart(df.set_index("Head"))

# ---------------- ALERTS ----------------
alerts = generate_alerts(amps, result, speed, base_speed, pressure)

st.subheader("🚨 Insights")
for a in alerts:
    st.warning(a)