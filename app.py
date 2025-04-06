import streamlit as st
import datetime
import pytz
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="Frizo Predictor", layout="centered")

st.title("🎯 Frizo Predictor")
st.markdown("### 👇 Enter 50 rounds of results to unlock Prediction Mode")

# India Standard Time (IST)
ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.datetime.now(ist)
seconds = current_time.second
remaining = 60 - seconds

st.subheader(f"🕒 India Time: `{current_time.strftime('%H:%M:%S')}`")
st.subheader(f"⏳ Next Round In: `{remaining}` seconds")

# Init session variables
if "history" not in st.session_state:
    st.session_state.history = []

# Buttons for input and control
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("🔴 BIG"):
        st.session_state.history.append("Big")
        st.rerun()

with col2:
    if st.button("🔵 SMALL"):
        st.session_state.history.append("Small")
        st.rerun()

with col3:
    if st.button("🧹 Reset History"):
        st.session_state.history = []
        st.session_state._rerun_flag = True

# Pattern count tracker
count = len(st.session_state.history)
st.info(f"🧾 You’ve entered `{count}` / 50 patterns")

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

# Prediction output
if count >= 50:
    st.markdown("## 🧠 Prediction Mode")
    prediction, confidence = predict_next_pattern(st.session_state.history)
    st.success(f"🔮 Predicted: `{prediction}` ({confidence}% confidence)")

# History and pie chart
if st.session_state.history:
    st.markdown("## 🔂 Full History (latest at top)")
    st.write(st.session_state.history[::-1])  # Reverse display

    fig, ax = plt.subplots()
    counts = [st.session_state.history.count("Big"), st.session_state.history.count("Small")]
    ax.pie(counts, labels=["Big", "Small"], autopct="%1.1f%%", startangle=90, colors=["red", "blue"])
    ax.axis("equal")
    st.pyplot(fig)

# Safe rerun for reset history
if st.session_state.get("_rerun_flag", False):
    st.session_state._rerun_flag = False
    st.experimental_rerun()

# Auto-refresh every second
import time
time.sleep(1)
st.rerun()
