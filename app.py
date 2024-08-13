import streamlit as st
import pandas as pd

# Define tax brackets for different years with concrete upper limits
TAX_BRACKETS = {
    "2024-25": [
        (0, 600000, 0.0),        # No tax for income up to 600,000
        (600001, 1200000, 0.05), # 5% tax on income between 600,001 and 1,200,000
        (1200001, 2400000, 0.1), # 10% tax on income between 1,200,001 and 2,400,000
        (2400001, 3000000, 0.15), # 15% tax on income between 2,400,001 and 3,000,000
        (3000001, float('inf'), 0.2)  # 20% tax on income above 3,000,000
    ],
    "2025-26": [
        (0, 700000, 0.0),        # Example updated brackets
        (700001, 1300000, 0.05),
        (1300001, 2500000, 0.1),
        (2500001, 3500000, 0.15),
        (3500001, float('inf'), 0.2)
    ]
    # Add more years as needed
}

def calculate_tax(income, brackets):
    tax = 0
    for lower, upper, rate in brackets:
        if income > lower:
            taxable_income = min(income, upper) - lower
            tax += taxable_income * rate
    return tax

# Streamlit app UI
st.title("Income Tax Calculator for Salaried Class")

# Sidebar for year selection
st.sidebar.header("Select Financial Year")
year = st.sidebar.selectbox("Select the financial year:", options=list(TAX_BRACKETS.keys()))
brackets = TAX_BRACKETS[year]

# Display tax slabs for selected year
st.subheader(f"Tax Slabs for {year}")
tax_slab_df = pd.DataFrame(brackets, columns=['Lower Bound', 'Upper Bound', 'Rate'])
tax_slab_df['Rate (%)'] = tax_slab_df['Rate'] * 100
tax_slab_df['Lower Bound (PKR)'] = tax_slab_df['Lower Bound'].apply(lambda x: f"{x:,.0f}")
tax_slab_df['Upper Bound (PKR)'] = tax_slab_df['Upper Bound'].apply(lambda x: f"{x:,.0f}")
tax_slab_df['Rate (%)'] = tax_slab_df['Rate (%)'].apply(lambda x: f"{x:.0f}%")

# Set 'Upper Bound' for last slab to a very high number if using 'inf'
tax_slab_df['Upper Bound (PKR)'] = tax_slab_df.apply(
    lambda row: f"{row['Upper Bound (PKR)']}" if row['Upper Bound'] < float('inf') else "Above",
    axis=1
)

tax_slab_df = tax_slab_df[['Lower Bound (PKR)', 'Upper Bound (PKR)', 'Rate (%)']]
st.dataframe(tax_slab_df)

# User input for income
st.sidebar.header("Income Input")
income = st.sidebar.number_input("Enter your annual income (PKR):", min_value=0.0, step=1000.0)

# Calculate and display results
if st.sidebar.button("Calculate Tax"):
    if income:
        tax = calculate_tax(income, brackets)
        monthly_salary = income / 12
        monthly_tax = tax / 12
        annual_salary_after_tax = income - tax

        # Display results
        st.subheader("Calculation Results")
        st.write(f"**Yearly Tax for {year}:** PKR {tax:,.2f}")
        st.write(f"**Monthly Salary before Tax:** PKR {monthly_salary:,.2f}")
        st.write(f"**Monthly Tax:** PKR {monthly_tax:,.2f}")
        st.write(f"**Annual Salary after Tax:** PKR {annual_salary_after_tax:,.2f}")

        # Display detailed breakdown
        st.subheader("Detailed Breakdown")
        breakdown = []
        for lower, upper, rate in brackets:
            if income > lower:
                taxable_income = min(income, upper) - lower
                breakdown.append({
                    'Bracket': f"{lower:,} - {upper:,}" if upper != float('inf') else f"{lower:,} and above",
                    'Taxable Income (PKR)': taxable_income,
                    'Rate (%)': rate * 100,
                    'Tax (PKR)': taxable_income * rate
                })
        breakdown_df = pd.DataFrame(breakdown)
        st.dataframe(breakdown_df)