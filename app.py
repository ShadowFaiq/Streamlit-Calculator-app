import streamlit as st

# Page config
st.set_page_config(
    page_title="🖤 Premium Calculator",
    page_icon="🧮",
    layout="centered"
)

# Sidebar theme selection
st.sidebar.title("Settings")
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])

# Apply safe CSS for dark mode
if theme == "Dark":
    st.markdown(
        """
        <style>
        /* App background and text */
        .stApp {background-color: #1e1e1e; color: white;}
        /* Buttons */
        div.stButton > button {background-color: #444444; color: white; border-radius: 8px;}
        /* Text inputs */
        input[type="text"] {background-color: #333333; color: white; border-radius: 4px;}
        /* Radio buttons */
        div[role="radiogroup"] > label {color: white;}
        </style>
        """,
        unsafe_allow_html=True
    )

# Title
st.title("🧮 Premium Streamlit Calculator")
st.markdown("Interactive calculator with calculation history and dark/light mode.")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Calculation function
def calculate(n1, n2, op):
    try:
        n1 = float(n1)
        n2 = float(n2)
        if op == "+": return n1 + n2
        if op == "-": return n1 - n2
        if op == "×": return n1 * n2
        if op == "÷": return n1 / n2 if n2 != 0 else "Error: Division by 0"
        if op == "^": return n1 ** n2
    except:
        return "Error"

# Input columns
col1, col2 = st.columns(2)
num1 = col1.text_input("First Number", "")
num2 = col2.text_input("Second Number", "")

# Operation
op = st.radio("Select Operation", ["+", "-", "×", "÷", "^"], horizontal=True)

# Calculate button
if st.button("Calculate"):
    result = calculate(num1, num2, op)
    st.session_state.history.append(f"{num1} {op} {num2} = {result}")
    st.success(f"Result: {result}")

# Show calculation history
if st.session_state.history:
    st.markdown("### 📝 Calculation History")
    for item in reversed(st.session_state.history):
        st.write(item)

# Clear history button
if st.button("Clear History"):
    st.session_state.history = []
    st.experimental_rerun()
