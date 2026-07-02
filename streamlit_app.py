import streamlit as st
from auth import init_db, register_user, login_user
from dashboard import dashboard

st.set_page_config(
    page_title="HustleLedger",
    page_icon="💼",
    layout="wide"
)

init_db()

st.title("💼 HustleLedger")
st.caption("Helping informal businesses build a trusted financial track record.")

menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Register"]
)

if menu == "Register":

    st.subheader("Create Account")

    fullname = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):

        if fullname == "" or email == "" or password == "":
            st.warning("Please complete all fields.")
        else:
            if register_user(fullname, email, password):
                st.success("✅ Account created successfully.")
            else:
                st.error("Email already exists.")

else:

    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = login_user(email, password)

        if user:
            st.success(f"Welcome {user[1]}!")
            dashboard()
        else:
            st.error("Incorrect email or password.")