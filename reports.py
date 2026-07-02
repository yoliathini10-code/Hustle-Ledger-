import streamlit as st
import pandas as pd
from database import get_connection
from io import BytesIO
from fpdf import FPDF


def export_excel(user_id):
    conn = get_connection()

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

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        sales.to_excel(writer, sheet_name="Sales", index=False)
        expenses.to_excel(writer, sheet_name="Expenses", index=False)

    st.download_button(
        label="📥 Download Excel Report",
        data=output.getvalue(),
        file_name="HustleLedger_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def export_pdf(user_id):
    conn = get_connection()

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

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "HustleLedger Financial Report", ln=True)

    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Total Sales: R {total_sales:.2f}", ln=True)
    pdf.cell(0, 10, f"Total Expenses: R {total_expenses:.2f}", ln=True)
    pdf.cell(0, 10, f"Net Profit: R {profit:.2f}", ln=True)

    pdf_output = pdf.output(dest="S").encode("latin-1")

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_output,
        file_name="HustleLedger_Report.pdf",
        mime="application/pdf",
    )


def reports_page(user_id):
    st.title("📊 Reports")

    st.write("Export your business reports.")

    export_excel(user_id)

    export_pdf(user_id)