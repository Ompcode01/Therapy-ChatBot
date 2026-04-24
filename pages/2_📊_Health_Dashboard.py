"""Wearable-device health dashboard (simulated)."""

from __future__ import annotations

import random
import time
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Health Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Black & white theme
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp {
            background: #ffffff;
            color: #000000;
        }
        section[data-testid="stSidebar"] {
            background: #f5f5f5;
            border-right: 1px solid #d4d4d4;
        }
        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: #000000 !important;
        }
        div[data-testid="stMetric"] {
            background: #ffffff;
            padding: 16px 18px;
            border-radius: 8px;
            border: 1px solid #000000;
        }
        div[data-testid="stMetric"] * { color: #000000 !important; }
        div.stButton > button {
            background: #000000;
            color: #ffffff !important;
            border: 1px solid #000000;
            border-radius: 8px;
            padding: 10px 22px;
            font-weight: 600;
        }
        div.stButton > button:hover {
            background: #ffffff;
            color: #000000 !important;
            border: 1px solid #000000;
        }
        div.stButton > button * { color: inherit !important; }
        .device-card {
            background: #ffffff;
            border-radius: 8px;
            padding: 18px 22px;
            border: 1px solid #000000;
        }
        .device-card * { color: #000000 !important; }
        div[data-testid="stProgress"] > div > div > div > div { background: #000000 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📊 Wearable Health Dashboard")
st.caption("Connect a smartwatch and monitor live vitals alongside a derived stress score.")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _read_vitals() -> dict:
    """Generate one snapshot of simulated wearable data."""
    spo2 = random.randint(95, 100)
    heart_rate = random.randint(60, 100)
    bp_sys = random.randint(110, 130)
    bp_dia = random.randint(70, 85)
    skin_temp = round(random.uniform(36.1, 37.2), 1)
    steps = random.randint(0, 220)  # steps in the last minute
    return {
        "ts": datetime.now(),
        "spo2": spo2,
        "heart_rate": heart_rate,
        "bp_sys": bp_sys,
        "bp_dia": bp_dia,
        "skin_temp": skin_temp,
        "steps": steps,
    }


def _stress_score(v: dict) -> int:
    """Derive a 1–10 stress score from vitals (simple heuristic)."""
    score = 0.0
    score += max(0, (v["heart_rate"] - 70)) * 0.10
    score += max(0, (v["bp_sys"] - 115)) * 0.12
    score += max(0, (v["bp_dia"] - 75)) * 0.10
    score += max(0, (98 - v["spo2"])) * 0.55
    score += max(0, (v["skin_temp"] - 36.5)) * 1.4
    return int(max(1, min(10, round(score) + 1)))


def _stress_label(score: int) -> tuple[str, str]:
    if score <= 3:
        return "Calm", "○"
    if score <= 6:
        return "Mild", "◔"
    if score <= 8:
        return "Elevated", "◑"
    return "High", "●"


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "device_connected" not in st.session_state:
    st.session_state.device_connected = False
if "device_name" not in st.session_state:
    st.session_state.device_name = ""
if "vitals_history" not in st.session_state:
    st.session_state.vitals_history = []

# ---------------------------------------------------------------------------
# Sidebar – device controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⌚ Device")
    device_choice = st.selectbox(
        "Select a wearable",
        ["Apple Watch (simulated)", "Fitbit Sense (simulated)", "Galaxy Watch (simulated)", "Mi Band (simulated)"],
        index=0,
    )

    auto_refresh = st.checkbox("Auto-refresh every 3s", value=False)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔗 Connect", use_container_width=True, disabled=st.session_state.device_connected):
            with st.spinner(f"Pairing with {device_choice}..."):
                time.sleep(0.8)
            st.session_state.device_connected = True
            st.session_state.device_name = device_choice
            st.session_state.vitals_history = []
            st.rerun()
    with col_b:
        if st.button("✂️ Disconnect", use_container_width=True, disabled=not st.session_state.device_connected):
            st.session_state.device_connected = False
            st.session_state.device_name = ""
            st.rerun()

    st.markdown("---")
    st.caption("💡 Data shown here is **simulated** for demo purposes.")

# ---------------------------------------------------------------------------
# Main body
# ---------------------------------------------------------------------------
if not st.session_state.device_connected:
    st.markdown(
        """
        <div class="device-card">
            <h3 style="margin-top:0;">No device connected</h3>
            <p>Pick a wearable in the sidebar and click <b>Connect</b> to start
            streaming simulated SpO₂, blood pressure, heart rate and a derived
            stress score.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    vitals = _read_vitals()
    st.session_state.vitals_history.append(vitals)
    st.session_state.vitals_history = st.session_state.vitals_history[-60:]

    stress = _stress_score(vitals)
    label, marker = _stress_label(stress)

    st.markdown(
        f"""
        <div class="device-card">
            <b>📡 Connected to:</b> {st.session_state.device_name}
            &nbsp;•&nbsp; Last sync: {vitals['ts'].strftime('%H:%M:%S')}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🫁 SpO₂", f"{vitals['spo2']} %", help="Blood oxygen saturation (95-100% normal)")
    c2.metric("❤️ Heart rate", f"{vitals['heart_rate']} bpm", help="Resting HR 60-100 bpm")
    c3.metric("🩸 Blood pressure", f"{vitals['bp_sys']}/{vitals['bp_dia']}", help="Systolic / diastolic mmHg")
    c4.metric("🌡️ Skin temp", f"{vitals['skin_temp']} °C", help="Surface temperature")

    st.write("")
    s1, s2 = st.columns([1, 2])
    with s1:
        st.markdown(f"#### {marker} Stress level")
        st.metric("Score (1–10)", f"{stress}", delta=label)
        st.progress(stress / 10)
        if stress >= 7:
            st.warning("Elevated stress detected. Try a 1-minute breathing exercise.")
        elif stress <= 3:
            st.success("You look calm — nice work staying balanced.")

    with s2:
        st.markdown("#### 📈 Trend (last minute)")
        df = pd.DataFrame(
            [
                {
                    "time": v["ts"].strftime("%H:%M:%S"),
                    "Heart rate": v["heart_rate"],
                    "SpO₂": v["spo2"],
                    "Stress": _stress_score(v),
                }
                for v in st.session_state.vitals_history
            ]
        ).set_index("time")
        st.line_chart(df, height=240, color=["#000000", "#737373", "#a3a3a3"])

    st.write("")
    with st.expander("🪜 Activity & detail"):
        st.write(f"**Steps in last minute:** {vitals['steps']}")
        st.write(
            "Stress score is a heuristic computed from heart rate, blood "
            "pressure, SpO₂ and skin temperature. It is **not** a clinical "
            "measurement."
        )

    if auto_refresh:
        time.sleep(3)
        st.rerun()
    else:
        if st.button("🔄 Refresh reading"):
            st.rerun()
