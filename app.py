import streamlit as st

st.title("🧮 Streamlit Calculator App")
st.write("Perform basic arithmetic operations.")


num1 = st.number_input("Enter the first number", value=0.0)
num2 = st.number_input("Enter the second number", value=0.0)


operation = st.selectbox(
    "Select an operation",
    ("Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)", "Exponentiation (^)")
)

if st.button("Calculate"):
    if operation == "Addition (+)":
        result = num1 + num2
    elif operation == "Subtraction (-)":
        result = num1 - num2
    elif operation == "Multiplication (×)":
        result = num1 * num2
    elif operation == "Division (÷)":
        if num2 != 0:
            result = num1 / num2
        else:
            st.error("❌ Division by zero is not allowed.")
            result = None
    elif operation == "Exponentiation (^)":
        result = num1 ** num2

    if result is not None:
        st.success(f"Result: {result}")
