import streamlit as st
import datetime
import pytz
import matplotlib.pyplot as plt
import time

# Set Streamlit page config
st.set_page_config(page_title="Frizo Predictor", layout="centered")
st.title("🎯 Frizo Predictor")
st.markdown("### 👇 Enter 50 rounds of results to unlock Prediction Mode")

# Time config (India Standard Time)
ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.datetime.now(ist)
seconds = current_time.second
remaining = 60 - seconds

# --- Initialize session state ---
if "history" not in st.session_state:
    st.session_state.history = []
if "current_period" not in st.session_state:
    st.session_state.current_period = None
if "pending_result" not in st.session_state:
    st.session_state.pending_result = None
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None
if "prediction_stats" not in st.session_state:
    st.session_state.prediction_stats = {"correct": 0, "total": 0}
if "wrong_streak" not in st.session_state:
    st.session_state.wrong_streak = 0

# --- Period Entry ---
with st.expander("🔢 Enter Last 3 Digits of Period Number (e.g. 101)"):
    last_3 = st.text_input("Enter Last 3 Digits", placeholder="e.g. 101")
    if last_3.isdigit() and 0 <= int(last_3) <= 999:
        st.session_state.current_period = int(last_3)

if st.session_state.current_period is not None:
    st.markdown(f"### 📌 Starting From Period: `{st.session_state.current_period}` (descending)")

# --- Time Display ---
st.subheader(f"🕒 India Time: `{current_time.strftime('%H:%M:%S')}`")
st.subheader(f"⏳ Next Round In: `{remaining}` seconds")

# --- Prediction Logic ---
def predict_next_pattern(history):
    values = [h["result"] for h in history]
    recent = values[-5:]
    pattern_counts = {"Big": 0, "Small": 0}
    for i in range(len(values) - 5):
        if values[i:i+5] == recent:
            next_value = values[i+5]
            pattern_counts[next_value] += 1
    if sum(pattern_counts.values()) == 0:
        return None, 0
    prediction = max(pattern_counts, key=pattern_counts.get)
    confidence = int((pattern_counts[prediction] / sum(pattern_counts.values())) * 100)
    return prediction, confidence

# --- Buttons ---
col1, col2, col3 = st.columns([1, 1, 2])

def set_pending_result(result):
    if st.session_state.current_period is not None:
        st.session_state.pending_result = {
            "period": st.session_state.current_period,
            "result": result
        }
        st.session_state.current_period -= 1
        st.rerun()

with col1:
    if st.button("🔴 BIG"):
        set_pending_result("Big")
with col2:
    if st.button("🔵 SMALL"):
        set_pending_result("Small")
with col3:
    if st.button("🧹 Reset History"):
