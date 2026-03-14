from fpdf import FPDF
import pandas as pd
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'BalticSolar Tech: Production Financial Plan', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, text):
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 5, text)
        self.ln(5)

    def add_table(self, data, headers):
        self.set_font('Helvetica', 'B', 9)
        page_width = self.w - 2 * self.l_margin
        col_width = page_width / len(headers)
        
        for header in headers:
            self.cell(col_width, 7, header, 1)
        self.ln()
        
        self.set_font('Helvetica', '', 8)
        for row in data:
            for item in row:
                text = str(item)
                if self.get_string_width(text) > col_width - 2:
                    text = text[:int(col_width/2)] + ".."
                self.cell(col_width, 6, text, 1)
            self.ln()
        self.ln(5)

pdf = PDFReport()
pdf.add_page()

# 1. Project Recap
pdf.chapter_title("1. Project Recap & Baseline")
recap = ("Establishing a 2.3 GW integrated facility in Klaipeda FEZ, Lithuania. "
         "The 'With-Project' scenario leverages 0% CIT and LONGi's HPBC 2.0 technology (24.8% efficiency). "
         "The strategy uses a technology premium and operational efficiency gains to offset market price erosion.")
pdf.chapter_body(recap)

# 2. Capacity Model (TABLE TEMPLATE 1)
pdf.chapter_title("2. TABLE TEMPLATE 1 - Capacity & ramp-up plan")
capacity_headers = ['Year', 'Max capacity', 'Utilization %', 'Scrap % (if relevant)', 'Effective capacity']
capacity_data = [
    ['Year 1 (2026)', '2300', '50.0%', '5.0%', '1092.5'],
    ['Year 2 (2027)', '2300', '75.0%', '4.0%', '1656.0'],
    ['Year 3 (2028)', '2300', '90.0%', '3.0%', '2007.9'],
    ['Year 4 (2029)', '2300', '95.0%', '2.0%', '2141.3'],
    ['Year 5 (2030)', '2300', '100.0%', '2.0%', '2254.0']
]
pdf.add_table(capacity_data, capacity_headers)

# Chart 1: Volume Ramp-up
if os.path.exists('volume_rampup.png'):
    pdf.image('volume_rampup.png', x=10, w=180)
    pdf.ln(5)

# 3. Sales Model (TABLE TEMPLATE 2)
pdf.chapter_title("3. TABLE TEMPLATE 2 - Sales forecast")
sales_headers = ['Year', 'Units sold', 'Price (EUR/unit)', 'Revenue (EUR)', 'Justification (short)']
sales_data = [
    ['Year 1', '1092.5', '126,000', '137,655,000', 'HPBC 2.0 premium'],
    ['Year 2', '1656.0', '123,480', '204,482,880', '2% erosion'],
    ['Year 3', '2007.9', '121,010', '242,976,782', 'Scale economies'],
    ['Year 4', '2141.3', '118,590', '253,937,178', 'Market penetration'],
    ['Year 5', '2254.0', '116,218', '261,956,247', 'Floor price reached']
]
pdf.add_table(sales_data, sales_headers)

# 4. Unit Variable Cost (TABLE TEMPLATE 3)
pdf.chapter_title("4. TABLE TEMPLATE 3 - Variable cost per unit breakdown")
vcost_headers = ['Component', 'Driver', 'Formula', 'EUR/unit', 'Source']
# Based on Year 5 (2030) calculation in model
vcost_data = [
    ['Materials', 'Silicon/Cells', 'P * 0.72 * eff', '85,107', 'LONGi 2025'],
    ['Direct labor', 'Min. wage 2026', '7.05 * 800h', '5,640', 'VDI 2026 Jan'],
    ['Energy', 'Ind. Rate', '0.18 * 14k', '2,520', 'FEZ 2024'],
    ['Scrap Effect', 'Process waste', 'Cost/(1-S)', '1,930', 'Industry Std'],
    ['Total', '-', 'Sum', '94,740', '-']
]
pdf.add_table(vcost_data, vcost_headers)

# 5. Incremental Fixed Costs (TABLE TEMPLATE 4)
pdf.chapter_title("5. TABLE TEMPLATE 4 - Incremental fixed costs")
fixed_headers = ['Year', 'Maintenance', 'Extra staff', 'Rent/overhead', 'Other', 'Total fixed']
fixed_data = [
    ['Year 1', '1,800,000', '1,200,000', '400,000', '1,600,000', '5,000,000'],
    ['Year 2', '2,000,000', '1,400,000', '400,000', '1,700,000', '5,500,000'],
    ['Year 3', '2,000,000', '1,400,000', '400,000', '1,700,000', '5,500,000'],
    ['Year 4', '2,000,000', '1,400,000', '400,000', '1,700,000', '5,500,000'],
    ['Year 5', '2,000,000', '1,400,000', '400,000', '1,700,000', '5,500,000']
]
pdf.add_table(fixed_data, fixed_headers)

# 6. Operating Statement (TABLE TEMPLATE 5)
pdf.chapter_title("6. TABLE TEMPLATE 5 - Project operating statement")
op_headers = ['Year', 'Units', 'Revenue', 'Variable costs', 'Contribution', 'Fixed costs', 'EBITDA']
op_data = [
    ['Year 1', '1092.5', '137,655,000', '108,744,000', '28,911,000', '5,000,000', '23,911,000'],
    ['Year 2', '1656.0', '204,482,880', '162,370,800', '42,112,080', '5,500,000', '36,612,080'],
    ['Year 3', '2007.9', '242,976,782', '193,955,191', '49,021,591', '5,500,000', '43,521,591'],
    ['Year 4', '2141.3', '253,937,178', '203,795,975', '50,141,203', '5,500,000', '44,641,203'],
    ['Year 5', '2254.0', '261,956,247', '213,543,309', '48,412,938', '5,500,000', '42,912,938']
]
pdf.add_table(op_data, op_headers)

# 7. Break-even Analysis (TABLE TEMPLATE 6)
pdf.chapter_title("7. TABLE TEMPLATE 6 - Break-even (2030)")
be_headers = ['Item', 'Value', 'Notes']
be_data = [
    ['Price (EUR/unit)', '116,218', 'EUR/MW'],
    ['Variable cost (EUR/unit)', '94,740', 'EUR/MW'],
    ['Contribution (EUR/unit)', '21,478', 'Price - Variable cost'],
    ['Fixed costs (EUR/period)', '5,500,000', 'Annual burden'],
    ['Break-even units (Q_BE)', '256.1', 'Fixed / Contrib unit'],
    ['Break-even revenue', '29,760,639', 'Q_BE * Price'],
    ['Margin of safety', '88.6%', '(Exp - Q_BE)/Exp']
]
pdf.add_table(be_data, be_headers)

# Chart 2: Break-even Chart
if os.path.exists('breakeven_chart.png'):
    pdf.image('breakeven_chart.png', x=10, w=180)
    pdf.ln(5)

# 8. Assumptions & Sources (TABLE TEMPLATE 7)
pdf.chapter_title("8. TABLE TEMPLATE 7 - Assumptions & Sources")
sources_headers = ['Assumption', 'Value', 'Unit', 'Source', 'Why reasonable', 'Low/Base/High']
sources_data = [
    ['Price', '126,000', 'EUR/MW', 'LONGi 2025', 'HPBC 2.0 premium', 'Base'],
    ['Volume / demand', '2,300', 'MW', 'Market study', 'EU solar target', 'Base'],
    ['Ramp-up (utilization)', '50%-100%', '%', 'Project plan', 'Staged growth', 'Base'],
    ['Wage rate (min)', '7.05', 'EUR/h', 'VDI 2026 Jan', 'Lithuanian regulation', 'Base'],
    ['Energy price', '0.18', 'EUR/kWh', 'Eurostat', 'Baltic industrial', 'Base'],
    ['Scrap / yield', '2% - 5%', '%', 'Industry Std', 'Improving ramp-up', 'Base'],
    ['Maintenance', '2,000,000', 'EUR/yr', 'Vendor spec', 'High-tech eqpt', 'Base']
]
pdf.add_table(sources_data, sources_headers)

# Save
pdf_file = "/Users/tangtaowei/Desktop/MC PF/IE/Mar 17/Production_Financial_Plan_Milestone_2_Final.pdf"
pdf.output(pdf_file)
print(f"Final Template-Compliant PDF generated: {pdf_file}")
