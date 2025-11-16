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
    border-radius: 16px;
    margin-bottom: 20px;
}

/* History item */
.history-card {
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 8px;
    font-family: monospace;
    white-space: pre;
}

/* Button style - scoped to Streamlit buttons */
div.stButton > button {
    border-radius: 10px;
    padding: 10px 20px;
}

/* Keep operator & text colors readable; avoid global label rules */
.card .stText, .card .stNumberInput, .history-card, .card label, .card p {
    color: inherit;
}
</style>
"""

# Light theme — ensure main app content text is black (but keep sidebar white text)
light_css = """
<style>
/* Main app view container (only) - ensures labels & inputs are black in light theme */
div[data-testid="stAppViewContainer"], div[data-testid="stAppViewContainer"] * {
    color: #000 !important;
}

.stApp {
    background: #f0f2f6 !important;
    color: #000 !important;
}

/* LEFT SIDEBAR — dark background with white text */
section[data-testid="stSidebar"] {
    background: #1e1e1e !important;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Card visual for light mode */
.card {
    background: rgba(255,255,255,0.95);
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
}
.history-card {
    background: rgba(240, 240, 240, 0.95);
    border: 1px solid #dcdcdc;
}
div.stButton > button {
    background: linear-gradient(180deg,#4a90e2,#357ABD) !important;
    color: white !important;
}
</style>
"""

# Dark theme — ensure main app content text is white
dark_css = """
<style>
/* Main app view container (only) - ensures labels & inputs are white in dark theme */
div[data-testid="stAppViewContainer"], div[data-testid="stAppViewContainer"] * {
    color: #fff !important;
}

.stApp {
    background: linear-gradient(145deg, #0f0f0f, #1A1A1A) !important;
    color: #fff !important;
}

/* LEFT SIDEBAR — keep it dark with white text */
section[data-testid="stSidebar"] {
    background: #000 !important;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Card visual for dark mode */
.card {
    background: rgba(20,20,20,0.55);
    backdrop-filter: blur(6px);
    box-shadow: 0 5px 20px rgba(255,255,255,0.03);
}
.history-card {
    background: rgba(40, 40, 40, 0.6);
}
div.stButton > button {
    background: linear-gradient(135deg, #444, #222) !important;
    color: white !important;
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
            # limit exponent size to avoid accidental huge numbers
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
    # use number_input with explicit format to avoid odd display
    num1 = col1.number_input("First Number", value=0.0, format="%f")
    num2 = col2.number_input("Second Number", value=0.0, format="%f")

    # Use explicit Unicode plus/minus to avoid being interpreted as markdown list markers
    # \u002B = plus sign, \u2212 = minus sign (unicode minus)
    op_labels = [
        "\u002B (Add)",        # shows as + (Add)
        "\u2212 (Subtract)",   # shows as − (Subtract) (unicode minus)
        "× (Multiply)",
        "÷ (Divide)",
        "^ (Power)",
    ]

    op_label = st.radio(
        "Select Operation",
        op_labels,
        horizontal=True,
    )

    # Map back to the real operator characters for calculation and display
    op_map = {
        "\u002B (Add)": "+",
        "\u2212 (Subtract)": "-",  # map unicode minus back to ASCII minus for calc/history
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
    # Prepare a readable expression and result
    n1s = format_number(num1)
    n2s = format_number(num2)
    results = format_number(result) if not isinstance(result, str) or not result.startswith("Error") else result

    expr = f"{n1s} {op} {n2s} = {results}"

    # store timestamp + expression
    st.session_state.history.append(
        {"time": datetime.utcnow().isoformat() + "Z", "expr": expr}
    )

    # show immediate result (use st.success for clear message)
    if isinstance(result, str) and result.startswith("Error"):
        st.error(f"{result}")
    else:
        st.success(f"Result: {results}")

# -----------------------------------------------------------
# HISTORY DISPLAY
# -----------------------------------------------------------
if st.session_state.history:
    st.markdown("### 📝 Calculation History")
    # show newest first
    for entry in reversed(st.session_state.history):
        # escape to ensure operators like + and - are rendered literally and not interpreted
        safe = html.escape(entry["expr"])
        card_html = f"<div class='history-card'><code>{safe}</code></div>"
        st.markdown(card_html, unsafe_allow_html=True)

# -----------------------------------------------------------
# CLEAR HISTORY
# -----------------------------------------------------------
if st.button("Clear History"):
    st.session_state.history = []
    st.info("History cleared successfully!")


