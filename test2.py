from fpdf import FPDF
# from PyPDF2 import PdfWriter
from io import StringIO, BytesIO

temp = StringIO()

pdf = FPDF()
pdf.add_page()
pdf.set_font("times", "", 16)

for i in range(1, 41):
    pdf.cell(0, 10, f"This is line{i}", ln=True)


outputStream = open(r"output.pdf", "wb")
pdf.write(outputStream)

outfile = BytesIO()
pdf.write(outfile)

with open("output.pdf", "wb") as f:
    f.write(outfile.getvalue())



