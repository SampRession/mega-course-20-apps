import glob
import os
from pathlib import Path

import pandas as pd
from fpdf import FPDF


def generate(invoices_path, pdfs_path, logo_path, invoices_format="xlsx"):
    """Generate pdf files from excel sheets.

    Args:
        invoices_path (str): specify path for invoices input
        pdfs_path (str): specify path for pdfs output
        logo_path (str): specify path for logo
        invoices_format (str, optional): specify invoices format. Defaults to "xlsx".
    """
    
    filepaths = glob.glob(f"{invoices_path}/*.{invoices_format}")

    for filepath in filepaths:
        # Invoice number format
        filename = Path(filepath).stem
        invoice_number = filename.split("-")[0]

        # Date format
        raw_date = filename.split("-")[1].strip(".xlsx")
        date_y, date_m, date_d = raw_date.split(".")
        if len(date_m) == 1:
            date_m = f"0{date_m}"
        invoice_date = f"{date_y}/{date_m}/{date_d}"

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "b", 20)
        pdf.cell(
            0, 10, f"Invoice nr. {invoice_number}", new_x="LEFT", new_y="NEXT"
        )
        pdf.cell(0, 10, f"Date: {invoice_date}", new_x="LEFT", new_y="NEXT")
        pdf.cell(0, 15, new_x="LEFT", new_y="NEXT")

        # Import datas from excel file
        df = pd.read_excel(f"{invoices_path}/{filename}.{invoices_format}")

        # Columns headers
        columns_h_raw = df.columns
        columns_h = [
            item.replace("_", " ").capitalize() for item in columns_h_raw
        ]
        pdf.set_font("helvetica", size=11, style="b")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(25, 8, text=columns_h[0], border=1, align="c")
        pdf.cell(70, 8, text=columns_h[1], border=1, align="c")
        pdf.cell(40, 8, text=columns_h[2], border=1, align="c")
        pdf.cell(30, 8, text=columns_h[3], border=1, align="c")
        pdf.cell(
            25,
            8,
            text=columns_h[4],
            border=1,
            align="c",
            new_y="NEXT",
            new_x="LMARGIN",
        )

        # Table rows with for loop
        pdf.set_font("helvetica", size=10)
        for index, row in df.iterrows():
            pdf.cell(
                25, 8, text=str(row[columns_h_raw[0]]), border=1, align="c"
            )
            pdf.cell(70, 8, text=str(row[columns_h_raw[1]]), border=1)
            pdf.cell(
                40, 8, text=str(row[columns_h_raw[2]]), border=1, align="r"
            )
            pdf.cell(
                30, 8, text=str(row[columns_h_raw[3]]), border=1, align="r"
            )
            pdf.cell(
                25,
                8,
                text=str(row[columns_h_raw[4]]),
                border=1,
                align="r",
                new_y="NEXT",
                new_x="LMARGIN",
            )

        # Total price
        pdf.set_font("helvetica", size=11, style="b")
        total_sum = df["total_price"].sum()
        pdf.cell(25, 8, text="", border=1, align="c")
        pdf.cell(70, 8, text="", border=1)
        pdf.cell(40, 8, text="", border=1, align="r")
        pdf.cell(30, 8, text="", border=1, align="r")
        pdf.cell(
            25,
            8,
            text=f"{str(total_sum)} $",
            border=1,
            align="r",
            new_y="NEXT",
            new_x="LMARGIN",
        )

        # Total sum sentence
        pdf.set_font("helvetica", "b", 16)
        pdf.cell(0, 15, new_x="LEFT", new_y="NEXT")
        pdf.cell(
            30,
            8,
            text=f"The total due amount is {total_sum}$.",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        # Company logo and name
        pdf.cell(0, 3, new_x="LEFT", new_y="NEXT")
        pdf.cell(35, 12, "PythonHow")
        pdf.image(f"{logo_path}/pythonhow.png", w=10)

        # Export pdf in 'output' dir
        if not os.path.exists(f"{pdfs_path}/"):
            os.mkdir(f"{pdfs_path}")
        pdf.output(name=f"{pdfs_path}/{filename.strip('.xlsx')}.pdf")
