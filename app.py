import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pytz import timezone
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Frizo Predictor", layout="centered")

# Auto refresh every 1 second
st_autorefresh(interval=1000, key="auto_refresh")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "latest_period" not in st.session_state:
    st.session_state.latest_period = None
if "prediction_feedback" not in st.session_state:
    st.session_state.prediction_feedback = []

st.title("🎯 Frizo Predictor")

# Get current IST time
ist = timezone('Asia/Kolkata')
current_time = datetime.now(ist)
seconds = current_time.second

# Input for last 3 digits of current period number
period_input = st.text_input("🔢 Enter last 3 digits of the current period number (e.g., 101 from 56231235101):", max_chars=3)

if period_input.isdigit() and len(period_input) == 3:
    st.session_state.latest_period = int(period_input)
    st.experimental_rerun()

if st.session_state.latest_period is None:
    st.warning("⚠️ Please enter the last 3 digits of the period number to start.")
    st.stop()

# Buttons to add outcomes
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🟢 Big"):
        period = st.session_state.latest_period - len(st.session_state.history)
        st.session_state.history.append((period, "Big"))
        st.experimental_rerun()
with col2:
    if st.button("🔴 Small"):
        period = st.session_state.latest_period - len(st.session_state.history)
        st.session_state.history.append((period, "Small"))
        st.experimental_rerun()
with col3:
    if st.button("🧹 Reset History"):
        st.session_state.history.clear()
        st.session_state.prediction_feedback.clear()
        st.experimental_rerun()

# Display timer
st.markdown(f"⏳ **Next Round In:** `{60 - seconds}` seconds")

# Prediction
if len(st.session_state.history) >= 50:
    last_50 = [entry[1] for entry in st.session_state.history[-50:]]
    big_count = last_50.count("Big")
    small_count = last_50.count("Small")

    prediction = "Big" if big_count > small_count else "Small"
    st.markdown(f"📈 **Predicted Next Outcome:** `{prediction}`")

    # Feedback buttons
    col4, col5 = st.columns(2)
    with col4:
        if st.button("✅ Prediction Correct"):
            st.session_state.prediction_feedback.append("Correct")
            st.experimental_rerun()
    with col5:
        if st.button("❌ Prediction Wrong"):
            st.session_state.prediction_feedback.append("Wrong")
            st.experimental_rerun()

    # Accuracy stats
    correct = st.session_state.prediction_feedback.count("Correct")
    total = len(st.session_state.prediction_feedback)
    if total > 0:
        accuracy = (correct / total) * 100
        st.markdown(f"🎯 **Prediction Accuracy:** `{accuracy:.2f}%` ({correct}/{total})")

# Display history
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history, columns=["Period", "Result"])
    df_sorted = df.sort_values(by="Period", ascending=False).reset_index(drop=True)
    st.subheader("📊 History Data")
    st.dataframe(df_sorted, use_container_width=True)
else:
    st.info("📭 No history data available.")
