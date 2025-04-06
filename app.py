import streamlit as st
import datetime
import pytz
import pandas as pd
import matplotlib.pyplot as plt
import threading
import time
import random

# Setup page
st.set_page_config(page_title="Frizo Predictor", layout="centered")

# Title - centered and styled
# Custom styled title with spacing below
st.markdown(
    """
    <div style='text-align: center; font-size: 48px; font-weight: bold; padding: 20px 0; margin-bottom: 30px;'>
        🎯 FRIZO PREDICTOR 😈
    </div>
    """,
    unsafe_allow_html=True
)


# 🔁 Referral Popup
if "show_referral_message" not in st.session_state:
    st.session_state.show_referral_message = True

if st.session_state.show_referral_message:
    with st.container():
        color = random.choice(["green", "orange", "blue", "purple"])
    st.markdown(
    f"""
    <div style="border: 2px solid orange; padding: 15px; border-radius: 12px; background-color: #f9f9f9; 
                text-align: center; font-size: 18px; animation: blinker 1.5s linear infinite; margin-bottom: 40px;">
        🤑 <strong>Get ₹100 Cashback</strong> on ₹300 Recharge!<br>
        👉 Create a new account using our referral link for best prediction results.<br><br>
        🔗 <a href="https://www.bigdaddygame.net//#/register?invitationCode=Narn6464148" 
              target="_blank" 
              style="text-decoration: none; color: orange; font-weight: bold;">
              Click Here to Register Now</a>
    </div>

    <style>
        @keyframes blinker {{
            50% {{ opacity: 0.6; }}
        }}
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div style='text-align: center; margin-top: 20px; margin-bottom: 20px;'>
        <span style='font-size: 24px; font-weight: bold; color: #333;'>👇 Enter 50 rounds of results to unlock</span><br>
        <span style='font-size: 26px; font-weight: bold; color: #007acc;'>🔐 Prediction Mode</span>
    </div>
    """,
    unsafe_allow_html=True
)


# Indian time sync
ist = pytz.timezone("Asia/Kolkata")
now = datetime.datetime.now(ist)
seconds_left = 60 - now.second
st.subheader(f"🕒 IST 🇮🇳: `{now.strftime('%H:%M:%S')}`")
st.subheader(f"⏳ Next Round In: `{seconds_left}` seconds")

# Timer placeholder
timer_placeholder = st.empty()

if "timer_seconds" not in st.session_state:
    st.session_state.timer_seconds = 60 - now.second

def countdown_timer():
    while True:
        now = datetime.datetime.now(ist)
        st.session_state.timer_seconds = 60 - now.second
        time.sleep(1)

if "timer_thread" not in st.session_state:
    st.session_state.timer_thread = threading.Thread(target=countdown_timer, daemon=True)
    st.session_state.timer_thread.start()

def refresh_timer():
    now = datetime.datetime.now(ist)
    st.session_state.timer_seconds = 60 - now.second

col1, col2 = st.columns([4, 1])
with col1:
    timer_placeholder.text(f"🕐 60-Second Timer: `{st.session_state.timer_seconds}` seconds remaining")
with col2:
    if st.button("🔄 Refresh Timer"):
        refresh_timer()

# Session variables
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

# Input current period
with st.expander("🔢 Enter Last 3 Digits of Current Period"):
    last_digits = st.text_input("Only digits", max_chars=3, placeholder="e.g. 101")
    if last_digits.isdigit():
        st.session_state.current_period = int(last_digits)

if st.session_state.current_period is not None:
    st.markdown(f"### 📌 Current Base Period: `{st.session_state.current_period}`")

def add_result(result):
    if st.session_state.current_period is not None:
        period = st.session_state.current_period
        st.session_state.history.append({"period": period, "result": result})

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
    total = sum(pattern_counts.values())
    if total == 0:
        return None, 0
    best = max(pattern_counts, key=pattern_counts.get)
    confidence = int((pattern_counts[best] / total) * 100)
    return best, confidence

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

count = len(st.session_state.history)
st.info(f"✅ Entries: `{count}` / 50")

if count >= 50:
    st.markdown("## 🔮 Prediction")
    pred, conf = predict(st.session_state.history)

    if pred:
        if st.session_state.wrong_streak >= 3:
            reversed_pred = "Small" if pred == "Big" else "Big"
            st.warning(f"🧭 Reversal Detected — Predicting: `{reversed_pred}` instead of `{pred}`")
            pred = reversed_pred

        st.success(f"📌 Predicted Next: `{pred}` with `{conf}%` confidence")
        st.session_state.last_prediction = {"value": pred, "confidence": conf}
    else:
        st.warning("⚠️ Not enough data")

    correct = st.session_state.prediction_stats["correct"]
    total = st.session_state.prediction_stats["total"]
    if total > 0:
        acc = int((correct / total) * 100)
        st.markdown(f"🎯 Accuracy: `{correct}` / `{total}` → **{acc}%**")
        if st.session_state.wrong_streak >= 3:
            st.error("⚠️ Trend Reversal Suspected")

if st.session_state.history:
    st.markdown("## 📚 History Data (Latest on Top)")
    history_df = pd.DataFrame(reversed(st.session_state.history))
    history_df.index = range(1, len(history_df)+1)
    history_df.index.name = "Sr. No."
    history_df = history_df.rename(columns={"period": "Period No.", "result": "Result"})
    st.dataframe(history_df, use_container_width=True)

    results = [entry["result"] for entry in st.session_state.history]
    fig, ax = plt.subplots()
    ax.pie([
        results.count("Big"),
        results.count("Small")
    ], labels=["Big", "Small"], autopct="%1.1f%%", colors=["red", "blue"], startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    st.markdown("## 📊 Trading-style Trend Tracker")
    trend_data = []
    score = 0
    for entry in reversed(st.session_state.history):
        score += 1 if entry["result"] == "Big" else -1
        trend_data.append(score)
    trend_data.reverse()
    trend_df = pd.DataFrame({"Round": list(range(1, len(trend_data) + 1)), "Trend": trend_data})
    st.line_chart(trend_df.set_index("Round"))

# Footer
st.markdown("""
    <hr style='margin-top: 50px;'>
    <div style='text-align: center; font-size: 18px;'>
        🚀 Created by <strong>Frizo</strong><br><br>
        🎥 Watch on 
        <a href='https://www.youtube.com/@FrizoClips' target='_blank' style='text-decoration: none; color: red; font-weight: bold;'>
            YouTube @FrizoClips
        </a><br><br>
        📢 Join Telegram Channel: 
        <a href='https://t.me/FA_INVESTMENTS88' target='_blank' style='text-decoration: none; color: blue; font-weight: bold;'>
            @FA_INVESTMENTS88
        </a><br><br>
        💸 Contact for Investments: <strong>x10 Returns Possible 💰</strong>
    </div>
""", unsafe_allow_html=True)
