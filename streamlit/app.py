import pandas as pd
import requests
import streamlit as st

# App Title
st.set_page_config(page_title="calTax")
st.title("calTax - Income Tax Calculator")

# Sidebar for Input Parameters
st.sidebar.header("Input")
gross_income = st.sidebar.number_input(
    "Gross Annual Income (₹)",
    value=1200000.0,
    min_value=0.0,
    step=50000.0,
    help="Total gross annual income before deductions",
)
is_salaried = st.sidebar.checkbox(
    "Are you a salaried individual?",
    value=True,
    help="Salaried individuals are eligible for standard deduction",
)
age = st.sidebar.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=22,
)
total_deductions = st.sidebar.number_input(
    "Total Deductions (₹)",
    min_value=0.0,
    value=10000.0,
    step=10000.0,
    help="Total eligible deductions",
)
mode = st.sidebar.selectbox(
    "Calculation Mode",
    options=["compare", "new", "old"],
    help="Choose whether to compare both regimes or view a single regime breakdown",
)


def format_regime_details(details: dict) -> pd.DataFrame:
    """Format regime dictionary into DataFrame."""
    formatted_data = {
        "Section": [
            "Taxable Income",
            "Standard Deduction",
            "Total Deductions",
            "Base Tax",
            "Cess (4%)",
            "Total Tax Payable",
        ],
        "Amount (₹)": [
            f"₹{details.get('taxable_income', 0):,.2f}",
            f"₹{details.get('standard_deduction', 0):,.2f}",
            f"₹{details.get('total_deductions', 0):,.2f}",
            f"₹{details.get('base_tax', 0):,.2f}",
            f"₹{details.get('cess', 0):,.2f}",
            f"₹{details.get('total_tax', 0):,.2f}",
        ],
    }
    return pd.DataFrame(formatted_data)


# Main Interface Tabs
tab_calc, tab_history = st.tabs(["Income Tax Calculator", "Calculation History"])

with tab_calc:
    if st.button("Calculate Tax", type="primary"):
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
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                st.subheader("Calculation Result")

                # Compare Mode
                if mode == "compare":

                    # Recommendation summary card
                    if result.get('message'):
                        st.success(f"**Recommendation**: {result.get('message')}")

                    # Metrics summary
                    st.metric("Gross Income", f"₹{result.get('gross_income', 0):,.2f}")
                    m1, m2 = st.columns(2)
                    m1.metric("Recommended Regime", result.get("recommended_regime", "N/A"))
                    m2.metric("Tax Savings", f"₹{result.get('tax_savings', 0):,.2f}")

                    st.markdown("---")

                    # Side-by-Side Comparison Tables
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Old Tax Regime")
                        old_df = format_regime_details(result.get("old_regime"))
                        st.table(old_df)

                    with col2:
                        st.subheader("New Tax Regime")
                        new_df = format_regime_details(result.get("new_regime"))
                        st.table(new_df)

                # Single Regime Mode ('new' or 'old')
                else:
                    regime_name = result.get("regime")
                    st.info(f"Showing breakdown for **{regime_name}**")
                    st.metric("Gross Income", f"₹{result.get('gross_income', 0):,.2f}")
                    
                    details_df = format_regime_details(result.get("details"))
                    st.table(details_df)

            else:
                error_detail = response.json().get("detail", response.text)
                st.error(f"Error ({response.status_code}): {error_detail}")

        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")

with tab_history:
    st.subheader("Saved Calculation History")
    if st.button("Fetch History"):
        try:
            history_res = requests.get("http://localhost:8000/api/v1/tax/history")
            if history_res.status_code == 200:
                history_data = history_res.json()
                if history_data:
                    st.dataframe(history_data)
                else:
                    st.info("No tax history records found in database yet.")
            else:
                st.error(f"Failed to fetch history ({history_res.status_code})")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")