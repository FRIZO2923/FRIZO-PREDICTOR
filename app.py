import streamlit as st
import datetime
import pytz
import matplotlib.pyplot as plt
import time

# Set page config
st.set_page_config(page_title="Frizo Predictor", layout="centered")
st.title("🎯 Frizo Predictor")
st.markdown("### 👇 Enter 50 rounds of results to unlock Prediction Mode")

# India Time
ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.datetime.now(ist)
seconds = current_time.second
remaining = 60 - seconds

# Session state init
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

# Period Entry
with st.expander("🔢 Enter Last 3 Digits of Period Number (e.g. 101)"):
    last_3 = st.text_input("Enter Last 3 Digits", placeholder="e.g. 101")
    if last_3.isdigit() and 0 <= int(last_3) <= 999:
        st.session_state.current_period = int(last_3)

if st.session_state.current_period is not None:
    st.markdown(f"### 📌 Starting From Period: `{st.session_state.current_period}` (descending)")

# Time
st.subheader(f"🕒 India Time: `{current_time.strftime('%H:%M:%S')}`")
st.subheader(f"⏳ Next Round In: `{remaining}` seconds")

# Prediction Logic
def predict_next_pattern(history):
    values = [h["result"] for h in history]
    if len(values) < 5:
        return None, 0
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

# Buttons
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
        st.session_state.history = []
        st.session_state.current_period = None
        st.session_state.pending_result = None
        st.session_state.last_prediction = None
        st.session_state.prediction_stats = {"correct": 0, "total": 0}
        st.session_state.wrong_streak = 0
        st.rerun()

# Store new result
if st.session_state.pending_result:
    result_data = st.session_state.pending_result
    st.session_state.history.append(result_data)

    # Check prediction accuracy
    if st.session_state.last_prediction:
        predicted = st.session_state.last_prediction["value"]
        actual = result_data["result"]
        st.session_state.prediction_stats["total"] += 1

        if predicted == actual:
            st.session_state.prediction_stats["correct"] += 1
            st.session_state.wrong_streak = 0
        else:
            st.session_state.wrong_streak += 1

    st.session_state.pending_result = None
    st.session_state.last_prediction = None

# Status
count = len(st.session_state.history)
st.info(f"🧾 You’ve entered `{count}` / 50 patterns")

# Prediction Section
if count >= 50:
    st.markdown("## 🧠 Prediction Mode")
    prediction, confidence = predict_next_pattern(st.session_state.history)
    if prediction:
        st.success(f"🔮 Predicted: `{prediction}` ({confidence}% confidence)")
        st.session_state.last_prediction = {"value": prediction, "confidence": confidence}
    else:
        st.warning("⚠️ Not enough matching pattern found.")

    # Accuracy tracking
    correct = st.session_state.prediction_stats["correct"]
    total = st.session_state.prediction_stats["total"]
    if total > 0:
        accuracy = int((correct / total) * 100)
        st.markdown(f"📈 Prediction Accuracy: `{correct}` correct / `{total}` → **{accuracy}%**")
        if st.session_state.wrong_streak >= 3:
            st.error("⚠️ Warning: Trend might be reversing!")

# History Table
if st.session_state.history:
    st.markdown("## 📚 History Data (latest at top)")

    table_data = []
    for idx, entry in enumerate(reversed(st.session_state.history), 1):
        table_data.append({
            "Sr. No.": idx,
            "Period No.": entry["period"],
            "Result": entry["result"]
        })

    st.dataframe(table_data, use_container_width=True)

    # Pie Chart
    fig, ax = plt.subplots()
    results = [entry["result"] for entry in st.session_state.history]
    counts = [results.count("Big"), results.count("Small")]
    ax.pie(counts, labels=["Big", "Small"], autopct="%1.1f%%", startangle=90, colors=["red", "blue"])
    ax.axis("equal")
    st.pyplot(fig)

# Auto-refresh (every second)
time.sleep(1)
st.rerun()
