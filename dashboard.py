import streamlit as st
import sqlite3
import pandas as pd

DB_NAME = "hustleledger.db"

def dashboard():

    conn = sqlite3.connect(DB_NAME)

    sales = pd.read_sql("SELECT * FROM sales", conn)
    expenses = pd.read_sql("SELECT * FROM expenses", conn)

    total_sales = sales["amount"].sum() if not sales.empty else 0
    total_expenses = expenses["amount"].sum() if not expenses.empty else 0
    profit = total_sales - total_expenses

    st.title("📊 HustleLedger Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("Sales", f"R{total_sales:,.2f}")
    c2.metric("Expenses", f"R{total_expenses:,.2f}")
    c3.metric("Profit", f"R{profit:,.2f}")

    st.divider()

    st.subheader("Recent Sales")
    st.dataframe(sales.tail(10), use_container_width=True)

    st.subheader("Recent Expenses")
    st.dataframe(expenses.tail(10), use_container_width=True)

    conn.close()