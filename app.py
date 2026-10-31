"""CampusBuddy - AI-Powered College Survival Assistant
===================================================
A student-focused, hackathon-ready Streamlit application designed to help
students navigate campus life, academic milestones, and day-to-day survival.

Prepared for local LLM integration via Ollama with configurable model support.
"""

import json
import os
import requests
import streamlit as st

# -----------------------------------------------------------------------------
# Streamlit Page Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CampusBuddy - College Survival Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE_PATH = "campus_data.json"

# -----------------------------------------------------------------------------
# Custom Styling: Consistent Light Theme, Navy/Purple Accents, Readable Buttons
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* -------------------------------------------------------------------------
       1. Base Page Styling & Consistent Light Theme
       ------------------------------------------------------------------------- */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* -------------------------------------------------------------------------
       2. Sidebar Styling: Light Blue Background, Compact Spacing, Navy Labels
       ------------------------------------------------------------------------- */
    section[data-testid="stSidebar"] {
        background-color: #F0F6FF !important;
        border-right: 1px solid #DCE6F5 !important;
    }

    /* Fix excessive top & vertical padding in sidebar */
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* All Sidebar Text, Headings & Labels: High-Contrast Dark Navy */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] strong,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #0F172A !important;
    }

    section[data-testid="stSidebar"] hr {
        margin: 12px 0 !important;
        border-color: #CBD5E1 !important;
    }

    /* Sidebar Text Input Fields */
    section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p {
        color: #0F172A !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }
    section[data-testid="stSidebar"] input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-size: 0.9rem !important;
    }
    section[data-testid="stSidebar"] input:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }

    /* -------------------------------------------------------------------------
       3. Sidebar Radio Navigation: Horizontal Alignment & High-Contrast Text
       ------------------------------------------------------------------------- */
    div[data-testid="stRadio"] {
        margin-top: 2px !important;
        margin-bottom: 6px !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
    }

    /* Radio Item Container Card */
    div[data-testid="stRadio"] label[data-baseweb="radio"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
        padding: 9px 12px !important;
        margin: 0 !important;
        cursor: pointer !important;
        width: 100% !important;
        box-sizing: border-box !important;
        transition: all 0.15s ease-in-out !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
    }

    /* Ensure radio circle container and label align horizontally */
    div[data-testid="stRadio"] label[data-baseweb="radio"] > div {
        display: inline-flex !important;
        align-items: center !important;
    }

    /* Navigation Label Text: Dark Navy and Perfectly Aligned */
    div[data-testid="stRadio"] label[data-baseweb="radio"] p,
    div[data-testid="stRadio"] label[data-baseweb="radio"] span,
    div[data-testid="stRadio"] label[data-baseweb="radio"] div:last-child p {
        color: #0F172A !important;
        font-size: 0.93rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
        padding-left: 6px !important;
        line-height: 1.3 !important;
        white-space: nowrap !important;
    }

    /* Radio Hover State */
    div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
        background-color: #EDE9FE !important;
        border-color: #8B5CF6 !important;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.15) !important;
    }
    div[data-testid="stRadio"] label[data-baseweb="radio"]:hover p,
    div[data-testid="stRadio"] label[data-baseweb="radio"]:hover span {
        color: #4C1D95 !important;
    }

    /* Radio Active / Selected State */
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
        background-color: #EEF2FF !important;
        border-color: #6366F1 !important;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2) !important;
    }
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p,
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span {
        color: #4338CA !important;
        font-weight: 700 !important;
    }

    /* -------------------------------------------------------------------------
       4. Universal Button Resets & Light Theming (No Black Boxes)
       ------------------------------------------------------------------------- */
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"],
    .stButton > button {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important;
        transition: all 0.15s ease-in-out !important;
    }

    button[data-testid="baseButton-secondary"] p,
    button[data-testid="baseButton-primary"] p,
    .stButton > button p,
    .stButton > button span {
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    /* Standard Button Hover State */
    button[data-testid="baseButton-secondary"]:hover,
    button[data-testid="baseButton-primary"]:hover,
    .stButton > button:hover {
        background-color: #EEF2FF !important;
        border-color: #6366F1 !important;
        color: #4338CA !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15) !important;
        transform: translateY(-1px) !important;
    }

    button[data-testid="baseButton-secondary"]:hover p,
    button[data-testid="baseButton-primary"]:hover p,
    .stButton > button:hover p,
    .stButton > button:hover span {
        color: #4338CA !important;
    }

    /* -------------------------------------------------------------------------
       5. Quick Action Cards: White Background, Purple Borders, Navy Text
       ------------------------------------------------------------------------- */
    .prompt-card {
        background: #FFFFFF !important;
        border: 2px solid #818CF8 !important;
        border-radius: 14px !important;
        padding: 18px 20px !important;
        box-shadow: 0 3px 6px -1px rgba(99, 102, 241, 0.06) !important;
        transition: all 0.2s ease-in-out !important;
        margin-top: 6px !important;
        margin-bottom: 6px !important;
    }

    .prompt-card:hover {
        border-color: #6366F1 !important;
        box-shadow: 0 10px 24px -4px rgba(99, 102, 241, 0.2) !important;
        transform: translateY(-2px) !important;
    }

    .prompt-category {
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        color: #4F46E5 !important;
        margin-bottom: 4px !important;
    }

    .prompt-text {
        font-size: 1.08rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        margin-bottom: 6px !important;
        line-height: 1.35 !important;
    }

    .prompt-desc {
        font-size: 0.88rem !important;
        color: #334155 !important;
        line-height: 1.45 !important;
    }

    /* Quick Action Buttons in Grid Columns */
    div[data-testid="stColumn"] .stButton > button {
        background-color: #EDE9FE !important;
        border: 1.5px solid #C4B5FD !important;
        color: #4338CA !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        margin-bottom: 14px !important;
    }

    div[data-testid="stColumn"] .stButton > button p,
    div[data-testid="stColumn"] .stButton > button span {
        color: #4338CA !important;
        font-weight: 700 !important;
    }

    div[data-testid="stColumn"] .stButton > button:hover {
        background-color: #6366F1 !important;
        border-color: #4F46E5 !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.28) !important;
        transform: translateY(-1px) !important;
    }

    div[data-testid="stColumn"] .stButton > button:hover p,
    div[data-testid="stColumn"] .stButton > button:hover span {
        color: #FFFFFF !important;
    }

    /* -------------------------------------------------------------------------
       6. Primary Form Submit Button (Ask CampusBuddy)
       ------------------------------------------------------------------------- */
    button[data-testid="baseButton-primaryFormSubmit"] {
        background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25) !important;
    }

    button[data-testid="baseButton-primaryFormSubmit"] p,
    button[data-testid="baseButton-primaryFormSubmit"] span {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    button[data-testid="baseButton-primaryFormSubmit"]:hover {
        background: linear-gradient(135deg, #4338CA 0%, #4F46E5 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.35) !important;
        transform: translateY(-1px) !important;
    }

    button[data-testid="baseButton-primaryFormSubmit"]:hover p,
    button[data-testid="baseButton-primaryFormSubmit"]:hover span {
        color: #FFFFFF !important;
    }

    /* -------------------------------------------------------------------------
       7. Hero Banner, Cards & Badges
       ------------------------------------------------------------------------- */
    .hero-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #312E81 100%) !important;
        border-radius: 16px !important;
        padding: 26px 30px !important;
        color: #FFFFFF !important;
        margin-bottom: 22px !important;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    .hero-title {
        font-size: 2.1rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.025em !important;
        margin-bottom: 6px !important;
        color: #FFFFFF !important;
    }
    .hero-tagline {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #A5B4FC !important;
        margin-bottom: 6px !important;
    }
    .hero-subtitle {
        font-size: 0.95rem !important;
        color: #E2E8F0 !important;
        margin: 0 !important;
        line-height: 1.4 !important;
    }

    .buddy-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px !important;
        padding: 20px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 2px 4px rgba(15, 23, 42, 0.03) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease !important;
    }
    .buddy-card:hover {
        border-color: #C7D2FE !important;
        box-shadow: 0 10px 20px -3px rgba(99, 102, 241, 0.08) !important;
    }

    .demo-badge {
        display: inline-block !important;
        background-color: #EDE9FE !important;
        color: #6D28D9 !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        padding: 3px 8px !important;
        border-radius: 6px !important;
        border: 1px solid #DDD6FE !important;
        text-transform: uppercase !important;
        margin-bottom: 8px !important;
    }

    .demo-banner {
        background-color: #F5F3FF !important;
        border-left: 4px solid #7C3AED !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
        margin-bottom: 22px !important;
        color: #4C1D95 !important;
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
        border: 1px solid #EDE9FE !important;
    }

    .status-pill {
        display: inline-flex !important;
        align-items: center !important;
        padding: 4px 10px !important;
        border-radius: 20px !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        margin-top: 4px !important;
    }
    .status-online {
        background-color: #ECFDF5 !important;
        color: #065F46 !important;
        border: 1px solid #A7F3D0 !important;
    }
    .status-offline {
        background-color: #FEF2F2 !important;
        color: #991B1B !important;
        border: 1px solid #FECACA !important;
    }
    .status-untested {
        background-color: #F1F5F9 !important;
        color: #1E293B !important;
        border: 1px solid #CBD5E1 !important;
    }

    /* Tabs Styling */
    button[data-baseweb="tab"] {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"] p {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #6366F1 !important;
    }
    button[data-baseweb="tab"]:hover p {
        color: #6366F1 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #4F46E5 !important;
        border-bottom-color: #4F46E5 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #4F46E5 !important;
        font-weight: 700 !important;
    }

    /* Inputs in Main Area */
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    div[data-testid="stTextInput"] label p {
        color: #0F172A !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
NAV_OPTIONS = [
    "🤖 AI Campus Assistant",
    "🏛️ Campus Guide",
    "🧰 Student Survival Toolkit",
]

if "current_page" not in st.session_state:
    st.session_state.current_page = NAV_OPTIONS[0]

if "ollama_status" not in st.session_state:
    st.session_state.ollama_status = {
        "checked": False,
        "connected": False,
        "models": [],
        "message": "Connection has not been tested yet.",
    }

if "configured_model" not in st.session_state:
    st.session_state.configured_model = "gemma4:e2b"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "active_query" not in st.session_state:
    st.session_state.active_query = ""

# Checklist state for the Hostel Essentials Toolkit
DEFAULT_CHECKLIST = {
    "Bedding: Fitted bedsheet and pillow covers": False,
    "Bedding: Light quilt or cozy blanket": False,
    "Tech: Surge-protected multi-plug power strip": False,
    "Tech: Long (6ft-10ft) phone & laptop charging cables": False,
    "Tech: Desk reading lamp with warm light": False,
    "Hygiene: Shower caddy with drainage holes": False,
    "Hygiene: Bathroom flip-flops / shower slippers": False,
    "Hygiene: Personal first-aid & emergency medicine pouch": False,
    "Laundry: Mesh laundry hamper and detergent pods": False,
    "Laundry: Set of sturdy plastic clothes hangers": False,
    "Documents: College ID, admission letter & document photocopies": False,
    "Daily Essentials: Reusable water bottle and stainless steel mug": False,
}

if "hostel_checklist" not in st.session_state:
    st.session_state.hostel_checklist = DEFAULT_CHECKLIST.copy()


# -----------------------------------------------------------------------------
# Data Loader
# -----------------------------------------------------------------------------
@st.cache_data
def load_campus_data(filepath: str = DATA_FILE_PATH) -> dict:
    """Load demonstration campus data safely from JSON file."""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as err:
        st.error(f"Error loading campus data: {err}")
        return {}


campus_data = load_campus_data(DATA_FILE_PATH)


# -----------------------------------------------------------------------------
# Ollama Connection & Query Logic
# -----------------------------------------------------------------------------
def check_ollama_connection(base_url: str):
    """Test connection to local Ollama instance and fetch installed model tags."""
    try:
        response = requests.get(f"{base_url.rstrip('/')}/api/tags", timeout=3)
        if response.status_code == 200:
            payload = response.json()
            models = [m.get("name") for m in payload.get("models", [])]
            return {
                "checked": True,
                "connected": True,
                "models": models,
                "message": "Connected to local Ollama server.",
            }
        return {
            "checked": True,
            "connected": False,
            "models": [],
            "message": f"Ollama returned HTTP status {response.status_code}.",
        }
    except requests.exceptions.ConnectionError:
        return {
            "checked": True,
            "connected": False,
            "models": [],
            "message": "Could not connect. Ensure the Ollama service is running.",
        }
    except Exception as exc:
        return {
            "checked": True,
            "connected": False,
            "models": [],
            "message": f"Error: {exc}",
        }


def build_supporting_context() -> str:
    """Extract demonstration campus knowledge to supply as background reference to Ollama."""
    parts = []
    facilities = campus_data.get("facilities", [])
    if facilities:
        parts.append("Campus Facilities & Operating Hours (DEMO DATA):")
        for f in facilities:
            parts.append(f"- {f.get('name')} ({f.get('category')}): {f.get('hours')}")
    services = campus_data.get("sample_services_directory", [])
    if services:
        parts.append("\nSupport Services Directory (DEMO DATA):")
        for s in services:
            parts.append(f"- {s.get('service_name')}: {s.get('general_location')} ({s.get('coverage')})")
    faqs = campus_data.get("general_survival_faqs", [])
    if faqs:
        parts.append("\nGeneral Campus Survival Guidelines (DEMO DATA):")
        for f in faqs:
            parts.append(f"- Q: {f.get('question')} | A: {f.get('answer')}")
    return "\n".join(parts)


def answer_student_question(query: str, model_tag: str, base_url: str) -> str:
    """Answer a student question using the local Ollama /api/chat endpoint with supporting context."""
    clean_query = query.strip()
    if not clean_query:
        return "Please enter a valid question or challenge."

    active_model = model_tag.strip() if model_tag and model_tag.strip() else "gemma4:e2b"
    api_endpoint = f"{base_url.rstrip('/')}/api/chat"

    supporting_context = build_supporting_context()
    system_prompt = (
        "You are CampusBuddy, a warm, supportive, and practical AI college survival assistant. "
        "Provide direct, actionable, encouraging, and clear student advice.\n\n"
        "Below is sample campus demonstration information. Use this ONLY as supporting background "
        "context when directly relevant to the student's question, and synthesize an original, "
        "helpful response tailored to their inquiry.\n\n"
        f"--- SUPPORTING CAMPUS CONTEXT (DEMO DATA) ---\n{supporting_context}\n------------------------------------------"
    )

    payload = {
        "model": active_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": clean_query},
        ],
        "stream": False,
    }

    try:
        resp = requests.post(api_endpoint, json=payload, timeout=120)
        if resp.status_code == 200:
            data = resp.json()
            message = data.get("message", {})
            # Primary response from assistant
            answer = message.get("content", "").strip()
            # If the thinking model outputted text in thinking field
            if not answer and message.get("thinking"):
                answer = message.get("thinking", "").strip()

            if answer:
                if "ollama_status" in st.session_state:
                    st.session_state.ollama_status["connected"] = True
                    st.session_state.ollama_status["checked"] = True
                return f"**[Generated via local model: `{active_model}`]**\n\n{answer}"
            else:
                return (
                    f"⚠️ **Empty response from Ollama (`{active_model}`):** "
                    "The model completed without generating text. Please try asking again."
                )
        else:
            err_msg = resp.text
            try:
                err_msg = resp.json().get("error", resp.text)
            except Exception:
                pass
            return (
                f"⚠️ **Ollama API Error ({resp.status_code}):** {err_msg}\n\n"
                f"Endpoint: `{api_endpoint}` | Model: `{active_model}`"
            )

    except requests.exceptions.Timeout:
        return (
            f"⚠️ **Request Timed Out:** The local model `{active_model}` took longer than 120 seconds to respond. "
            "Because this model runs locally on your machine, it may require more time or system memory. Please try again."
        )
    except requests.exceptions.ConnectionError:
        if "ollama_status" in st.session_state:
            st.session_state.ollama_status["connected"] = False
            st.session_state.ollama_status["checked"] = True
        return (
            f"⚠️ **Ollama Connection Error:** Could not connect to Ollama at `{base_url}`. "
            "Please ensure that the Ollama service is running (`ollama serve`) and accessible."
        )
    except Exception as exc:
        return f"⚠️ **Ollama Error:** Unexpected error communicating with `{active_model}`: {exc}"


def handle_prompt_click(prompt_text: str):
    """Process a quick prompt click, set active query, and navigate to AI assistant."""
    st.session_state.current_page = "🤖 AI Campus Assistant"
    st.session_state.active_query = ""

    clean_prompt = prompt_text.strip()
    # Check if this exact prompt was already the last question asked to prevent duplicates
    last_user_query = None
    for msg in reversed(st.session_state.chat_history):
        if msg.get("role") == "user":
            last_user_query = msg.get("content", "").strip()
            break

    if clean_prompt and clean_prompt != last_user_query:
        response = answer_student_question(
            query=clean_prompt,
            model_tag=st.session_state.configured_model,
            base_url=st.session_state.get(
                "ollama_base_url", "http://localhost:11434"
            ),
        )
        st.session_state.chat_history.append(
            {"role": "user", "content": clean_prompt}
        )
        st.session_state.chat_history.append(
            {"role": "assistant", "content": response}
        )


# -----------------------------------------------------------------------------
# Sidebar: Compact, Light Blue Background, Navy Labels, Aligned Navigation
# -----------------------------------------------------------------------------
with st.sidebar:
    # 1. Branding Header
    st.markdown(
        """
        <div style="padding-bottom: 2px;">
            <div style="font-size: 1.45rem; font-weight: 800; color: #0F172A; display: flex; align-items: center; gap: 8px;">
                <span>🎓</span> <span>CampusBuddy</span>
            </div>
            <div style="font-size: 0.88rem; font-weight: 600; color: #1E293B; margin-top: 4px; line-height: 1.35;">
                Your AI companion for surviving and thriving in college.
            </div>
            <div style="font-size: 0.78rem; color: #475569; margin-top: 4px; line-height: 1.35;">
                From campus questions to college life advice, get help with your student journey.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    # 2. Navigation with Horizontal Icon & Label Alignment
    st.markdown(
        "<div style='font-size: 0.95rem; font-weight: 700; color: #0F172A; margin-bottom: 6px;'>🧭 Navigation</div>",
        unsafe_allow_html=True,
    )
    selected_page = st.radio(
        "Select Section",
        options=NAV_OPTIONS,
        index=NAV_OPTIONS.index(st.session_state.current_page)
        if st.session_state.current_page in NAV_OPTIONS
        else 0,
        label_visibility="collapsed",
    )
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        st.rerun()

    st.divider()

    # 3. Ollama Connection & Model Configuration
    st.markdown(
        "<div style='font-size: 0.95rem; font-weight: 700; color: #0F172A; margin-bottom: 6px;'>⚙️ Local Ollama Setup</div>",
        unsafe_allow_html=True,
    )

    ollama_url = st.text_input(
        "Ollama Endpoint",
        value=st.session_state.get("ollama_base_url", "http://localhost:11434"),
        help="Local Ollama REST server URL.",
    )
    st.session_state["ollama_base_url"] = ollama_url

    # Configured Model Tag
    model_input = st.text_input(
        "Configured Model Name",
        value=st.session_state.configured_model,
        placeholder="e.g., gemma-4 or local model tag",
        help="Enter the exact model tag available in your local Ollama instance.",
    )
    st.session_state.configured_model = model_input.strip()

    # Test Connection Button
    if st.button(
        "🔍 Test Ollama Connection", key="check_ollama_btn", use_container_width=True
    ):
        result = check_ollama_connection(ollama_url)
        st.session_state.ollama_status = result

    # Connection Status Indicator (Honest, Unchecked by Default)
    status_info = st.session_state.ollama_status
    if not status_info.get("checked", False):
        st.markdown(
            """
            <div class="status-pill status-untested">
                ⚪ Status: Not checked yet
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif status_info.get("connected", False):
        st.markdown(
            """
            <div class="status-pill status-online">
                🟢 Status: Connected to Ollama
            </div>
            """,
            unsafe_allow_html=True,
        )
        if status_info["models"]:
            st.caption(
                f"**Detected Models ({len(status_info['models'])}):** "
                + ", ".join(f"`{m}`" for m in status_info["models"][:3])
                + ("..." if len(status_info["models"]) > 3 else "")
            )
        else:
            st.caption(
                "Ollama is running, but no models found. Pull your model tag via CLI."
            )
    else:
        st.markdown(
            """
            <div class="status-pill status-offline">
                🔴 Status: Unreachable
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(
            "Ensure Ollama is running locally (`ollama serve`) before testing."
        )

    # Display configured model state
    if st.session_state.configured_model:
        st.caption(
            f"Active Model: **`{st.session_state.configured_model}`**"
        )
    else:
        st.caption("Active Model: *None configured* (Enter tag above)")

    st.divider()

    # 4. Project Information
    st.markdown(
        "<div style='font-size: 0.92rem; font-weight: 700; color: #0F172A; margin-bottom: 6px;'>ℹ️ Project Info</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="background:#FFFFFF; border:1.5px solid #CBD5E1; border-radius:10px; padding:10px 12px; font-size:0.8rem; color:#0F172A; line-height:1.45;">
            <strong style="color:#0F172A;">CampusBuddy v1.2</strong><br>
            <span style="color:#334155;">• AI-Powered College Survival Assistant</span><br>
            <span style="color:#334155;">• Hackathon Edition</span><br>
            <span style="color:#334155;">• Privacy-Focused: 100% Local Inference via Ollama</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# Main Dashboard Hero Header
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">CampusBuddy 🎓</div>
        <div class="hero-tagline">"Your AI companion for surviving and thriving in college."</div>
        <div class="hero-subtitle">From campus questions to college life advice, get help with your student journey.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Four Quick Action Prompt Cards: White Background, Purple Borders, Navy Text
# -----------------------------------------------------------------------------
st.markdown("### ⚡ Quick Survival Prompts")
st.caption(
    "Click any prompt below to receive actionable student guidance instantly."
)

col1, col2 = st.columns(2)

with col1:
    # Prompt Card 1
    st.markdown(
        """
        <div class="prompt-card">
            <div class="prompt-category">Orientation & Academics</div>
            <div class="prompt-text">Help me prepare for my first week.</div>
            <div class="prompt-desc">Master your class locations, syllabus breakdown, tech setup, and social rhythm.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "👉 Prepare for First Week",
        key="btn_card_1",
        use_container_width=True,
    ):
        handle_prompt_click("Help me prepare for my first week.")
        st.rerun()

    # Prompt Card 3
    st.markdown(
        """
        <div class="prompt-card">
            <div class="prompt-category">Hostel & Living Essentials</div>
            <div class="prompt-text">Give me a checklist for hostel essentials.</div>
            <div class="prompt-desc">Must-pack bedding, power strips, bathroom caddy, medicine pouch, and laundry gear.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "👉 Get Hostel Checklist",
        key="btn_card_3",
        use_container_width=True,
    ):
        handle_prompt_click("Give me a checklist for hostel essentials.")
        st.rerun()

with col2:
    # Prompt Card 2
    st.markdown(
        """
        <div class="prompt-card">
            <div class="prompt-category">Campus Clubs & Societies</div>
            <div class="prompt-text">How do I prepare for a club interview?</div>
            <div class="prompt-desc">Craft your 60-second pitch, prove reliability, and ask memorable questions.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "👉 Prepare for Club Interview",
        key="btn_card_2",
        use_container_width=True,
    ):
        handle_prompt_click("How do I prepare for a club interview?")
        st.rerun()

    # Prompt Card 4
    st.markdown(
        """
        <div class="prompt-card">
            <div class="prompt-category">Academics & Presentations</div>
            <div class="prompt-text">Help me plan my college presentation.</div>
            <div class="prompt-desc">Structure your hook, 3 core arguments, clean visual slides, and handle Q&A.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "👉 Plan My College Presentation",
        key="btn_card_4",
        use_container_width=True,
    ):
        handle_prompt_click("Help me plan my college presentation.")
        st.rerun()

st.divider()

# -----------------------------------------------------------------------------
# Active Feature Section Display (Based on Navigation)
# -----------------------------------------------------------------------------
current_page = st.session_state.current_page

# -----------------------------------------------------------------------------
# SECTION 1: AI Campus Assistant
# -----------------------------------------------------------------------------
if current_page == "🤖 AI Campus Assistant":
    st.subheader("🤖 AI Campus Assistant")
    st.markdown(
        "Ask any question about campus life, study tactics, roommate dynamics, or presentation planning."
    )

    # Input form for student question
    with st.form(key="student_ask_form", clear_on_submit=True):
        user_input = st.text_input(
            "Your Question or Challenge:",
            placeholder="e.g., How do I manage time between 5 classes and club activities?",
            value=st.session_state.active_query
            if st.session_state.active_query
            else "",
        )
        submit_button = st.form_submit_button(
            "Ask CampusBuddy 🚀", use_container_width=True
        )

        if submit_button and user_input.strip():
            clean_query = user_input.strip()
            st.session_state.active_query = ""

            # Check if this exact query was already recorded as the last question to prevent duplicates
            last_user_query = None
            for msg in reversed(st.session_state.chat_history):
                if msg.get("role") == "user":
                    last_user_query = msg.get("content", "").strip()
                    break

            if clean_query != last_user_query:
                # Generate answer
                response_text = answer_student_question(
                    query=clean_query,
                    model_tag=st.session_state.configured_model,
                    base_url=st.session_state.get(
                        "ollama_base_url", "http://localhost:11434"
                    ),
                )
                # Record in history
                st.session_state.chat_history.append(
                    {"role": "user", "content": clean_query}
                )
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": response_text}
                )

    # Clear chat option
    col_hist_title, col_hist_btn = st.columns([4, 1])
    with col_hist_title:
        st.markdown("#### Conversation")
    with col_hist_btn:
        if st.session_state.chat_history:
            if st.button("Clear Chat", key="clear_chat_btn"):
                st.session_state.chat_history = []
                st.session_state.active_query = ""
                st.rerun()

    # Render Conversation Messages
    if st.session_state.chat_history:
        for idx, msg in enumerate(st.session_state.chat_history):
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div style="background:#EFF6FF; border-left:4px solid #3B82F6; border-radius:10px; padding:12px 16px; margin-top:12px; margin-bottom:8px;">
                        <span style="font-weight:700; color:#1E40AF; font-size:0.85rem;">YOU ASKED:</span><br>
                        <span style="font-size:1.02rem; color:#0F172A; font-weight:600;">{msg['content']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                with st.container(border=True):
                    st.markdown(msg["content"])
    else:
        st.info(
            "👋 No questions asked yet! Select one of the quick prompt cards above or type your question in the box."
        )

# -----------------------------------------------------------------------------
# SECTION 2: Campus Guide (Campus Information with Clear DEMO DATA Labels)
# -----------------------------------------------------------------------------
elif current_page == "🏛️ Campus Guide":
    st.subheader("🏛️ Campus Information Guide")

    # Clear DEMO DATA Notice Banner
    st.markdown(
        """
        <div class="demo-banner">
            <strong>⚠️ DEMO DATA NOTICE:</strong> All facilities, directory contacts, and operating hours below are 
            <strong>demonstration templates</strong> designed to show how CampusBuddy organizes college resources. 
            Replace with your institution's verified administrative records.
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_facilities, tab_services, tab_faqs = st.tabs(
        [
            "🏢 Facilities & Hours",
            "📞 Campus Support Services",
            "❓ General FAQs",
        ]
    )

    # Facilities Tab
    with tab_facilities:
        st.markdown("#### Sample Campus Facilities")
        facilities = campus_data.get("facilities", [])
        for facility in facilities:
            with st.expander(
                f"📍 {facility.get('name')} — {facility.get('category')}"
            ):
                st.markdown(
                    "<span class='demo-badge'>DEMO DATA</span>",
                    unsafe_allow_html=True,
                )
                st.write(f"**Operating Hours:** {facility.get('hours')}")
                st.write("**Available Services:**")
                for s in facility.get("services", []):
                    st.markdown(f"- {s}")

    # Services Directory Tab
    with tab_services:
        st.markdown("#### Campus Support Directory")
        services = campus_data.get("sample_services_directory", [])
        for svc in services:
            st.markdown(
                f"""
                <div class="buddy-card">
                    <span class="demo-badge">DEMO DATA</span>
                    <h4 style="margin:4px 0 6px 0; color:#0F172A;">{svc.get('service_name')}</h4>
                    <p style="margin:0 0 6px 0; color:#475569; font-size:0.9rem;"><strong>Location:</strong> {svc.get('general_location')} | <strong>Hours:</strong> {svc.get('coverage')}</p>
                    <p style="margin:0; color:#6366F1; font-size:0.88rem;">ℹ️ {svc.get('contact_placeholder')}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # FAQs Tab
    with tab_faqs:
        st.markdown("#### Common College Guidelines & FAQs")
        faqs = campus_data.get("general_survival_faqs", [])
        for faq in faqs:
            with st.expander(f"❓ {faq.get('question')}"):
                st.markdown(
                    "<span class='demo-badge'>DEMO DATA</span>",
                    unsafe_allow_html=True,
                )
                st.write(faq.get("answer"))

# -----------------------------------------------------------------------------
# SECTION 3: Student Survival Toolkit
# -----------------------------------------------------------------------------
elif current_page == "🧰 Student Survival Toolkit":
    st.subheader("🧰 Student Survival Toolkit")
    st.markdown(
        "Interactive tools and checklists to make day-to-day college life manageable and stress-free."
    )

    toolkit_tab1, toolkit_tab2, toolkit_tab3, toolkit_tab4 = st.tabs(
        [
            "🎒 Hostel Essentials Checklist",
            "🎙️ Club Interview Playbook",
            "📊 Presentation Blueprint",
            "⏱️ 7-Day First Week Roadmap",
        ]
    )

    # 1. Hostel Essentials Checklist
    with toolkit_tab1:
        st.markdown("#### 🎒 Interactive Hostel & Dorm Packing Checklist")
        st.caption(
            "Check off items as you pack. Your progress updates dynamically."
        )

        total_items = len(st.session_state.hostel_checklist)
        checked_count = sum(
            1 for v in st.session_state.hostel_checklist.values() if v
        )
        progress_val = checked_count / total_items if total_items > 0 else 0.0

        st.progress(
            progress_val,
            text=f"Packing Progress: {checked_count} of {total_items} items packed ({int(progress_val * 100)}%)",
        )

        col_chk1, col_chk2 = st.columns(2)
        items_list = list(st.session_state.hostel_checklist.keys())
        mid = len(items_list) // 2

        with col_chk1:
            for item in items_list[:mid]:
                current_val = st.session_state.hostel_checklist[item]
                new_val = st.checkbox(item, value=current_val, key=f"chk_{item}")
                st.session_state.hostel_checklist[item] = new_val

        with col_chk2:
            for item in items_list[mid:]:
                current_val = st.session_state.hostel_checklist[item]
                new_val = st.checkbox(item, value=current_val, key=f"chk_{item}")
                st.session_state.hostel_checklist[item] = new_val

        if st.button("Reset Checklist", key="reset_chk_btn"):
            st.session_state.hostel_checklist = DEFAULT_CHECKLIST.copy()
            st.rerun()

    # 2. Club Interview Playbook
    with toolkit_tab2:
        st.markdown("#### 🎙️ Club & Society Selection Strategy")
        st.markdown(
            """
            <div class="buddy-card">
                <h4 style="color:#1E293B; margin-top:0;">1. The 60-Second "Why This Club?" Structure</h4>
                <p style="color:#475569; font-size:0.92rem;">
                    Don't give a generic bio. Use the 3-part framework:<br>
                    • <strong>Current Focus:</strong> "I'm a first-year studying Computer Science..."<br>
                    • <strong>Specific Resonance:</strong> "...and I followed your recent Hackathon and open-source bootcamp."<br>
                    • <strong>Tangible Contribution:</strong> "I want to help with technical workshop coordination and frontend design."
                </p>
            </div>

            <div class="buddy-card">
                <h4 style="color:#1E293B; margin-top:0;">2. Common Trap Questions & How to Win Them</h4>
                <p style="color:#475569; font-size:0.92rem;">
                    • <strong>"What if you have midterms during a club event?"</strong><br>
                    <em>Winning answer:</em> Show that you communicate early: "I block exam prep two weeks in advance and flag schedule conflicts to team leads early so tasks can be delegated."<br><br>
                    • <strong>"Why should we pick you over someone with more experience?"</strong><br>
                    <em>Winning answer:</em> Focus on grit: "Experience can be trained, but reliability and enthusiasm cannot. I show up consistently and finish what I start."
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 3. Presentation Blueprint
    with toolkit_tab3:
        st.markdown("#### 📊 High-Scoring College Presentation Blueprint")
        st.markdown(
            """
            <div class="buddy-card">
                <h4 style="color:#1E293B; margin-top:0;">The 5-Slide Presentation Architecture</h4>
                <ol style="color:#475569; font-size:0.92rem; line-height:1.6;">
                    <li><strong>Slide 1: The Hook (0-45 sec):</strong> An intriguing question, unexpected stat, or real-world dilemma.</li>
                    <li><strong>Slide 2: The Core Problem:</strong> Why current solutions fail or why this topic matters right now.</li>
                    <li><strong>Slide 3: Your Solution / Key Findings:</strong> Clear diagrams, bullet points (max 5), or key data points.</li>
                    <li><strong>Slide 4: Real-World Impact:</strong> Case study, benchmark results, or implementation challenges.</li>
                    <li><strong>Slide 5: Actionable Conclusion:</strong> One central takeaway you want your audience to remember.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 4. 7-Day First Week Roadmap
    with toolkit_tab4:
        st.markdown("#### ⏱️ 7-Day College First-Week Roadmap")
        days = [
            (
                "Days 1-2: Territory & Tech",
                "Locate your lecture halls, verify your ID card, test your Wi-Fi credentials, and explore library study areas.",
            ),
            (
                "Days 3-4: Syllabus Mastery",
                "Download all course syllabi, mark assignment dates in your calendar, and note professors' office hours.",
            ),
            (
                "Days 5-6: Social & Club Exploration",
                "Attend student club fairs, introduce yourself to two classmates per course, and find a consistent study spot.",
            ),
            (
                "Day 7: Weekly Review & Reset",
                "Organize digital course folders, prep class readings for the week ahead, and ensure your sleep schedule is stable.",
            ),
        ]
        for title, desc in days:
            st.markdown(
                f"""
                <div class="buddy-card" style="border-left: 4px solid #38BDF8;">
                    <strong style="color:#0F172A; font-size:1rem;">{title}</strong>
                    <p style="margin:4px 0 0 0; color:#475569; font-size:0.9rem;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
