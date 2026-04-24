"""Streamlit chat UI for the Therapy ChatBot (IGD & BDD)."""

import dotenv
import streamlit as st

from app.services.llm import GroqUnavailableError, generate_reply

dotenv.load_dotenv()

st.set_page_config(
    page_title="Therapy Chatbot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Black & white theme + chat bubbles
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
        .chat-bubble-user {
            background: #000000;
            color: #ffffff !important;
            padding: 12px 16px;
            border-radius: 18px 18px 4px 18px;
            margin: 6px 0;
            max-width: 85%;
            margin-left: auto;
            border: 1px solid #000000;
        }
        .chat-bubble-user * { color: #ffffff !important; }
        .chat-bubble-bot {
            background: #ffffff;
            color: #000000 !important;
            padding: 12px 16px;
            border-radius: 18px 18px 18px 4px;
            margin: 6px 0;
            max-width: 85%;
            margin-right: auto;
            border: 1px solid #000000;
        }
        .chat-row { display: flex; flex-direction: column; }
        .disclaimer {
            background: #f5f5f5;
            border-left: 4px solid #000000;
            padding: 10px 14px;
            border-radius: 4px;
            font-size: 0.85rem;
            color: #000000 !important;
            margin-top: 12px;
        }
        div.stButton > button {
            background: #000000;
            color: #ffffff !important;
            border: 1px solid #000000;
            border-radius: 8px;
            padding: 8px 18px;
            font-weight: 600;
        }
        div.stButton > button:hover {
            background: #ffffff;
            color: #000000 !important;
            border: 1px solid #000000;
        }
        div.stButton > button * { color: inherit !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧹 Session")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption(
        "💡 Tip: open the **📊 Health Dashboard** page from the sidebar to "
        "connect a wearable device and view live vitals."
    )

# ---------------------------------------------------------------------------
# Main chat area
# ---------------------------------------------------------------------------
st.title("💬 Therapy Chatbot")
st.caption(
    "A safe space for support around **Internet Gaming Disorder** and "
    "**Body Dysmorphic Disorder**."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_area = st.container()
with chat_area:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-row"><div class="chat-bubble-user">🧑‍💬 {msg["content"]}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-row"><div class="chat-bubble-bot">🤖 {msg["content"]}</div></div>',
                unsafe_allow_html=True,
            )

user_input = st.chat_input("Share what's on your mind...")

if user_input and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    try:
        with st.spinner("Thinking..."):
            reply = generate_reply(st.session_state.messages)
    except GroqUnavailableError:
        reply = "⚠️ The chatbot is not configured yet. Please contact the administrator."
    except Exception:  # noqa: BLE001
        reply = "⚠️ Sorry, something went wrong. Please try again in a moment."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

st.markdown(
    '<div class="disclaimer">⚠️ This chatbot is for supportive and educational '
    "purposes only. It is <b>not</b> a substitute for professional medical or "
    "psychological care. If you are in crisis, please contact a local emergency "
    "service or a trusted mental-health professional.</div>",
    unsafe_allow_html=True,
)
