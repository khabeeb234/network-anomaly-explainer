import streamlit as st
import pandas as pd
import time
from utils import (
    load_metrics,
    load_changes,
    detect_anomalies_isolationforest,
    build_report,
    check_gemini_connection
)
import os

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------
st.set_page_config(
    page_title="Network Anomaly Explainer",
    page_icon="💻",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM THEME CSS
# --------------------------------------------------
if os.path.exists("custom_theme.css"):
    with open("custom_theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER (Centered Layout - Clean Version)
# --------------------------------------------------
st.markdown("""
<div style="
    text-align:center;
    padding:20px 0;
    background:rgba(20,25,35,0.8);
    border-radius:10px;
    box-shadow:0 0 20px rgba(0,150,255,0.25);
    margin-bottom:25px;">
  <h1 style='color:#58b8ff; font-size:36px; margin-bottom:5px;'>
      💻 Network Performance Anomaly Explainer
  </h1>
  <p style='color:#a9c8ff; font-size:16px;'>
      AI-powered diagnostics assistant for identifying and explaining network performance anomalies.
  </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# GEMINI CONNECTION STATUS
# --------------------------------------------------
status, message = check_gemini_connection()
if status:
    st.success(message)
else:
    st.warning(message)

# --------------------------------------------------
# UI LAYOUT
# --------------------------------------------------
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("### 📁 Data Input")

    uploaded_metrics = st.file_uploader(
        "Upload Network Metrics (CSV)",
        type=["csv"],
        help="Upload telemetry with columns like: timestamp, latency_ms, packet_loss, throughput_mbps."
    )

    uploaded_changes = st.file_uploader(
        "Upload Config Changes (CSV)",
        type=["csv"],
        help="Optional: configuration events (timestamp, event, details)."
    )

    use_sample = st.checkbox("Use sample data", value=True)

    st.markdown("### ⚙️ Model Options")

    # --- Expected anomaly fraction with tooltip ---
    st.markdown("""
    <div style="font-size:15px; color:#58b8ff; font-weight:600;">
        Expected anomaly fraction 
        <span title="Fraction of data points likely to be anomalies. 
Example: 0.03 means 3% of your data is expected to be abnormal. 
Lower = fewer anomalies detected, higher = more sensitive detection.">ℹ️</span>
    </div>
    """, unsafe_allow_html=True)
    contamination = st.slider(
        "",
        0.01, 0.5, 0.03, step=0.01,
        help="Percentage of data points likely to be anomalies (e.g., 0.03 = 3%)"
    )

    # --- Correlation window with tooltip ---
    st.markdown("""
    <div style="font-size:15px; color:#58b8ff; font-weight:600; margin-top:15px;">
        Correlation window (minutes)
        <span title="How far (in minutes) around an anomaly the system should search for related configuration events. 
Example: 5 means look ±5 minutes around each anomaly timestamp.">ℹ️</span>
    </div>
    """, unsafe_allow_html=True)
    window_minutes = st.number_input(
        "",
        min_value=1, max_value=60, value=3,
        help="Minutes to look before/after an anomaly for related configuration events"
    )

    use_llm = st.checkbox(
        "Use Gemini AI for explanations",
        value=False,
        help="Enable if you want AI-based natural-language root-cause explanations."
    )

with col2:
    st.markdown("### 🤖 Run Analysis")
    run = st.button("🚀 Analyze Now", use_container_width=True)

# --------------------------------------------------
# DATA HANDLING
# --------------------------------------------------
if use_sample or (not uploaded_metrics):
    df_metrics = load_metrics("sample_data/network_metrics.csv")
else:
    df_metrics = pd.read_csv(uploaded_metrics, parse_dates=["timestamp"])

if use_sample or (not uploaded_changes):
    df_changes = load_changes("sample_data/config_changes.csv")
else:
    df_changes = pd.read_csv(uploaded_changes, parse_dates=["timestamp"])

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------
st.markdown("<hr style='border:1px solid rgba(88,184,255,0.3);margin:20px 0;'>", unsafe_allow_html=True)
st.subheader("📊 Telemetry Preview")
st.dataframe(df_metrics.head(10), use_container_width=True)

# --------------------------------------------------
# RUN ANALYSIS WITH ANIMATED FEEDBACK
# --------------------------------------------------
if run:
    st.markdown("""
    <div style='text-align:center;margin-top:25px;'>
        <div class="loading-pulse"></div>
        <p style='color:#00ffb3;font-weight:bold;margin-top:10px;font-size:16px;'>
        Running anomaly detection and AI correlation... please wait ⏳</p>
    </div>
    """, unsafe_allow_html=True)

    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.03)
        progress_bar.progress(i + 1)

    metrics_df, model = detect_anomalies_isolationforest(df_metrics.copy(), contamination=contamination)

    st.success("✅ Analysis Complete!")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("🔍 Anomaly Summary")

    summary_df = metrics_df[metrics_df["anomaly_isof"]].copy()
    if summary_df.empty:
        st.info("No anomalies detected.")
    else:
        st.dataframe(
            summary_df[["timestamp", "latency_ms", "packet_loss", "throughput_mbps"]],
            use_container_width=True
        )

    st.subheader("📘 Detailed AI Explanations")
    anomalies = build_report(
        metrics_df,
        df_changes,
        window_seconds=int(window_minutes * 60),
        use_llm=use_llm
    )

    if not anomalies:
        st.warning("No explanations generated.")
    else:
        for a in anomalies:
            st.markdown(f"### 🕒 {a['timestamp']}")
            st.write(f"**Latency:** {a['latency_ms']} ms | **Packet loss:** {a['packet_loss']}% | **Throughput:** {a['throughput_mbps']} Mbps")
            if a['changes']:
                st.markdown("**Correlated Events:**")
                for c in a['changes']:
                    st.write(f"- {c['timestamp']}: {c['event']} — {c.get('details','')}")
            st.markdown("**AI Explanation:**")
            st.info(a['explanation'])
            st.markdown("<hr>", unsafe_allow_html=True)

# --------------------------------------------------
# CSS ANIMATION
# --------------------------------------------------
st.markdown("""
<style>
/* Animated AI Pulse Loader */
.loading-pulse {
  display:inline-block;
  width:50px;
  height:50px;
  border-radius:50%;
  background:radial-gradient(circle, #00eaff 10%, transparent 11%), 
              radial-gradient(circle, #00eaff 10%, transparent 11%);
  background-position:0 0, 25px 25px;
  background-size:50px 50px;
  animation:pulse 1s infinite;
  box-shadow:0 0 25px #00eaff;
}

@keyframes pulse {
  0% { transform:scale(1); opacity:1; }
  50% { transform:scale(1.3); opacity:0.6; }
  100% { transform:scale(1); opacity:1; }
}
</style>
""", unsafe_allow_html=True)
