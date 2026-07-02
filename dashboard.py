import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_connection


def dashboard(user):

    conn = get_connection()

    user_id = user["id"]

    sales = pd.read_sql(
        "SELECT * FROM sales WHERE user_id=?",
        conn,
        params=(user_id,)
    )

    expenses = pd.read_sql(
        "SELECT * FROM expenses WHERE user_id=?",
        conn,
        params=(user_id,)
    )

    conn.close()

    total_sales = sales["amount"].sum() if not sales.empty else 0
    total_expenses = expenses["amount"].sum() if not expenses.empty else 0
    profit = total_sales - total_expenses

    st.title("📊 HustleLedger Dashboard")
    st.write(f"Welcome, **{user['fullname']}**")

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Sales", f"R {total_sales:,.2f}")
    col2.metric("💸 Total Expenses", f"R {total_expenses:,.2f}")
    col3.metric("📈 Net Profit", f"R {profit:,.2f}")

    st.divider()

    chart_data = pd.DataFrame({
        "Category": ["Sales", "Expenses"],
        "Amount": [total_sales, total_expenses]
    })

    fig = px.bar(
        chart_data,
        x="Category",
        y="Amount",
        title="Business Performance"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    left, right = st.columns(2)

   