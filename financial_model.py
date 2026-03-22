import pandas as pd
import numpy as np

# --- 1. PROJECT SPECIFICATIONS & ASSUMPTIONS ---
MAX_CAPACITY_MW = 250
YEARS = [2026, 2027, 2028, 2029, 2030]
UTILIZATION = [0.50, 0.75, 0.90, 0.95, 1.00]
SCRAP_RATE = [0.05, 0.04, 0.03, 0.02, 0.02]

# Sales Assumptions
START_PRICE_EUR_MW = 126000  # €0.126/W
PRICE_EROSION = 0.02         # -2.0% annual decline

# Variable Cost Assumptions (per MW)
DIRECT_MATERIALS_EUR_MW = 80700
PACKAGING_EUR_MW = 1500      # Added packaging cost
HOURS_PER_MW = 800
WAGE_RATE_EUR_H = 16.50
DIRECT_ENERGY_EUR_MW = 2500

# Fixed Cost Assumptions
FIXED_COST_EUR_YR = 1200000  # €1.2M annually (scaled for 250MW)
MAINTENANCE_EUR = 432000
EXTRA_STAFF_EUR = 288000
RENT_OVERHEAD_EUR = 96000
OTHER_FIXED_EUR = 384000

# --- 2. BUILD THE MODEL ---
df = pd.DataFrame({
    'Year': YEARS,
    'Utilization_%': UTILIZATION,
    'Scrap_%': SCRAP_RATE
})

# 1. Capacity Model
df['Max_Capacity_MW'] = MAX_CAPACITY_MW
df['Effective_Capacity_MW'] = df['Max_Capacity_MW'] * df['Utilization_%'] * (1 - df['Scrap_%'])

# 2. Sales Model
df['Price_EUR_MW'] = START_PRICE_EUR_MW * ((1 - PRICE_EROSION) ** (df.index))
df['Revenue_EUR'] = df['Effective_Capacity_MW'] * df['Price_EUR_MW']

# 3. Variable Cost Breakdown (per MW)
direct_labor_eur_mw = HOURS_PER_MW * WAGE_RATE_EUR_H
# Base variable cost includes Materials + Packaging + Labor + Energy
base_variable_cost_mw = DIRECT_MATERIALS_EUR_MW + PACKAGING_EUR_MW + direct_labor_eur_mw + DIRECT_ENERGY_EUR_MW

df['Direct_Labor_EUR_MW'] = direct_labor_eur_mw
df['Direct_Materials_EUR_MW'] = DIRECT_MATERIALS_EUR_MW
df['Packaging_EUR_MW'] = PACKAGING_EUR_MW
df['Direct_Energy_EUR_MW'] = DIRECT_ENERGY_EUR_MW
# Scrap effect applies to the base cost
df['Scrap_Effect_EUR_MW'] = (base_variable_cost_mw / (1 - df['Scrap_%'])) - base_variable_cost_mw
df['Total_Var_Cost_Per_MW'] = base_variable_cost_mw + df['Scrap_Effect_EUR_MW']

# 4. Operating Statement
df['Total_Var_Costs_EUR'] = df['Effective_Capacity_MW'] * df['Total_Var_Cost_Per_MW']
df['Contribution_Margin_EUR'] = df['Revenue_EUR'] - df['Total_Var_Costs_EUR']
df['CM_Pct'] = (df['Contribution_Margin_EUR'] / df['Revenue_EUR']) * 100
df['Fixed_Costs_EUR'] = FIXED_COST_EUR_YR
df['EBITDA_EUR'] = df['Contribution_Margin_EUR'] - df['Fixed_Costs_EUR']

# 5. Break-even Analysis (Year 5)
year_5 = df[df['Year'] == 2030].iloc[0]
q_be = year_5['Fixed_Costs_EUR'] / (year_5['Price_EUR_MW'] - year_5['Total_Var_Cost_Per_MW'])
margin_of_safety = (year_5['Effective_Capacity_MW'] - q_be) / year_5['Effective_Capacity_MW'] * 100

# --- 3. OUTPUT ---
# Export for chart generation
df.to_csv('financial_data.csv', index=False)
print("Model updated with packaging and exported to financial_data.csv")
