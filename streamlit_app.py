import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="HustleLedger", page_icon="💼")

st.title("💼 HustleLedger")
st.subheader("Helping informal businesses build a trusted financial track record.")

FILE = "transactions.csv"

if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["Date", "Type", "Description", "Amount"])

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Add Sale", "Add Expense", "Transactions"]
)

if menu == "Dashboard":
    sales = df[df["Type"] == "Sale"]["Amount"].sum()
    expenses = df[df["Type"] == "Expense"]["Amount"].sum()

    st.metric("Total Sales", f"R{sales:.2f}")
    st.metric("Total Expenses", f"R{expenses:.2f}")
    st.metric("Profit", f"R{sales-expenses:.2f}")

elif menu == "Add Sale":
    st.header("Record Sale")
    desc = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0)

    if st.button("Save Sale"):
        new = pd.DataFrame([[datetime.now(), "Sale", desc, amount]],
                           columns=df.columns)
        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success("Sale saved!")

elif menu == "Add Expense":
    st.header("Record Expense")
    desc = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0)

    if st.button("Save Expense"):
        new = pd.DataFrame([[datetime.now(), "Expense", desc, amount]],
                           columns=df.columns)
        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success("Expense saved!")

elif menu == "Transactions":
    st.header("Transaction History")
    st.dataframe(df)