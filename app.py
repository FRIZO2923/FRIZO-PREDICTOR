import streamlit as st
import datetime
import pytz
import random

# Page setup
st.set_page_config(page_title="Frizo Predictor", layout="centered")

st.title("🎯 FRIZO PREDICTOR 😈")

# Indian time
ist = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
st.subheader(f"🕒 IST: {ist.strftime('%H:%M:%S')}")
st.subheader(f"⏳ Next Round In: {60 - ist.second} seconds")

# Session variables
if "history" not in st.session_state:
    st.session_state.history = []
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "total" not in st.session_state:
    st.session_state.total = 0

# Input result
col1, col2 = st.columns(2)
with col1:
    if st.button("🔴 BIG"):
        st.session_state.history.append("Big")
with col2:
    if st.button("🔵 SMALL"):
        st.session_state.history.append("Small")

# Prediction logic
if len(st.session_state.history) >= 5:
    last5 = st.session_state.history[-5:]
    pred = random.choice(["Big", "Small"])  # Placeholder logic
    st.session_state.last_prediction = pred
    st.success(f"🔮 Prediction: `{pred}`")

# Show history
if st.session_state.history:
    st.markdown("### 📚 History")
    for i, result in enumerate(reversed(st.session_state.history[-20:]), 1):
        st.write(f"{i}. {result}")

# Accuracy placeholder
if st.session_state.total > 0:
    acc = int((st.session_state.correct / st.session_state.total) * 100)
    st.info(f"🎯 Accuracy: {acc}%")
