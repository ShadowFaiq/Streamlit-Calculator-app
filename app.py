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
# CSS — scoped and theme-aware
# -----------------------------------------------------------
base_css = """
<style>
.card {
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.history-card {
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 8px;
    font-family: monospace;
    white-space: pre;
}

div.stButton > button {
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}

.history-card code {
    color: inherit;
    background: transparent;
}
</style>
"""

light_css = """
<style>
/* Main app content */
div[data-testid="stAppViewContainer"], div[data-testid="stAppViewContainer"] * {
    color: #000 !important;
}

.stApp {
    background: #f0f2f6 !important;
    color: #000 !important;
}

/* Sidebar: dark background, white text */
section[data-testid="stSidebar"] {
    background: #1e1e1e !important;
}
section[data-testid="stSidebar"] * {
    color: #fff !important;
    fill: #fff !important;
}

/* Inputs in main app */
div[data-testid="stAppViewContainer"] input {
    background: white !important;
    color: black !important;
    border: 1px solid #ccc !important;
}

/* Button */
div[data-testid="stAppViewContainer"] div.stButton > button {
    background: linear-gradient(180deg,#4a90e2,#357ABD) !important;
    color: white !important;
}
</style>
"""

dark_css = """
<style>
/* Main app (dark) */
div[data-testid="stAppViewContainer"], div[data-testid="stAppViewContainer"] * {
    color: #fff !important;
}

.stApp {
    background: linear-gradient(145deg, #0f0f0f, #1A1A1A) !important;
    color: #fff !important;
}

/* Sidebar text forced to white */
section[data-testid="stSidebar"] {
    background: #000 !important;
}
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] svg,
section[data-testid="stSidebar"] input {
    color: #fff !important;
    fill: #fff !important;
}

/* Inputs dark */
div[data-testid="stAppViewContainer"] input {
    background: rgba(30,30,30,0.9) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

/* Button */
div[data-testid="stAppViewContainer"] div.stButton > button {
    background: linear-gradient(135deg, #444, #222) !important;
    color: white !important;
}
</style>
"""

st.markdown(base_css, unsafe_allow_html=True)
st.markdown(light_css if theme == "Light" else dark_css, unsafe_allow_html=True)

# -----------------------------------------------------------
# SESSION STATE
# -----------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------------------------------------
# UTILITIES
# -----------------------------------------------------------
def format_number(n):
    if isinstance(n, float) and n.is_integer():
        return str(int(n))
    return str(n)

def calculate(n1, n2, op):
    try:
        if op == "+": return n1 + n2
        if op == "-": return n1 - n2
        if op == "×": return n1 * n2
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
# UI — INPUT AREA
# -----------------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title("🧮 Here's your god dayumn Calculator")
st.markdown("Math aint even that difficult twin !")

with st.form("calc_form"):
    col1, col2 = st.columns(2)
    num1 = col1.number_input("First Number", value=0.0, format="%f")
    num2 = col2.number_input("Second Number", value=0.0, format="%f")

    # FIX: Display + and - properly (no invisible Unicode hacks)
    op_label = st.radio(
        "Select Operation",
        ["+ (Add)", "- (Subtract)", "× (Multiply)", "÷ (Divide)", "^ (Power)"],
        horizontal=True,
    )

    op = {
        "+ (Add)": "+",
        "- (Subtract)": "-",
        "× (Multiply)": "×",
        "÷ (Divide)": "÷",
        "^ (Power)": "^",
    }[op_label]

    submit = st.form_submit_button("Calculate")

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------
# CALCULATE
# -----------------------------------------------------------
if submit:
    result = calculate(num1, num2, op)

    # Build expression safely (escape any user-visible text to avoid HTML injection)
    n1s = format_number(num1)
    n2s = format_number(num2)
    results = format_number(result) if not (isinstance(result, str) and result.startswith("Error")) else str(result)
    expr_raw = f"{n1s} {op} {n2s} = {results}"

    # store escaped expression to avoid accidental HTML rendering later
    expr_safe = html.escape(expr_raw)
    st.session_state.history.append({"time": datetime.utcnow().isoformat() + "Z", "expr": expr_safe})

    if isinstance(result, str) and result.startswith("Error"):
        st.error(result)
    else:
        st.success(f"Result: {result}")

# -----------------------------------------------------------
# HISTORY
# -----------------------------------------------------------
if st.session_state.history:
    st.markdown("### 📝 Calculation History")
    for entry in reversed(st.session_state.history):
        # entry["expr"] is already escaped when stored; render inside code block
        st.markdown(f"<div class='history-card'><code>{entry['expr']}</code></div>", unsafe_allow_html=True)

# -----------------------------------------------------------
# CLEAR HISTORY
# -----------------------------------------------------------
if st.button("Clear History"):
    st.session_state.history = []
    st.info("History cleared successfully!")
