# main.py

import streamlit as st # Front-end framework
import pandas as pd
import time # To create delays between simulation frames
import pydeck as pdk # WebGL-powered mapping library

from scripts.plot_pydeck import plot_aircraft_pydeck
from scripts.generate_insights import generate_insights_from_csv

# Page setup
st.set_page_config(page_title="Airfield Insights", layout="wide")
st.markdown("# 🛫 Aircraft Simulation – Pydeck Map")

# Load and parse data
df = pd.read_csv("data/simulated_aircraft_movements.csv")
df["Time"] = pd.to_datetime(df["Time"], format="%H:%M")
time_steps = sorted(df["Time"].dt.strftime("%H:%M").unique().tolist())

# Session state
if "frame_index" not in st.session_state:
    st.session_state.frame_index = 0 # Tracks time step
if "running" not in st.session_state:
    st.session_state.running = False
if "last_run" not in st.session_state:
    st.session_state.last_run = time.time() # Time step of last frame advance

# Controls
if st.button("▶️ Start"):
    st.session_state.running = True
if st.button("⏹ Stop"):
    st.session_state.running = False

# Sim speed slider
speed = st.slider("⏱ Simulation speed (seconds per frame)", 0.5, 2.0, 2.0, 0.1)

# Get current frame
current_time = time_steps[st.session_state.frame_index] # Get current time
st.markdown(f"**🕒 Time:** `{current_time}`")
current_df = df[df["Time"].dt.strftime("%H:%M") == current_time] # Filter DF to show aircraft at time

# Show map 
deck_map = plot_aircraft_pydeck(current_df, df, pd.to_datetime(current_time, format="%H:%M"))
st.pydeck_chart(deck_map)

# Show data
st.table(current_df[["Flight", "Status", "Gate"]])

# Simulation loop
if st.session_state.running:
    now = time.time()
    if now - st.session_state.last_run >= speed:
        st.session_state.frame_index = (st.session_state.frame_index + 1) % len(time_steps)
        st.session_state.last_run = now
        st.rerun()
    else:
        # Wait and rerun to check again
        time.sleep(0.1)
        st.rerun()


# Generate analysis using csv data and OpenAI
if st.button("🧠 Generate AI Insights"):
    with st.spinner("Generating AI summary..."):
        summary = generate_insights_from_csv(df)
        st.markdown("### 📋 AI Summary")
        st.success(summary)