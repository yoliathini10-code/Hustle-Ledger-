import streamlit as st
import pandas as pd
from database import get_connection


def add_sale(user_id):

    st.subheader("➕ Record Sale")

    description = st.text_input("Sale Description")
    amount = st.number_input("Amount (R)", min_value=0.0, step=1.0)
    date = st.date_input("Sale Date")

    if st.button("Save Sale"):

        if description == "":
            st.warning("Please enter a description.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sales
            (user_id, description, amount, transaction_date)
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            description,
            amount,
            str(date)
        ))

        conn.commit()
        conn.close()

        st.success("Sale saved successfully.")


def add_expense(user_id):

    st.subheader("➖ Record Expense")

    description = st.text_input("Expense Description")
    amount = st.number_input("Expense Amount (R)", min_value=0.0, step=1.0)
    date = st.date_input("Expense Date")

    if st.button("Save Expense"):

        if description == "":
            st.warning("Please enter a description.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO expenses
            (user_id, description, amount, transaction_date)
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            description,
            amount,
            str(date)
        ))

        conn.commit()
        conn.close()

        st.success("Expense saved successfully.")


def view_transactions(user_id):

    conn = get_connection()

    sales = pd.read_sql(
        "SELECT transaction_date, description, amount FROM sales WHERE user_id=?",
        conn,
        params=(user_id,)
    )

    expenses = pd.read_sql(
        "SELECT transaction_date, description, amount FROM expenses WHERE user_id=?",
        conn,
        params=(user_id,)
    )

    conn.close()

    st.subheader("Sales")

    if sales.empty:
        st.info("No sales recorded.")
    else:
        st.dataframe(sales, use_container_width=True)

    st.subheader("Expenses")

    if expenses.empty:
        st.info("No expenses recorded.")
    else:
        st.dataframe(expenses, use_container_width=True)