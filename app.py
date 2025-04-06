import streamlit as st
import datetime
import pytz
import matplotlib.pyplot as plt

# Configure page
st.set_page_config(page_title="Frizo Predictor", layout="centered")
st.title("🎯 Frizo Predictor")
st.markdown("### 👇 Enter 50 rounds of results to unlock Prediction Mode")

# Get Indian time
ist = pytz.timezone("Asia/Kolkata")
now = datetime.datetime.now(ist)
seconds_left = 60 - now.second
st.subheader(f"🕒 Indian Time: `{now.strftime('%H:%M:%S')}`")
st.subheader(f"⏳ Next Round In: `{seconds_left}` seconds")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "current_period" not in st.session_state:
    st.session_state.current_period = None
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None
if "prediction_stats" not in st.session_state:
    st.session_state.prediction_stats = {"correct": 0, "total": 0}
if "wrong_streak" not in st.session_state:
    st.session_state.wrong_streak = 0

# Enter last 3 digits of period number
with st.expander("🔢 Enter Last 3 Digits of Period Number (e.g. 101)"):
    last_digits = st.text_input("Only digits", max_chars=3, placeholder="e.g. 101")
    if last_digits.isdigit():
        st.session_state.current_period = int(last_digits)

if st.session_state.current_period is not None:
    st.markdown(f"### 📌 Starting From Period: `{st.session_state.current_period}`")

# Prediction logic
def predict(history):
    values = [entry["result"] for entry in history]
    if len(values) < 5:
        return None, 0
    recent = values[-5:]
    pattern_counts = {"Big": 0, "Small": 0}
    for i in range(len(values) - 5):
        if values[i:i+5] == recent:
            next_val = values[i+5]
            pattern_counts[next_val] += 1
    total_matches = sum(pattern_counts.values())
    if total_matches == 0:
        return None, 0
    best = max(pattern_counts, key=pattern_counts.get)
    confidence = int((pattern_counts[best] / total_matches) * 100)
    return best, confidence

# Store result
def add_result(result):
    if st.session_state.current_period is not None:
        st.session_state.history.append({
            "period": st.session_state.current_period,
            "result": result
        })
        # Handle prediction check
        if st.session_state.last_prediction:
            predicted = st.session_state.last_prediction["value"]
            if predicted == result:
                st.session_state.prediction_stats["correct"] += 1
                st.session_state.wrong_streak = 0
            else:
                st.session_state.wrong_streak += 1
            st.session_state.prediction_stats["total"] += 1
        st.session_state.current_period -= 1
        st.session_state.last_prediction = None

# Buttons
col1, col2, col3 = st.columns([1,1,2])
with col1:
    if st.button("🔴 BIG"):
        add_result("Big")
with col2:
    if st.button("🔵 SMALL"):
        add_result("Small")
with col3:
    if st.button("🧹 Reset History"):
        st.session_state.history = []
        st.session_state.current_period = None
        st.session_state.last_prediction = None
        st.session_state.prediction_stats = {"correct": 0, "total": 0}
        st.session_state.wrong_streak = 0

# Progress
count = len(st.session_state.history)
st.info(f"✅ Data Entered: `{count}` / 50")

# Prediction Section
if count >= 50:
    st.markdown("## 🔮 Prediction")
    pred, conf = predict(st.session_state.history)
    if pred:
        st.success(f"📌 Predicted Next: `{pred}` with `{conf}%` confidence")
        st.session_state.last_prediction = {"value": pred, "confidence": conf}
    else:
        st.warning("⚠️ Not enough pattern data for prediction")

    # Accuracy Display
    correct = st.session_state.prediction_stats["correct"]
    total = st.session_state.prediction_stats["total"]
    if total > 0:
        acc = int((correct / total) * 100)
        st.markdown(f"🎯 Accuracy: `{correct}` out of `{total}` → **{acc}%**")
        if st.session_state.wrong_streak >= 3:
            st.error("⚠️ Warning: Possible Trend Reversal Detected!")

# History Data
if st.session_state.history:
    st.markdown("## 📚 History Data (Latest on Top)")
    display_data = []
    for idx, entry in enumerate(reversed(st.session_state.history), 1):
        display_data.append({
            "Sr. No.": idx,
            "Period No.": entry["period"],
            "Result": entry["result"]
        })
    st.dataframe(display_data, use_container_width=True)

    # Pie Chart
    fig, ax = plt.subplots()
    all_results = [h["result"] for h in st.session_state.history]
    counts = [all_results.count("Big"), all_results.count("Small")]
    ax.pie(counts, labels=["Big", "Small"], autopct="%1.1f%%", startangle=90, colors=["red", "blue"])
    ax.axis("equal")
    st.pyplot(fig)

# Manual refresh button
st.button("🔄 Refresh Timer", on_click=lambda: st.rerun())
