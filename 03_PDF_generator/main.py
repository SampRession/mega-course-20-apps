import pandas as pd
from fpdf import FPDF

pdf = FPDF(orientation="portrait", unit="mm", format="A4")
pdf.set_auto_page_break(auto=False, margin=0)

df = pd.read_csv("topics.csv")
for index, row in df.iterrows():
    pdf.add_page()
    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 12, text=f"{row['Order']} - {row['Topic']}",
             new_x="LEFT",
             new_y="NEXT",
             border="B")

    # Ardit's solution to Student Project : Lined PDF -> Use page's
    # coordinates in range()
    for y in range(40, 290, 12):
        pdf.line(10, y, 200, y)

    # My solution to Student Project : Lined PDF
    # x1, y1, x2, y2 = 10, 40, 200, 40
    # for i in range(21):
    #     pdf.line(x1, y1, x2, y2)
    #     y1 += 12
    #     y2 += 12

    # Set the footer for main loop
    pdf.set_font("helvetica", "I", 8)
    pdf.ln(268)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 0, text=f"{row['Topic']} - Page {pdf.page_no()}/{{nb}}",
             new_x="RIGHT",
             new_y="TOP",
             align='r')

    for i in range(row['Pages'] - 1):
        pdf.add_page()
        # Set the footer other pages
        pdf.set_font("helvetica", "I", 8)
        pdf.ln(280)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 0, text=f"{row['Topic']} - Page {pdf.page_no()}/{{nb}}",
                 new_x="RIGHT",
                 new_y="TOP",
                 align='r')

        # Ardit's solution to Student Project : Lined PDF -> Use page's
        # coordinates in range()
        for y in range(20, 290, 12):
            pdf.line(10, y, 200, y)

        # My solution to Student Project : Lined PDF
        # x1, y1, x2, y2 = 10, 20, 200, 20
        # for x in range(23):
        #     pdf.line(x1, y1, x2, y2)
        #     y1 += 12
        #     y2 += 12

pdf.output("tuto1.pdf")
