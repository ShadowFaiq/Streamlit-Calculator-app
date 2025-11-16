import streamlit as st

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(
    page_title="🖤 Premium Calculator",
    page_icon="🧮",
    layout="centered"
)

# -----------------------------------------------------------
# SIDEBAR — THEME SELECTION
# -----------------------------------------------------------
st.sidebar.title("Settings")
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])

# -----------------------------------------------------------
# PREMIUM + FIXED CSS (Light & Dark)
# -----------------------------------------------------------
light_css = """
<style>

.stApp {
    background: #f0f2f6 !important;
    color: #000 !important;
}

h1, h2, h3, h4, h5, h6, label, p, span {
    color: #000 !important;
}

.card {
    background: rgba(255,255,255,0.8);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.history-card {
    padding: 12px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    border: 1px solid #ddd;
    margin-bottom: 8px;
}

div.stButton > button {
    background: #4a90e2 !important;
    color: white !important;
    border-radius: 10px;
    padding: 10px 20px;
}

</style>
"""

dark_css = """
<style>

.stApp {
    background: linear-gradient(145deg, #0f0f0f, #1A1A1A) !important;
    color: white !important;
}

h1, h2, h3, h4, h5, h6, label, p, span {
    color: #fff !important;
}

.card {
    background: rgba(20,20,20,0.55);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 5px 20px rgba(255,255,255,0.04);
    margin-bottom: 20px;
}

.history-card {
    padding: 12px;
    background: rgba(40, 40, 40, 0.6);
    border-radius: 12px;
    margin-bottom: 8px;
}

div.stButton > button {
    background: linear-gradient(135deg, #444, #222) !important;
    color: white !important;
    border-radius: 10px;
    padding: 10px 20px;
}

</style>
"""

# Apply correct theme
if theme == "Light":
    st.markdown(light_css, unsafe_allow_html=True)
else:
    st.markdown(dark_css, unsafe_allow_html=True)

# -----------------------------------------------------------
# SESSION STATE
# -----------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------------------------------------
# CALCULATION FUNCTION
# -----------------------------------------------------------
def calculate(n1, n2, op):
    if op == "+": return n1 + n2
    if op == "-": return n1 - n2
    if op == "×": return n1 * n2
    if op == "÷": return n2 and n1 / n2 or "Error: Division by 0"
    if op == "^": return n1 ** n2
    return "Error"

# -----------------------------------------------------------
# UI – INPUT AREA (Glass Card)
# -----------------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.title("🧮 Premium Streamlit Calculator")
st.markdown("Maths ?! aint even a problem ")

col1, col2 = st.columns(2)

# Number inputs show + / – buttons automatically (no CSS needed)
num1 = col1.number_input("First Number", value=0.0)
num2 = col2.number_input("Second Number", value=0.0)

op = st.radio("Select Operation", ["+", "-", "×", "÷", "^"], horizontal=True)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------
# CALCULATE
# -----------------------------------------------------------
if st.button("Calculate"):
    result = calculate(num1, num2, op)
    st.session_state.history.append(f"{num1} {op} {num2} = {result}")
    st.success(f"Result: {result}")

# -----------------------------------------------------------
# HISTORY SECTION
# -----------------------------------------------------------
if st.session_state.history:
    st.markdown("### 📝 Calculation History")

    for item in reversed(st.session_state.history):
        st.markdown(f"<div class='history-card'>{item}</div>", unsafe_allow_html=True)

# -----------------------------------------------------------
# CLEAR HISTORY
# -----------------------------------------------------------
if st.button("Clear History"):
    st.session_state.history = []
    st.info("History cleared successfully!")


