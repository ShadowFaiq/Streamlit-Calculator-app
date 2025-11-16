import streamlit as st

st.set_page_config(
    page_title="🖤 Premium Calculator",
    page_icon="🧮",
    layout="centered"
)

st.sidebar.title("Settings")
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])

base_css = """
<style>

.stApp {
    background: linear-gradient(145deg, #e6e6e6, #ffffff);
    padding: 20px;
}

[data-testid="stSidebar"] {
    backdrop-filter: blur(12px);
}

/* Card for inputs */
.card {
    background: rgba(255, 255, 255, 0.4);
    padding: 20px;
    border-radius: 16px;
    backdrop-filter: blur(15px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.10);
    margin-bottom: 20px;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #4a90e2, #357ABD);
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
    transition: 0.2s;
}
div.stButton > button:hover {
    transform: scale(1.03);
}

/* History card */
.history-card {
    padding: 12px;
    background: rgba(255, 255, 255, 0.45);
    border-radius: 12px;
    backdrop-filter: blur(12px);
    margin-bottom: 8px;
    font-size: 16px;
}

</style>
"""

dark_css = """
<style>

.stApp {
    background: linear-gradient(145deg, #0f0f0f, #1A1A1A);
    color: white;
}

.card {
    background: rgba(25, 25, 25, 0.5);
    box-shadow: 0 8px 20px rgba(255,255,255,0.03);
}

.history-card {
    background: rgba(40, 40, 40, 0.5);
}

/* Inputs */
input, .stNumberInput input {
    background-color: #222 !important;
    color: white !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #444, #222);
    color: white;
}

</style>
"""

st.markdown(base_css, unsafe_allow_html=True)
if theme == "Dark":
    st.markdown(dark_css, unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

def calculate(n1, n2, op):
    try:
        if op == "+": return n1 + n2
        if op == "-": return n1 - n2
        if op == "×": return n1 * n2
        if op == "÷": return n1 / n2 if n2 != 0 else "Error: Division by 0"
        if op == "^": return n1 ** n2
    except:
        return "Error"

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title("🧮 Premium Streamlit Calculator")
st.markdown("Aesthetic calculator with history, animations, and dark/light modes.")

col1, col2 = st.columns(2)

num1 = col1.number_input("First Number", value=0.0, step=1.0)
num2 = col2.number_input("Second Number", value=0.0, step=1.0)

op = st.radio("Select Operation", ["+", "-", "×", "÷", "^"], horizontal=True)

st.markdown("</div>", unsafe_allow_html=True)

if st.button("Calculate"):
    result = calculate(num1, num2, op)
    st.session_state.history.append(f"{num1} {op} {num2} = {result}")
    st.success(f"Result: {result}")

if st.session_state.history:
    st.markdown("### 📝 Calculation History")
    for item in reversed(st.session_state.history):
        st.markdown(f"<div class='history-card'>{item}</div>", unsafe_allow_html=True)

if st.button("Clear History"):
    st.session_state.history = []
    st.info("History cleared! Refresh page to update.")

