import streamlit as st

st.set_page_config(
    page_title="🖤 Premium Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.sidebar.title("Settings")
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp {background-color: #1e1e1e; color: white;}
        .stButton>button {background-color: #444444; color: white;}
        .stTextInput>div>input {background-color: #333333; color: white;}
        </style>
        """,
        unsafe_allow_html=True
    )

st.title("🧮 Premium Streamlit Calculator")
st.markdown("Interactive calculator with buttons, dark/light mode, and calculation history.")

if "history" not in st.session_state:
    st.session_state.history = []

def calculate(n1, n2, op):
    try:
        n1 = float(n1)
        n2 = float(n2)
        if op == "+": return n1 + n2
        if op == "-": return n1 - n2
        if op == "×": return n1 * n2
        if op == "÷":
            return n1 / n2 if n2 != 0 else "Error: Division by 0"
        if op == "^": return n1 ** n2
    except:
        return "Error"

col1, col2 = st.columns(2)
num1 = col1.text_input("First Number", "")
num2 = col2.text_input("Second Number", "")

op = st.radio("Select Operation", ["+", "-", "×", "÷", "^"], horizontal=True)

if st.button("Calculate"):
    result = calculate(num1, num2, op)
    st.session_state.history.append(f"{num1} {op} {num2} = {result}")
    st.success(f"Result: {result}")

if st.session_state.history:
    st.markdown("### 📝 Calculation History")
    for item in reversed(st.session_state.history):
        st.write(item)

if st.button("Clear History"):
    st.session_state.history = []
    st.experimental_rerun()

