import pandas as pd
import numpy as np

# --- 1. ASSUMPTIONS & DRIVERS ---
MACRO_ASSUMPTIONS = {
    'labor_cost_per_hour_eur': 16.50,
    'industrial_electricity_per_kwh_eur': 0.18,
    'annual_price_erosion': 0.02, # 2% YoY price drop
    'tax_rate': 0.0 # 0% CIT in Klaipeda FEZ for first 10 years
}

YEARS = [2026, 2027, 2028, 2029, 2030]
RAMP_UP = [0.50, 0.75, 0.90, 0.95, 1.00]
SCRAP_RATE = [0.05, 0.04, 0.03, 0.02, 0.02]

PRODUCTS = {
    'PV Modules (GW)': {
        'Capacity': 1000, # MW
        'Price_EUR_MW': 120000, # €0.12/W
        'VarCost_EUR_MW': 110000,
        'FixedCost_EUR': 3000000
    },
    'Inverters (GW)': {
        'Capacity': 800, # MW
        'Price_EUR_MW': 45000, # €0.045/W
        'VarCost_EUR_MW': 42000,
        'FixedCost_EUR': 1000000
    },
    'ESS (GWh)': {
        'Capacity': 500, # MWh
        'Price_EUR_MW': 150000, # €150/kWh
        'VarCost_EUR_MW': 142000,
        'FixedCost_EUR': 1000000
    }
}

def build_product_model(product_name, config):
    df = pd.DataFrame({'Year': YEARS, 'Ramp_Up': RAMP_UP, 'Scrap_Rate': SCRAP_RATE})
    df['Product'] = product_name
    df['Max_Capacity'] = config['Capacity']
    df['Effective_Capacity'] = df['Max_Capacity'] * df['Ramp_Up'] * (1 - df['Scrap_Rate'])
    
    # Sales Plan
    df['Units_Sold'] = df['Effective_Capacity']
    df['Price_EUR'] = config['Price_EUR_MW'] * ((1 - MACRO_ASSUMPTIONS['annual_price_erosion']) ** (df.index))
    df['Revenue_EUR'] = df['Units_Sold'] * df['Price_EUR']
    
    # Variable Costs
    df['Unit_Var_Cost_EUR'] = config['VarCost_EUR_MW'] / (1 - df['Scrap_Rate'])
    df['Total_Var_Cost_EUR'] = df['Units_Sold'] * df['Unit_Var_Cost_EUR']
    
    # Financials
    df['Contribution_Margin_EUR'] = df['Revenue_EUR'] - df['Total_Var_Cost_EUR']
    df['Fixed_Costs_EUR'] = config['FixedCost_EUR']
    df['EBITDA_EUR'] = df['Contribution_Margin_EUR'] - df['Fixed_Costs_EUR']
    
    # Break-even
    df['BE_Units'] = df['Fixed_Costs_EUR'] / (df['Price_EUR'] - df['Unit_Var_Cost_EUR'])
    df['BE_Revenue'] = df['BE_Units'] * df['Price_EUR']
    
    return df

# Build models for all products
all_dfs = [build_product_model(name, config) for name, config in PRODUCTS.items()]
total_df = pd.concat(all_dfs).groupby('Year').sum(numeric_only=True).reset_index()

# Recalculate margins and BE for the total project
total_df['Contribution_Margin_Pct'] = total_df['Contribution_Margin_EUR'] / total_df['Revenue_EUR']

# Industry Stress Test (-0.8% margin target)
# If target margin is -0.8%, we check the delta
total_df['Stress_Test_Margin_Delta'] = total_df['Contribution_Margin_Pct'] - (-0.008)

# Export for report generation
print("--- PROJECT OPERATING STATEMENT (TOTAL) ---")
print(total_df[['Year', 'Revenue_EUR', 'Total_Var_Cost_EUR', 'Contribution_Margin_EUR', 'Contribution_Margin_Pct', 'Fixed_Costs_EUR', 'EBITDA_EUR']])

print("\n--- PV MODULES MODEL ---")
print(all_dfs[0][['Year', 'Max_Capacity', 'Ramp_Up', 'Scrap_Rate', 'Effective_Capacity', 'Units_Sold', 'Price_EUR', 'Revenue_EUR']])

print("\n--- INVERTERS MODEL ---")
print(all_dfs[1][['Year', 'Max_Capacity', 'Ramp_Up', 'Scrap_Rate', 'Effective_Capacity', 'Units_Sold', 'Price_EUR', 'Revenue_EUR']])

print("\n--- ESS MODEL ---")
print(all_dfs[2][['Year', 'Max_Capacity', 'Ramp_Up', 'Scrap_Rate', 'Effective_Capacity', 'Units_Sold', 'Price_EUR', 'Revenue_EUR']])

print("\n--- BREAK-EVEN ANALYSIS (Year 2030) ---")
be_2030 = total_df[total_df['Year'] == 2030].iloc[0]
print(f"Total Revenue BE: {be_2030['BE_Revenue']:,.0f}")
print(f"Contribution Margin %: {be_2030['Contribution_Margin_Pct']:.2%}")
