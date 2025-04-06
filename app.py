import streamlit as st
import datetime
import pytz
import pandas as pd
import matplotlib.pyplot as plt
import time

# 📋 Setup page first
st.set_page_config(page_title="Frizo Predictor", layout="centered")
st.title("🎯 Frizo Predictor")
st.markdown("### 👇 Enter 50 rounds of results to unlock Prediction Mode")

# 🇮🇳 Indian Standard Time
ist = pytz.timezone("Asia/Kolkata")
now = datetime.datetime.now(ist)
seconds_left = 60 - now.second
st.subheader(f"🕒 IST: `{now.strftime('%H:%M:%S')}`")
st.subheader(f"⏳ Next Round In: `{seconds_left}` seconds")

# ✅ Safe auto-refresh using rerun
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()
elif time.time() - st.session_state.last_refresh >= 1:
    st.session_state.last_refresh = time.time()
    st.experimental_rerun()
