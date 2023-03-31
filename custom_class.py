from fpdf import FPDF

class PDF(FPDF):
  def header(self):
    self.image("Logo.png", 27, 10, 160)
    self.set_font("times", "B", 12)
    self.cell(0, 90, "IDEA-net: Expanding the network of Inclusion, Diversity, Equity and Access (IDEA) practitioners in higher", border=False, ln=True, align="C")
    self.cell(0, -80, "education through institutional capacity building", border=False, ln=True, align="C")
    self.cell(0, 93, "Project Reference : 2022-1-NL01-KA220-HED-000089789", border=False, ln=True, align="C")
    self.set_font("times", "I", 12)
    self.cell(0, -80, 'Programme Erasmus+ key action 2 "Partnerships for Cooperation"', border=False, ln=True, align="C")

    self.ln(50)


  def footer(self):
    self.set_y(-15)
    self.set_font("times", "B", 12)
    self.cell(0, 10, f"{self.page_no()}", align="C")