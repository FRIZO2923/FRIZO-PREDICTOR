import streamlit as st
import datetime
import pytz
import matplotlib.pyplot as plt

# Set page config
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

# Get period number (last 3 digits)
with st.expander("🔢 Enter Last 3 Digits of Period Number (e.g. 101)"):
    last_digits = st.text_input("Only digits", max_chars=3, placeholder="e.g. 101")
    if last_digits.isdigit():
        st.session_state.current_period = int(last_digits)

if st.session_state.current_period is not None:
    st.markdown(f"### 📌 Starting From Period: `{st.session_state.current_period}`")

# Predict function
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

# Add result
def add_result(result):
    if st.session_state.current_period is not None:
        st.session_state.history.append({
            "period": st.session_state.current_period,
            "result": result
        })
        if st.session_state.last_prediction:
            if st.session_state.last_prediction["value"] == result:
                st.session_state.prediction_stats["correct"] += 1
                st.session_state.wrong_streak = 0
            else:
                st.session_state.wrong_streak += 1
            st.session_state.prediction_stats["total"] += 1
        st.session_state.current_period -= 1
        st.session_state.last_prediction = None

# Add buttons
col1, col2, col3 = st.columns([1, 1, 2])
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

# Show progress
count = len(st.session_state.history)
st.info(f"✅ Data Entered: `{count}` / 50")

# Prediction after 50+
if count >= 50:
    st.markdown("## 🔮 Prediction")
    pred, conf = predict(st.session_state.history)
    if pred:
        st.success(f"📌 Predicted Next: `{pred}` with `{conf}%` confidence")
        st.session_state.last_prediction = {"value": pred, "confidence": conf}
    else:
        st.warning("⚠️ Not enough pattern data for prediction")

    correct = st.session_state.prediction_stats["correct"]
    total = st.session_state.prediction_stats["total"]
    if total > 0:
        acc = int((correct / total) * 100)
        st.markdown(f"🎯 Accuracy: `{correct}` / `{total}` → **{acc}%**")
        if st.session_state.wrong_streak >= 3:
            st.error("⚠️ Trend Reversal Possible!")

# Show history
if st.session_state.history:
    st.markdown("## 📚 History Data (Latest on Top)")
    history_table = []
    for i, entry in enumerate(reversed(st.session_state.history), start=1):
        history_table.append({
            "Sr. No.": i,
            "Period No.": entry["period"],
            "Result": entry["result"]
        })
    st.dataframe(history_table, use_container_width=True)

    # Pie chart
    fig, ax = plt.subplots()
    results = [x["result"] for x in st.session_state.history]
    counts = [results.count("Big"), results.count("Small")]
    ax.pie(counts, labels=["Big", "Small"], autopct="%1.1f%%", startangle=90, colors=["red", "blue"])
    ax.axis("equal")
    st.pyplot(fig)

# Refresh manually
st.button("🔄 Refresh Timer", on_click=st.experimental_rerun)
