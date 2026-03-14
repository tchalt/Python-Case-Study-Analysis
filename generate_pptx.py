from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
import os

def create_presentation():
    prs = Presentation()

    # Slide 1: Title Slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "BalticSolar Tech: Production Financial Plan"
    subtitle.text = "Strategic Investment Evaluation - Klaipeda Hub\nMarch 2026"

    # Slide 2: Project Recap & Story
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Project Overview & Story"
    content = slide.placeholders[1]
    content.text = ("• Strategic local production in Klaipeda FEZ, Lithuania.\n"
                    "• Transition from Chinese outsourcing to 'Made in EU'.\n"
                    "• High-efficiency HPBC 2.0 Tech (24.8%) to secure market share.\n"
                    "• Leveraging 0% CIT and optimized logistics.")

    # Slide 3: Baseline vs With-Project Summary
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Baseline vs. With-Project Summary"
    rows, cols = 3, 3
    table = slide.shapes.add_table(rows, cols, Inches(0.5), Inches(1.5), Inches(9), Inches(2)).table
    table.cell(0, 0).text = 'Metric'
    table.cell(0, 1).text = 'Baseline (Outsource)'
    table.cell(0, 2).text = 'With-Project (Local)'
    table.cell(1, 0).text = 'Supply Chain'
    table.cell(1, 1).text = 'High risk, long lead'
    table.cell(1, 2).text = 'Secure EU local'
    table.cell(2, 0).text = 'Unit Cost (2030)'
    table.cell(2, 1).text = '> EUR 115k (Import)'
    table.cell(2, 2).text = 'EUR 94.7k (Internal)'

    # Slide 4: Capacity & Ramp-up Plan (Template 1)
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "TABLE 1: Capacity & Ramp-up Plan"
    rows, cols = 6, 5
    table = slide.shapes.add_table(rows, cols, Inches(0.5), Inches(1.5), Inches(9), Inches(3)).table
    headers = ['Year', 'Max Cap', 'Util %', 'Scrap %', 'Eff Cap']
    data = [
        ['Year 1 (2026)', '2300', '50.0%', '5.0%', '1092.5'],
        ['Year 2 (2027)', '2300', '75.0%', '4.0%', '1656.0'],
        ['Year 3 (2028)', '2300', '90.0%', '3.0%', '2007.9'],
        ['Year 4 (2029)', '2300', '95.0%', '2.0%', '2141.3'],
        ['Year 5 (2030)', '2300', '100.0%', '2.0%', '2254.0']
    ]
    for c, h in enumerate(headers): table.cell(0, c).text = h
    for r, row in enumerate(data):
        for c, val in enumerate(row): table.cell(r+1, c).text = val

    # Slide 5: Volume Ramp-up Chart
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Chart: Production Volume Ramp-up"
    if os.path.exists('volume_rampup.png'):
        slide.shapes.add_picture('volume_rampup.png', Inches(1), Inches(1.5), width=Inches(8))

    # Slide 6: Sales Forecast (Template 2)
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "TABLE 2: Sales Forecast"
    rows, cols = 6, 4
    table = slide.shapes.add_table(rows, cols, Inches(0.5), Inches(1.5), Inches(9), Inches(3)).table
    headers = ['Year', 'Units sold', 'Price (EUR)', 'Revenue (EUR)']
    data = [
        ['Year 1', '1092.5', '126,000', '137,655,000'],
        ['Year 2', '1656.0', '123,480', '204,482,880'],
        ['Year 3', '2007.9', '121,010', '242,976,782'],
        ['Year 4', '2141.3', '118,590', '253,937,178'],
        ['Year 5', '2254.0', '116,218', '261,956,247']
    ]
    for c, h in enumerate(headers): table.cell(0, c).text = h
    for r, row in enumerate(data):
        for c, val in enumerate(row): table.cell(r+1, c).text = val

    # Slide 7: Unit Variable Cost Breakdown (Template 3)
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "TABLE 3: Variable Cost Breakdown (2030)"
    rows, cols = 6, 4
    table = slide.shapes.add_table(rows, cols, Inches(0.5), Inches(1.5), Inches(9), Inches(3)).table
    headers = ['Component', 'Formula', 'EUR/unit', 'Source']
    data = [
        ['Materials', 'P * 0.72 * eff', '85,107', 'LONGi 2025'],
        ['Direct labor', '7.05 * 800h', '5,640', 'VDI 2026 Jan'],
        ['Energy', '0.18 * 14k', '2,520', 'FEZ 2024'],
        ['Scrap Effect', 'Cost/(1-S)', '1,930', 'Industry Std'],
        ['Total', 'Sum', '94,740', '-']
    ]
    for c, h in enumerate(headers): table.cell(0, c).text = h
    for r, row in enumerate(data):
        for c, val in enumerate(row): table.cell(r+1, c).text = val

    # Slide 8: Operating Statement (Template 5)
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "TABLE 5: Project Operating Statement"
    rows, cols = 6, 5
    table = slide.shapes.add_table(rows, cols, Inches(0.2), Inches(1.5), Inches(9.6), Inches(3)).table
    headers = ['Year', 'Revenue', 'Variable costs', 'Fixed costs', 'EBITDA']
    data = [
        ['Year 1', '137,655,000', '108,744,000', '5,000,000', '23,911,000'],
        ['Year 2', '204,482,880', '162,370,800', '5,500,000', '36,612,080'],
        ['Year 3', '242,976,782', '193,955,191', '5,500,000', '43,521,591'],
        ['Year 4', '253,937,178', '203,795,975', '5,500,000', '44,641,203'],
        ['Year 5', '261,956,247', '213,543,309', '5,500,000', '42,912,938']
    ]
    for c, h in enumerate(headers): table.cell(0, c).text = h
    for r, row in enumerate(data):
        for c, val in enumerate(row): table.cell(r+1, c).text = val

    # Slide 9: Break-even Chart
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Break-even Analysis (Chart)"
    if os.path.exists('breakeven_chart.png'):
        slide.shapes.add_picture('breakeven_chart.png', Inches(1), Inches(1.5), width=Inches(8))

    # Slide 10: Assumptions & Sources (Template 7)
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Assumptions & Sources"
    rows, cols = 6, 3
    table = slide.shapes.add_table(rows, cols, Inches(0.5), Inches(1.5), Inches(9), Inches(4)).table
    headers = ['Assumption', 'Value', 'Source']
    data = [
        ['Wage Rate (Min)', 'EUR 7.05/h', 'VDI 2026 Jan'],
        ['CIT Rate', '0%', 'FEZ Law (10yr)'],
        ['Price Erosion', '2% YoY', 'Market Analysis'],
        ['HPBC 2.0 Eff.', '24.8%', 'LONGi 2025'],
        ['Elec. Price', 'EUR 0.18/kWh', 'Eurostat']
    ]
    for c, h in enumerate(headers): table.cell(0, c).text = h
    for r, row in enumerate(data):
        for c, val in enumerate(row): table.cell(r+1, c).text = val

    prs.save('Production_Financial_Plan_Presentation.pptx')
    print("Presentation generated: Production_Financial_Plan_Presentation.pptx")

if __name__ == "__main__":
    create_presentation()
