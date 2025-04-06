import streamlit as st
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="Frizo Predictor", layout="centered")

st.title("🎯 Frizo Predictor")
st.markdown("### 👇 Enter 50 rounds of results to unlock Prediction Mode")

# Init session variables
if "history" not in st.session_state:
    st.session_state.history = []
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

TIMER_DURATION = 60
elapsed = time.time() - st.session_state.start_time
remaining = max(0, TIMER_DURATION - int(elapsed))

st.subheader(f"⏳ Next Round In: `{remaining}` seconds")

# Prediction logic
def predict_next_pattern(history):
    recent = history[-5:]
    pattern_counts = {"Big": 0, "Small": 0}
    for i in range(len(history) - 5):
        if history[i:i+5] == recent:
            next_value = history[i+5]
            pattern_counts[next_value] += 1
    if sum(pattern_counts.values()) == 0:
        return "❓ Not enough pattern matches", 0
    prediction = max(pattern_counts, key=pattern_counts.get)
    confidence = int((pattern_counts[prediction] / sum(pattern_counts.values())) * 100)
    return prediction, confidence

# Add Big / Small buttons
if remaining == 0:
    st.success("🚨 NEW ROUND READY! Add result below:")
