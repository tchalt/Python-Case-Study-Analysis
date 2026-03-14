import pandas as pd
import numpy as np

# --- 1. ASSUMPTIONS & DRIVERS (Step 8) ---
TECH_DATA = {
    'module_efficiency': 0.248, # HPBC 2.0 mass production
    'base_price_pv_mw': 120000, # €0.12/W
    'base_price_inverter_mw': 80000,
    'base_price_ess_mwh': 110000,
    'annual_price_erosion': 0.02, # 2% price drop due to market competition
    'hpbc_premium_pct': 0.05 # 5% premium for high efficiency to offset erosion
}

COST_DRIVERS = {
    'labor_hourly_rate_eur': 7.05, # Minimum hourly wage, Valstybinė darbo inspekcija, 2026 Jan
    'electricity_kwh_eur': 0.18, # Klaipeda FEZ Industrial rate
    'materials_pct_of_rev_base': 0.82, # Industry benchmark
}

YEARS = [2026, 2027, 2028, 2029, 2030]
MAX_CAP_MW = 2300 # Combined total capacity (Modules + Inverters + ESS)
UTIL_SCHEDULE = [0.50, 0.75, 0.90, 0.95, 1.00]
SCRAP_SCHEDULE = [0.05, 0.04, 0.03, 0.02, 0.02]

def calculate_refined_plan():
    data = []
    for i, year in enumerate(YEARS):
        # Step 2: Capacity
        eff_cap = MAX_CAP_MW * UTIL_SCHEDULE[i] * (1 - SCRAP_SCHEDULE[i])
        
        # Step 3: Sales
        # Price includes HPBC 2.0 premium and erosion
        base_price = TECH_DATA['base_price_pv_mw'] * ((1 - TECH_DATA['annual_price_erosion'])**i)
        premium_price = base_price * (1 + TECH_DATA['hpbc_premium_pct'])
        revenue = eff_cap * premium_price
        
        # Step 4: Variable Costs (Inflated by Scrap)
        # Includes Materials, Labor, Energy
        # Materials base: TECH_DATA['base_price_pv_mw'] * 0.72 (reduced to allow for labor/energy)
        mat_efficiency_gain = (1 - 0.005)**i
        base_mat_cost = (TECH_DATA['base_price_pv_mw'] * 0.72 * mat_efficiency_gain)
        
        # Labor: 800 hours/MW * labor_rate
        labor_cost_unit = 800 * COST_DRIVERS['labor_hourly_rate_eur']
        
        # Energy: 14,000 kWh/MW * energy_rate
        energy_cost_unit = 14000 * COST_DRIVERS['electricity_kwh_eur']
        
        base_v_cost_unit = base_mat_cost + labor_cost_unit + energy_cost_unit
        
        # Adjusted for scrap
        adj_v_cost_unit = base_v_cost_unit / (1 - SCRAP_SCHEDULE[i])
        total_v_cost = eff_cap * adj_v_cost_unit
        
        # Step 5: Fixed Costs (Maintenance, Staff, Insurance)
        # Incremental staff/maintenance
        fixed_costs = 5000000 if i == 0 else 5500000 
        
        # Step 6: Operating Statement
        contrib_margin = revenue - total_v_cost
        ebitda = contrib_margin - fixed_costs
        
        data.append({
            'Year': year,
            'Util_Pct': UTIL_SCHEDULE[i],
            'Scrap_Pct': SCRAP_SCHEDULE[i],
            'Eff_Cap_MW': round(eff_cap, 1),
            'Price_EUR_MW': round(premium_price, 0),
            'Revenue_EUR': round(revenue, 0),
            'Var_Cost_Unit': round(adj_v_cost_unit, 0),
            'Total_Var_Cost': round(total_v_cost, 0),
            'Contrib_Margin': round(contrib_margin, 0),
            'Contrib_Margin_Pct': round((contrib_margin / revenue) * 100, 2),
            'Fixed_Costs': round(fixed_costs, 0),
            'EBITDA': round(ebitda, 0)
        })
    
    df = pd.DataFrame(data)
    
    # Step 7: Break-even for Year 2030
    be_2030_price = df.iloc[-1]['Price_EUR_MW']
    be_2030_vcost = df.iloc[-1]['Var_Cost_Unit']
    be_2030_fixed = df.iloc[-1]['Fixed_Costs']
    
    q_be = be_2030_fixed / (be_2030_price - be_2030_vcost)
    rev_be = q_be * be_2030_price
    
    return df, q_be, rev_be

# Execute and output
refined_df, q_be, rev_be = calculate_refined_plan()

print("--- REFINED OPERATING STATEMENT ---")
print(refined_df.to_string(index=False))
print(f"\nBreak-even Units (2030): {q_be:,.1f} MW")
print(f"Break-even Revenue (2030): €{rev_be:,.0f}")
