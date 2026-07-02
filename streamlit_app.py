import streamlit as st

from database import create_tables
from auth import register_user, login_user
from dashboard import dashboard
from transactions import add_sale, add_expense, view_transactions
from reports import reports_page

# ------------------------
# DATABASE
# ------------------------

create_tables()

# ------------------------
# PAGE SETTINGS
# ------------------------

st.set_page_config(
    page_title="HustleLedger",
    page_icon="💼",
    layout="wide"
)

# ------------------------
# SESSION STATE
# ------------------------

if "user" not in st.session_state:
    st.session_state.user = None

# ------------------------
# LOGIN / REGISTER
# ------------------------

if st.session_state.user is None:

    st.title("💼 HustleLedger")
    st.caption("Helping informal businesses build a trusted financial track record.")

    menu = st.sidebar.radio(
        "Account",
        ["Login", "Register"]
    )

    if menu == "Register":

        st.subheader("Create Account")

        fullname = st.text_input("Full Name")
        business = st.text_input("Business Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Create Account"):

            if register_user(fullname, email, password, business):
                st.success("Account created successfully.")
            else:
                st.error("Email already exists.")

    else:

        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = login_user(email, password)

            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid email or password.")

# ------------------------
# MAIN APPLICATION
# ------------------------

else:

    user = st.session_state.user

    st.sidebar.success(f"Welcome {user['fullname']}")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Add Sale",
            "Add Expense",
            "Transactions",
            "Reports"
        ]
    )

    if page == "Dashboard":
        dashboard(user["id"])

    elif page == "Add Sale":
        add_sale(user["id"])

    elif page == "Add Expense":
        add_expense(user["id"])

    elif page == "Transactions":
        view_transactions(user["id"])

    elif page == "Reports":
        reports_page(user["id"])

    st.sidebar.markdown("---")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()