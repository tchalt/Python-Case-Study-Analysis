from fpdf import FPDF
import pandas as pd
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'Lithuania PV Production Financial Plan (Market-Scaled)', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, text):
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 5, text)
        self.ln(5)

    def add_table(self, data, headers, col_widths=None):
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(73, 124, 182) 
        self.set_text_color(255, 255, 255)
        
        page_width = self.w - 2 * self.l_margin
        if col_widths is None:
            col_width = page_width / len(headers)
            col_widths = [col_width] * len(headers)
        
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, 'C', True)
        self.ln()
        
        self.set_font('Helvetica', '', 8)
        self.set_text_color(0, 0, 0)
        fill = False
        for row in data:
            if fill:
                self.set_fill_color(217, 226, 243)
            else:
                self.set_fill_color(255, 255, 255)
                
            for i, item in enumerate(row):
                text = str(item).replace('€', 'EUR')
                if self.get_string_width(text) > col_widths[i] - 2:
                    text = text[:int(col_widths[i]/4)] + ".."
                self.cell(col_widths[i], 7, text, 1, 0, 'C', True)
            self.ln()
            fill = not fill
        self.ln(5)

# Load data
df = pd.read_csv('financial_data.csv')
y5 = df.iloc[-1]

pdf = PDFReport()
pdf.add_page()

# 1. Baseline vs With-Project Summary
pdf.chapter_title("1. Baseline vs With-Project summary")
baseline_headers = ['Metric', 'Baseline (Outsource)', 'With-Project (Local)']
baseline_data = [
    ['Supply Chain Risk', 'High (Long lead times)', 'Low (Local control)'],
    ['Production Cost', 'Market Price + Margin', 'Internal Variable Cost'],
    ['Strategic Value', 'Dependency on Imports', 'EU "Made in EU" Premium'],
    ['CIT Rate', '15%', '0% (Klaipeda FEZ)']
]
pdf.add_table(baseline_data, baseline_headers, col_widths=[50, 70, 70])

# 2. Capacity & Ramp-up Plan
pdf.chapter_title("TABLE TEMPLATE 1 - Capacity & ramp-up plan")
cap_headers = ['Year', 'Max capacity', 'Utilization %', 'Scrap %', 'Effective capacity']
cap_data = []
for idx, row in df.iterrows():
    cap_data.append([
        f"Year {idx+1}",
        f"{row['Max_Capacity_MW']:.0f}",
        f"{row['Utilization_%']*100:.1f}%",
        f"{row['Scrap_%']*100:.1f}%",
        f"{row['Effective_Capacity_MW']:.2f}"
    ])
pdf.add_table(cap_data, cap_headers)

# 3. Sales Forecast
pdf.chapter_title("TABLE TEMPLATE 2 - Sales forecast")
sales_headers = ['Year', 'Units sold', 'Price (EUR/unit)', 'Revenue (EUR)', 'Justification (short)']
sales_data = []
justifications = ['Market entry', 'Growth phase', 'Scale reach', 'Maturity', 'Full capacity']
for idx, row in df.iterrows():
    sales_data.append([
        f"Year {idx+1}",
        f"{row['Effective_Capacity_MW']:.2f}",
        f"{row['Price_EUR_MW']:,.0f}",
        f"{row['Revenue_EUR']:,.0f}",
        justifications[idx]
    ])
pdf.add_table(sales_data, sales_headers, col_widths=[25, 35, 35, 45, 50])

# 4. Unit Variable Cost Build-up
pdf.chapter_title("TABLE TEMPLATE 3 - Variable cost per unit breakdown")
vcost_headers = ['Component', 'Driver', 'Formula', 'EUR/unit', 'Source']
vcost_data = [
    ['Materials/ingredients', 'LONGi HPBC 2.0', 'Direct', '80,700', 'LONGi 2025 Spec'],
    ['Packaging', 'Export grade', 'Fixed', '1,500', 'Logistics Spec'],
    ['Direct labor', 'Lithuania Min', '800h * 16.5', '13,200', 'VDI 2026 Standard'],
    ['Energy (if relevant)', 'Industrial rate', '0.18/kWh', '2,500', 'Eurostat Baltic'],
    ['Platform fee / other', 'Scrap Effect', 'Cost/(1-S)-C', f"{y5['Scrap_Effect_EUR_MW']:,.0f}", 'Industry Std']
]
pdf.add_table(vcost_data, vcost_headers, col_widths=[45, 35, 35, 35, 40])

# 5. Incremental Fixed Costs
pdf.chapter_title("TABLE TEMPLATE 4 - Incremental fixed costs")
fixed_headers = ['Year', 'Maintenance', 'Extra staff', 'Rent/overhead', 'Other', 'Total fixed']
fixed_data = []
for idx, row in df.iterrows():
    fixed_data.append([
        f"Year {idx+1}",
        '432,000',
        '288,000',
        '96,000',
        '384,000',
        '1,200,000'
    ])
pdf.add_table(fixed_data, fixed_headers)

# 6. Project Operating Statement
pdf.chapter_title("TABLE TEMPLATE 5 - Project operating statement")
op_headers = ['Year', 'Units', 'Revenue', 'Variable costs', 'Contribution', 'Fixed costs', 'EBITDA']
op_data = []
for idx, row in df.iterrows():
    op_data.append([
        f"Year {idx+1}",
        f"{row['Effective_Capacity_MW']:.1f}",
        f"{row['Revenue_EUR']:,.0f}",
        f"{row['Total_Var_Costs_EUR']:,.0f}",
        f"{row['Contribution_Margin_EUR']:,.0f}",
        '1,200,000',
        f"{row['EBITDA_EUR']:,.0f}"
    ])
pdf.add_table(op_data, op_headers, col_widths=[20, 20, 35, 35, 35, 25, 20])

# 7. Break-even Calculation
pdf.chapter_title("TABLE TEMPLATE 6 - Break-even")
q_be = y5['Fixed_Costs_EUR'] / (y5['Price_EUR_MW'] - y5['Total_Var_Cost_Per_MW'])
mos = (y5['Effective_Capacity_MW'] - q_be) / y5['Effective_Capacity_MW'] * 100
be_data = [
    ['Price (EUR/unit)', f"{y5['Price_EUR_MW']:,.0f}", 'EUR/MW'],
    ['Variable cost (EUR/unit)', f"{y5['Total_Var_Cost_Per_MW']:,.0f}", 'EUR/MW'],
    ['Contribution (EUR/unit)', f"{(y5['Price_EUR_MW'] - y5['Total_Var_Cost_Per_MW']):,.0f}", 'Price - Variable cost'],
    ['Fixed costs (EUR/period)', '1,200,000', 'Annual burden'],
    ['Break-even units (Q_BE)', f"{q_be:,.2f}", 'Fixed / Contribution per unit'],
    ['Break-even revenue', f"{q_be * y5['Price_EUR_MW']:,.0f}", 'Q_BE x Price'],
    ['Margin of safety', f"{mos:.1f}%", '(Expected - Q_BE)/Expected']
]
pdf.add_table(be_data, ['Item', 'Value', 'Notes'], col_widths=[50, 40, 100])

# 8. Assumptions & Sources
pdf.chapter_title("TABLE TEMPLATE 7 - Assumptions & Sources")
sources_headers = ['Assumption', 'Value', 'Unit', 'Source', 'Why reasonable', 'Low/Base/High']
sources_data = [
    ['Price', '126,000', 'EUR/MW', 'LONGi 2025', 'HPBC 2.0 premium', 'Base'],
    ['Volume / demand', '250', 'MW', 'Market study', 'Realistic domestic share', 'Base'],
    ['Ramp-up (utilization)', '50%-100%', '%', 'Project plan', 'Staged growth', 'Base'],
    ['Wage rate', '16.50', 'EUR/h', 'VDI 2026', 'Lithuanian standard', 'Base'],
    ['Energy price', '0.18', 'EUR/kWh', 'Eurostat', 'Baltic industrial', 'Base'],
    ['Scrap / yield', '2% - 5%', '%', 'Industry Std', 'Improving ramp-up', 'Base'],
    ['Maintenance', '432,000', 'EUR/yr', 'Vendor spec', 'Scaled for 250MW', 'Base']
]
pdf.add_table(sources_data, sources_headers, col_widths=[35, 20, 20, 30, 45, 30])

# Visuals at the end
pdf.add_page()
pdf.chapter_title("Financial Visualizations")
if os.path.exists('volume_rampup.png'):
    pdf.image('volume_rampup.png', x=15, w=180)
    pdf.ln(5)
if os.path.exists('breakeven_chart.png'):
    pdf.image('breakeven_chart.png', x=15, w=180)

# Save
output_path = "/Users/tangtaowei/Desktop/IE/Mar 17/Production_Financial_Plan_Milestone_2_Final.pdf"
pdf.output(output_path)
print(f"Reordered and updated PDF generated: {output_path}")
