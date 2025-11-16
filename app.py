import html
from datetime import datetime

import streamlit as st

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(
    page_title="🖤 Premium Calculator",
    page_icon="🧮",
    layout="centered",
)

# -----------------------------------------------------------
# SIDEBAR — THEME SELECTION
# -----------------------------------------------------------
st.sidebar.title("Settings")
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])

# -----------------------------------------------------------
# CSS — scoped, theme-aware fixes
# -----------------------------------------------------------
base_css = """
<style>
/* Card / container */
.card {
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}

/* History item */
.history-card {
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 8px;
    font-family: monospace;
    white-space: pre;
}

/* Button style - scoped to Streamlit buttons */
div.stButton > button {
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    cursor: pointer;
}

/* Ensure code/history uses readable monospace */
.history-card code {
    color: inherit;
    background: transparent;
    border: none;
    padding: 0;
}
</style>
"""

# Light theme — ensure main app content text is black and inputs are white,
# and make sure the Calculate button text is white and visible
light_css = """
<style>
/* Main app view container only (not sidebar) */
div[data-testid="stAppViewContainer"], div[data-testid="stAppViewContainer"] * {
    color: #000 !important;
}

/* App background */
.stApp {
    background: #f0f2f6 !important;
    color: #000 !important;
}

/* Sidebar: dark background with white text */
section[data-testid="stSidebar"] {
    background: #1e1e1e !important;
}
/* Force all text/icons/inputs in sidebar to be white */
section[data-testid="stSidebar"] * {
    color: #fff !important;
    fill: #fff !important;
}
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] button,
section[data-testid="stSidebar"] select,
section[data-testid="stSidebar"] textarea {
    color: #fff !important;
    background: transparent !important;
    border-color: rgba(255,255,255,0.06) !important;
}

/* Inputs (number/text) in main app: white background, black text */
div[data-testid="stAppViewContainer"] input[type="number"],
div[data-testid="stAppViewContainer"] input[type="text"],
div[data-testid="stAppViewContainer"] .stNumberInput input,
div[data-testid="stAppViewContainer"] .stTextInput input {
    background: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #cfcfcf !important;
    border-radius: 6px !important;
}

/* Radio labels and form labels (main area) */
div[data-testid="stAppViewContainer"] label,
div[data-testid="stAppViewContainer"] .stRadio, 
div[data-testid="stAppViewContainer"] .stRadio * {
    color: #000 !important;
}

/* Make the calculate button clearly visible in light mode, ensure text is white */
div[data-testid="stAppViewContainer"] div.stButton > button {
    background: linear-gradient(180deg,#4a90e2,#357ABD) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 4px 10px rgba(53,122,189,0.18) !important;
}

/* Ensure nested spans/svg inside buttons inherit color */
div[data-testid="stAppViewContainer"] div.stButton > button span,
div[data-testid="stAppViewContainer"] div.stButton > button svg {
    color: inherit !important;
    fill: inherit !important;
}
</style>
"""

# Dark theme — ensure main app content text is white and sidebar stays white-on-dark.
dark_css = """
<style>
/* Main app view container only (not sidebar) */
div[data-testid="stAppViewContainer"], div[data-testid="stAppViewContainer"] * {
    color: #fff !important;
}

.stApp {
    background: linear-gradient(145deg, #0f0f0f, #1A1A1A) !important;
    color: #fff !important;
}

/* Sidebar stays dark with white text: force all nested elements to white,
   including inputs, spans, svg fills and placeholders. This targets more
   internal Streamlit generated elements so text won't remain black. */
section[data-testid="stSidebar"] {
    background: #000 !important;
}
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] svg,
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] button,
section[data-testid="stSidebar"] select,
section[data-testid="stSidebar"] textarea {
    color: #fff !important;
    fill: #fff !important;
    border-color: rgba(255,255,255,0.06) !important;
    background: transparent !important;
}

/* Specifically ensure radio groups in sidebar are white */
section[data-testid="stSidebar"] div[role="radiogroup"] * {
    color: #fff !important;
}

/* Inputs (number/text) in main app: dark background, white text */
div[data-testid="stAppViewContainer"] input[type="number"],
div[data-testid="stAppViewContainer"] input[type="text"],
div[data-testid="stAppViewContainer"] .stNumberInput input,
div[data-testid="stAppViewContainer"] .stTextInput input {
    background: rgba(30,30,30,0.9) !important;
    color: #fff !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 6px !important;
}

/* Radio labels and form labels (main area) */
div[data-testid="stAppViewContainer"] label,
div[data-testid="stAppViewContainer"] .stRadio, 
div[data-testid="stAppViewContainer"] .stRadio * {
    color: #fff !important;
}

/* Button style for dark theme (ensure text visible) */
div[data-testid="stAppViewContainer"] div.stButton > button {
    background: linear-gradient(135deg, #444, #222) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 3px 8px rgba(0,0,0,0.4) !important;
}
div[data-testid="stAppViewContainer"] div.stButton > button span,
div[data-testid="stAppViewContainer"] div.stButton > button svg {
    color: inherit !important;
    fill: inherit !important;
}
</style>
"""

# Inject CSS
st.markdown(base_css, unsafe_allow_html=True)
if theme == "Light":
    st.markdown(light_css, unsafe_allow_html=True)
else:
    st.markdown(dark_css, unsafe_allow_html=True)

# -----------------------------------------------------------
# SESSION STATE — history as list of dicts
# -----------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------------------------------------
# UTILITIES
# -----------------------------------------------------------
def format_number(n):
    """Format floats to avoid showing .0 for integers."""
    try:
        if isinstance(n, float) and n.is_integer():
            return str(int(n))
        return str(n)
    except Exception:
        return str(n)


def calculate(n1, n2, op):
    """Perform calculation with clear error handling."""
    try:
        if op == "+":
            return n1 + n2
        if op == "-":
            return n1 - n2
        if op == "×":
            return n1 * n2
        if op == "÷":
            if n2 == 0:
                return "Error: Division by 0"
            return n1 / n2
        if op == "^":
            if abs(n2) > 1000:
                return "Error: Exponent too large"
            return n1 ** n2
        return "Error: Unknown operator"
    except Exception as e:
        return f"Error: {e}"


# -----------------------------------------------------------
# UI — INPUT AREA (use a form to avoid accidental triggers)
# -----------------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title("🧮 Premium Streamlit Calculator")
st.markdown("Clean, readable and aesthetic calculator with dark/light mode.")

with st.form("calc_form"):
    col1, col2 = st.columns(2)
    # use number_input with explicit format to avoid odd display and ensure text color applies
    num1 = col1.number_input("First Number", value=0.0, format="%f")
    num2 = col2.number_input("Second Number", value=0.0, format="%f")

    # Zero-width-space trick for reliable + / - rendering but map back to ASCII +/- for calc/history
    ZWSP = "\u200B"
    op_labels = [
        ZWSP + "+ (Add)",
        ZWSP + "- (Subtract)",
        "× (Multiply)",
        "÷ (Divide)",
        "^ (Power)",
    ]

    op_label = st.radio(
        "Select Operation",
        op_labels,
        horizontal=True,
    )

    # Map back to real operator characters for calculation and history
    op_map = {
        ZWSP + "+ (Add)": "+",
        ZWSP + "- (Subtract)": "-",
        "× (Multiply)": "×",
        "÷ (Divide)": "÷",
        "^ (Power)": "^",
    }
    op = op_map.get(op_label, "+")

    submit = st.form_submit_button("Calculate")
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------
# CALCULATE — when the form is submitted
# -----------------------------------------------------------
if submit:
    result = calculate(num1, num2, op)
    n1s = format_number(num1)
    n2s = format_number(num2)
    results = format_number(result) if not isinstance(result, str) or not result.startswith("Error") else result
    expr = f"{n1s} {op} {n2s} = {results}"
    st.session_state.history.append(
        {"time": datetime.utcnow().isoformat() + "Z", "expr": expr}
    )

    if isinstance(result, str) and result.startswith("Error"):
        st.error(f"{result}")
    else:
        st.success(f"Result: {results}")

# -----------------------------------------------------------
# HISTORY DISPLAY
# -----------------------------------------------------------
if st.session_state.history:
    st.markdown("### 📝 Calculation History")
    for entry in reversed(st.session_state.history):
        safe = html.escape(entry["expr"])
        card_html = f"<div class='history-card'><code>{safe}</code></div>"
        st.markdown(card_html, unsafe_allow_html=True)

# -----------------------------------------------------------
# CLEAR HISTORY
# -----------------------------------------------------------
if st.button("Clear History"):
    st.session_state.history = []
    st.info("History cleared successfully!")
