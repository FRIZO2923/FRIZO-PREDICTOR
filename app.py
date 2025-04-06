import streamlit as st
import time
import matplotlib.pyplot as plt
from collections import Counter

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

# Prediction logic placeholder
def predict_next_pattern(history):
    # Look at last 5 patterns
    recent = history[-5:]
    # Count what came after similar patterns in past
    pattern_counts = {"Big": 0, "Small": 0}
    for i in range(len(history
