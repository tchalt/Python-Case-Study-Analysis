# Lithuania PV Production Financial Plan (Market-Scaled)

This repository contains the financial modeling and report generation scripts for a PV manufacturing hub in Klaipeda FEZ, Lithuania. The project is scaled to a 250 MW maximum capacity, reflecting a realistic share of the Lithuanian domestic market.

## Project Specifications
- **Project Scale**: Total Max Capacity = 250 MW.
- **Product**: High-efficiency modules using LONGi HPBC 2.0 technology (24.8% efficiency).
- **Financial Horizon**: 5 years (2026–2030).
- **Key Incentive**: 0% Corporate Income Tax (CIT) for 10 years in Klaipeda FEZ.

## Project Structure
- `financial_model.py`: Core Python script that calculates capacity, sales, variable costs (including packaging), fixed costs, and EBITDA.
- `generate_charts.py`: Generates visualizations for production volume ramp-up and break-even path using Matplotlib.
- `generate_pdf.py`: Creates a structured PDF report following professional templates.
- `generate_pptx.py`: Generates a professional presentation slide deck.
- `financial_data.csv`: Exported data from the financial model.
- `volume_rampup.png` & `breakeven_chart.png`: Generated visualization charts.

## Key Financial Summary (Year 5 - 2030)
- **Effective Capacity**: 245.00 MW
- **Revenue**: EUR 28.47 Million
- **Total Variable Cost**: EUR 99,898/MW (includes Materials, Packaging, Labor, Energy, and Scrap Effect)
- **Annual Fixed Burden**: EUR 1,200,000
- **EBITDA**: EUR 2.80 Million
- **Break-even Units**: 73.53 MW
- **Margin of Safety**: 70.0%

## Deliverables
- [Production_Financial_Plan_Milestone_2_Final.pdf] Comprehensive data analysis report.
- [Production_Financial_Plan_Presentation.pptx] Strategic evaluation presentation.
- [PDF_Data_Analysis_Report.txt] Structured text-based analysis summary.

---
*Report Generated: 2026-03-21*
