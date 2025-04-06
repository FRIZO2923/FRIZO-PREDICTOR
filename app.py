import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

st.set_page_config(page_title="Big Daddy 1-Min Predictor", layout="centered")
st.title("🎲 Big Daddy Games - 1 Minute Pattern Predictor")

# Initialize session state
if "results" not in st.session_state:
    st.session_state.results = deque(maxlen=50)

# Add result
col1, col2 = st.columns(2)
with col1:
    if st.button("🟥 Big"):
        st.session_state.results.append("Big")
with col2:
    if st.button("🟦 Small"):
        st.session_state.results.append("Small")

# Display results
st.subheader("🔁 Last 50 Results")
st.write(list(st.session_state.results))

# Count occurrences
big_count = st.session_state.results.count("Big")
small_count = st.session_state.results.count("Small")

st.write(f"🔴 Big: {big_count} | 🔵 Small: {small_count}")

# Prediction Logic (Simple)
last_3 = list(st.session_state.results)[-3:]
prediction = "Big" if last_3.count("Small") > last_3.count("Big") else "Small"

st.subheader("🔮 Next Prediction")
st.markdown(f"### Likely: **{prediction}**")

# Line chart of trends
def plot_trends(results):
    numeric = [1 if r == "Big" else 0 for r in results]
    df = pd.DataFrame(numeric, columns=["Big = 1 / Small = 0"])
    st.line_chart(df)

st.subheader("📈 Pattern Trend (1 = Big, 0 = Small)")
plot_trends(st.session_state.results)

st.caption("⚠️ Manual input for now. Auto-tracking coming soon...")
