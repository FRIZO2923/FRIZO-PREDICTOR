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

# Buttons to log results
col1, col2, col3, col4 = st.columns([1, 1, 2, 2])

with col1:
    if st.button("🔴 BIG"):
        st.session_state.history.append("Big")
        st.session_state.start_time = time.time()
        st.rerun()

with col2:
    if st.button("🔵 SMALL"):
        st.session_state.history.append("Small")
        st.session_state.start_time = time.time()
        st.rerun()

with col3:
    if st.button("🔁 Restart Timer Only"):
        st.session_state.start_time = time.time()
        st.rerun()

with col4:
    if st.button("🔄 Restart Data"):
        st.session_state.history = []
        st.session_state.start_time = time.time()
        st.experimental_rerun()

# Count tracker
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

# History and Pie Chart
if st.session_state.history:
    st.markdown("## 🔂 Full History (latest at top)")
    st.write(st.session_state.history[::-1])  # Reversed order

    fig, ax = plt.subplots()
    counts = [st.session_state.history.count("Big"), st.session_state.history.count("Small")]
    ax.pie(counts, labels=["Big", "Small"], autopct="%1.1f%%", startangle=90, colors=["red", "blue"])
    ax.axis("equal")
    st.pyplot(fig)

# Auto-refresh timer
if remaining > 0:
    time.sleep(1)
    st.rerun()
