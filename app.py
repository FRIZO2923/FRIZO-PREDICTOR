import streamlit as st
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="Frizo Predictor", layout="centered")

st.title("🎯 Frizo Predictor")
st.markdown("1-Min Auto-Timer Mode is now **active** ⏱️")

# Store session variables
if "history" not in st.session_state:
    st.session_state.history = []

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Timer logic
TIMER_DURATION = 60  # seconds
elapsed = time.time() - st.session_state.start_time
remaining = max(0, TIMER_DURATION - int(elapsed))

# Display countdown
st.subheader(f"⏳ Next Round In: `{remaining}` seconds")

# When timer hits 0
if remaining == 0:
    st.success("🚨 NEW ROUND READY! Log your prediction:")

    col1, col2, col3 = st.columns([1, 1, 2])
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

# Show history if available
if st.session_state.history:
    st.markdown("## 🧾 History")
    st.write(st.session_state.history)

    fig, ax = plt.subplots()
    counts = [st.session_state.history.count("Big"), st.session_state.history.count("Small")]
    ax.pie(counts, labels=["Big", "Small"], autopct="%1.1f%%", startangle=90, colors=["red", "blue"])
    ax.axis("equal")
    st.pyplot(fig)

# Smooth auto-refresh using Streamlit's rerun (not HTML meta)
# Add small delay so the app doesn’t overload
if remaining > 0:
    time.sleep(1)
    st.rerun()
