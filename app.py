import streamlit as st

# Constants for theme CSS
LIGHT_CSS = """
<style>
.stApp {
    background: #f0f2f6 !important;
    color: #000 !important;
}
section[data-testid="stSidebar"] {
    background: #1e1e1e !important;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
.card {
    background: rgba(255,255,255,0.85);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
label, h1, h2, h3, h4, p, span {
    color: black !important;
}
.history-card {
    padding: 12px;
    background: rgba(240, 240, 240, 0.95);
    border-radius: 12px;
    border: 1px solid #ccc;
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

DARK_CSS = """
<style>
.stApp {
    background: linear-gradient(145deg, #0f0f0f, #1A1A1A) !important;
    color: white !important;
}
section[data-testid="stSidebar"] {
    background: #000 !important;
}
section[data-testid="stSidebar"] * {
    color: white !important;
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

# Function to set theme CSS
def set_theme_css(theme: str):
    if theme == "Light":
        st.markdown(LIGHT_CSS, unsafe_allow_html=True)
    else:
        st.markdown(DARK_CSS, unsafe_allow_html=True)

# Calculation logic
def calculate(n1, n2, op):
    try:
        if op == "+":
            return n1 + n2
        elif op == "-":
            return n1 - n2
        elif op == "×":
            return n1 * n2
        elif op == "÷":
            return n1 / n2 if n2 != 0 else "Error: Division by 0"
        elif op == "^":
            return n1 ** n2
        else:
            return "Invalid operation"
    except Exception as e:
        return f"Error: {e}"

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar theme selection
st.sidebar.title("Settings")
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])
set_theme_css(theme)

# Main UI
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title("🧮 Premium Streamlit Calculator")
st.markdown("Clean, readable, and aesthetic calculator with dark/light mode.")

# Input columns
col1, col2 = st.columns(2)
num1 = col1.number_input("First Number", value=0.0)
num2 = col2.number_input("Second Number", value=0.0)

# Operation selection
operation_labels = ["+ (Add)", "- (Subtract)", "× (Multiply)", "÷ (Divide)", "^ (Power)"]
operation_map = {
    "+ (Add)": "+",
    "- (Subtract)": "-",
    "× (Multiply)": "×",
    "÷ (Divide)": "÷",
    "^ (Power)": "^"
}
op_label = st.radio("Select Operation", operation_labels, horizontal=True)
op = operation_map[op_label]

st.markdown("</div>", unsafe_allow_html=True)

# Calculate button
if st.button("Calculate"):
    result = calculate(num1, num2, op)
    st.session_state.history.append(f"{num1} {op} {num2} = {result}")
    st.success(f"Result: {result}")

# Show history
if st.session_state.history:
    st.markdown("### 📝 Calculation History")
    for item in reversed(st.session_state.history):
        st.markdown(f"<div class='history-card'>{item}</div>", unsafe_allow_html=True)

# Clear history button
if st.button("Clear History"):
    st.session_state.history = []
    st.info("History cleared successfully!")



