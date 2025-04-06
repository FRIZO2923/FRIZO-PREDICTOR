import streamlit as st
import datetime
import pytz
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Frizo Predictor", layout="centered")
st.title("🎯 Frizo Predictor")
st.markdown("### 👇 Enter 50 rounds of results to unlock Prediction Mode")

# Get Indian Standard Time
ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.datetime.now(ist)
seconds = current_time.second
remaining = 60 - seconds
st.subheader(f"🕒 India Time: `{current_time.strftime('%H:%M:%S')}`")
st.subheader(f"⏳ Next Round In: `{remaining}` seconds")

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

# Period number input
with st.expander("🔢 Enter Last 3 Digits of Period Number (e.g. 101)"):
    last_3 = st.text_input("Enter 3 Digits", placeholder="e.g. 101")
    if last_3.isdigit() and 0 <= int(last_3) <= 999:
        st.session_state.current_period = int(last_3)

if st.session_state.current_period is not None:
    st.markdown(f"### 🧾 Current Period: `{st.session_state.current_period}` (desc.)")

# Prediction function
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

# Add result
def add_result(result):
    if st.session_state.current_period is not None:
        entry = {
            "period": st.session_state.current_period,
            "result": result
        }
        st.session_state.history.append(entry)

        # Track prediction result
        if st.session_state.last_prediction:
            predicted = st.session_state.last_prediction["value"]
            actual = result
            st.session_state.prediction_stats["total"] += 1
            if predicted == actual:
                st.session_state.prediction_stats["correct"] += 1
                st.session_state.wrong_streak = 0
            else:
                st.session_state.wrong_streak += 1

        # Decrease period for next round
        st.session_state.current_period -= 1
        st.session_state.last_prediction = None

# Buttons
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

# Progress tracker
count = len(st.session_state.history)
st.info(f"✅ Data Entered: `{count}` / 50")

# Prediction display
if count >= 50:
    st.markdown("## 🔮 Prediction")
    prediction, confidence = predict_next_pattern(st.session_state.history)
    if prediction:
        st.success(f"📌 Predicted Next: `{prediction}` ({confidence}% confidence)")
        st.session_state.last_prediction = {"value": prediction, "confidence": confidence}
    else:
        st.warning("⚠️ No matching pattern found.")

    # Accuracy display
    correct = st.session_state.prediction_stats["correct"]
    total = st.session_state.prediction_stats["total"]
    if total > 0:
        accuracy = int((correct / total) * 100)
        st.markdown(f"🎯 Accuracy: `{correct}` correct / `{total}` → **{accuracy}%**")
        if st.session_state.wrong_streak >= 3:
            st.error("⚠️ Warning: Possible trend reversal!")

# History table
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

    # Pie chart
    fig, ax = plt.subplots()
    results = [e["result"] for e in st.session_state.history]
    counts = [results.count("Big"), results.count("Small")]
    ax.pie(counts, labels=["Big", "Small"], autopct="%1.1f%%", startangle=90, colors=["red", "blue"])
    ax.axis("equal")
    st.pyplot(fig)

# Manual refresh button (optional)
if st.button("🔄 Refresh Timer"):
    st.rerun()
