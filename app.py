import streamlit as st
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="Frizo Predictor", layout="centered")

st.title("🎯 Frizo Predictor")
st.markdown("1-Min Auto-Timer Mode is now **active** ⏱️")

# Store history in session
if "history" not in st.session_state:
    st.session_state.history = []

# --- TIMER SECTION ---
TIMER_DURATION = 60  # seconds

# Store the timer start time
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Calculate time remaining
elapsed = time.time() - st.session_state.start_time
remaining = max(0, TIMER_DURATION - int(elapsed))

# Timer countdown display
st.subheader(f"⏳ Next Round In: `{remaining}` seconds")

# If timer hits zero
if remaining == 0:
    st.success("🚨 NEW ROUND READY! Log your prediction now.")
    if st.button("🔁 Restart Timer"):
        st.session_state.start_time = time.time()
        st.experimental_rerun()

    st.markdown("### Quick Log:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔴 BIG"):
            st.session_state.history.append("Big")
            st.experimental_rerun()
    with col2:
        if st.button("🔵 SMALL"):
            st.session_state.history.append("Small")
            st.experimental_rerun()

# --- SHOW HISTORY ---
if st.session_state.history:
    st.markdown("## 🧾 History")
    st.write(st.session_state.history)

    # Pie chart
    fig, ax = plt.subplots()
    ax.pie(
        [st.session_state.history.count("Big"), st.session_state.history.count("Small")],
        labels=["Big", "Small"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["red", "blue"]
    )
    ax.axis("equal")
    st.pyplot(fig)

# Auto-refresh the app every 1 sec to keep timer live
st.experimental_rerun()
time.sleep(1)
