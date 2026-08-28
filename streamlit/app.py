import requests
import streamlit as st

# App Title
st.title("calTax - Income Tax Calculator")

# Input Fields
gross_income = st.number_input("Gross Annual Income (₹)", min_value=0.0, value=1200000.0, step=50000.0)
is_salaried = st.checkbox("Are you a salaried individual?", value=True)
age = st.number_input("Age", min_value=18, max_value=100, value=22)
total_deductions = st.number_input("Total Deductions (₹)", min_value=0.0, value=10000.0, step=10000.0)
mode = st.selectbox("Calculation Mode", options=["compare", "new", "old"])

# Calculate Button & API Call
if st.button("Calculate Tax"):
    payload = {
        "gross_income": gross_income,
        "is_salaried": is_salaried,
        "age": age,
        "total_deductions": total_deductions,
    }

    try:
        response = requests.post(
            "http://localhost:8000/api/v1/tax/calculate",
            params={"mode": mode},
            json=payload,
        )

        if response.status_code == 200:
            result = response.json()
            st.subheader("Calculation Result:")
            st.dataframe(result)
        else:
            st.error(f"Error from API: {response.text}")

    except Exception as e:
        st.error(f"Some error occured - {e}")


if st.button("View Tax History"):
    history_res = requests.get("http://localhost:8000/api/v1/tax/history")
    st.dataframe(history_res.json())
