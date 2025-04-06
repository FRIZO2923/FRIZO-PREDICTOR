import streamlit as st
import datetime
import pytz
import matplotlib.pyplot as plt
import time

# Set Streamlit page config
st.set_page_config(page_title="Frizo Predictor", layout="centered")

st.title("🎯 Frizo Predictor")
st.markdown("### 👇 Enter 50 rounds of results to unlock Prediction Mode")

# India Standard Time (IST)
ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.datetime.now(ist)
seconds = current_time.second
remaining = 60 - seconds

# Session state setup
if "history" not in st.session_state:
    st.session_state.history = []
if "current_period" not in st.session_state:
    st.session_state.current_period = None

# Input: Only 3 digits of last period number
with st.expander("🔢 Enter Last 3 Digits of Period Number (e.g. 101)"):
    last_3 = st.text_input("Enter Last 3 Digits", placeholder="e.g. 101")

    if last_3.isdigit() and 0 <= int(last_3) <= 999:
        st.session_state.current_period = int(last_3)

if st.session_state.current_period is not None:
    st.markdown(f"### 📌 Starting From Period: `{st.session_state.current_period}` (descending)")

# Time display
st.subheader(f"🕒 India Time: `{current_time.strftime('%H:%M:%S')}`")
st.subheader(f"⏳ Next Round In: `{remaining}` seconds")

# Button actions
col1, col2, col3 = st.columns([1, 1, 2])

def add_result(result):
    if st.session_state.current_period is not None:
        current = st.session_state.current_period
        st.session_state.history.append({
            "period": current,
            "result": result
        })
        st.session_state.current_period -= 1  # Decrease BEFORE rerun
        st.rerun()

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
        st.session_state._rerun_flag = True

# Track pattern entry count
count = len(st.session_state.history)
st.info(f"🧾 You’ve entered `{count}` / 50 patterns")

# Prediction logic
def predict_next_pattern(history):
    values = [h["result"] for h in history]
    recent = values[-5:]
    pattern_counts = {"Big": 0, "Small": 0}
    for i in range(len(values) - 5):
        if values[i:i+5] == recent:
            next_value = values[i+5]
            pattern_counts[next_value] += 1
    if sum(pattern_counts.values()) == 0:
        return "❓ Not enough pattern matches", 0
    prediction = max(pattern_counts, key=pattern_counts.get)
    confidence = int((pattern_counts[prediction] / sum(pattern_counts.values())) * 100)
    return prediction, confidence

# Show prediction if enough data
if count >= 50:
    st.markdown("## 🧠 Prediction Mode")
    prediction, confidence = predict_next_pattern(st.session_state.history)
    st.success(f"🔮 Predicted: `{prediction}` ({confidence}% confidence)")

# Show history
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

    # Pie chart visualization
    fig, ax = plt.subplots()
    all_results = [entry["result"] for entry in st.session_state.history]
    counts = [all_results.count("Big"), all_results.count("Small")]
    ax.pie(counts, labels=["Big", "Small"], autopct="%1.1f%%", startangle=90, colors=["red", "blue"])
    ax.axis("equal")
    st.pyplot(fig)

# Reset trigger
if st.session_state.get("_rerun_flag", False):
    st.session_state._rerun_flag = False
    st.experimental_rerun()

# Auto refresh every second
time.sleep(1)
st.rerun()
