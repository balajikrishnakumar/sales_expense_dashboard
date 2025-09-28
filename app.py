import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

# Page configuration
st.set_page_config(page_title="📊 Sales & Expense Dashboard", layout="wide")

# Ensure data directory exists
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
file_path = os.path.join(data_dir, "sales_expenses.csv")

# Load or create dataset
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])
    df.to_csv(file_path, index=False)

# Title
st.title("📊 Sales & Expense Management Dashboard")

# Form to add new data
with st.form("entry_form"):
    date = st.date_input("Date", value=datetime.today())
    entry_type = st.selectbox("Type", ["Sale", "Expense"])
    category = st.selectbox("Category", ["Product A", "Product B", "Marketing", "Travel", "Office", "Other"])
    amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0)
    submit = st.form_submit_button("Add Entry")
    if submit:
        new_data = {
            "Date": date,
            "Type": entry_type,
            "Category": category,
            "Amount": amount
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(file_path, index=False)
        st.success("✅ Entry added!")

# Filter section
st.subheader("📋 Filtered Data Table")
entry_filter = st.multiselect("Select Type", options=["Sale", "Expense"], default=["Sale", "Expense"])
df_filtered = df[df["Type"].isin(entry_filter)]
st.dataframe(df_filtered)

# Metrics
total_sales = df[df["Type"] == "Sale"]["Amount"].sum()
total_expenses = df[df["Type"] == "Expense"]["Amount"].sum()
profit = total_sales - total_expenses

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales (₹)", f"{total_sales:,.2f}")
col2.metric("📉 Total Expenses (₹)", f"{total_expenses:,.2f}")
col3.metric("📈 Net Profit (₹)", f"{profit:,.2f}", delta=f"{profit:.2f}")

# Charts
st.subheader("📈 Visualizations")
if not df_filtered.empty:
    col4, col5 = st.columns(2)

    with col4:
        fig1 = px.line(df_filtered, x="Date", y="Amount", color="Type", title="Amount Over Time")
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    with col5:
        fig2 = px.bar(df_filtered, x="Category", y="Amount", color="Type", title="Amount by Category", barmode="group")
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
else:
    st.warning("No data to display. Please add entries above.")

# Download button
st.download_button(
    label="📥 Download Data as CSV",
    data=df_filtered.to_csv(index=False),
    file_name="sales_expenses.csv",
    mime="text/csv"
)

