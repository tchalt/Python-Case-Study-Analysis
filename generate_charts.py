import matplotlib.pyplot as plt
import pandas as pd
import os

# Ensure the working directory is correct
working_dir = "/Users/tangtaowei/Desktop/IE/Mar 17"
os.chdir(working_dir)

# Load data from the model
df = pd.read_csv('financial_data.csv')

years = df['Year'].astype(int).tolist()
revenue = (df['Revenue_EUR'] / 1e6).tolist() # Million EUR
ebitda = (df['EBITDA_EUR'] / 1e6).tolist() # Million EUR
total_costs = ((df['Total_Var_Costs_EUR'] + df['Fixed_Costs_EUR']) / 1e6).tolist() # Million EUR
eff_capacity_mw = df['Effective_Capacity_MW'].tolist()

# --- Chart 1: Volume Ramp-up ---
plt.figure(figsize=(10, 6))
bars = plt.bar(years, eff_capacity_mw, color='#3498db', label='Effective Capacity (MW)', alpha=0.8)
plt.plot(years, eff_capacity_mw, marker='o', color='#2c3e50', linewidth=2, markersize=8)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, f'{yval:,.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.title("Production Volume Ramp-up (2026-2030) - 250MW Scale", fontsize=14, fontweight='bold')
plt.xlabel("Year", fontsize=12)
plt.ylabel("Effective Capacity (MW)", fontsize=12)
plt.ylim(0, 300)
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('volume_rampup.png', dpi=300)
print("Updated: volume_rampup.png")

# --- Chart 2: Revenue vs. Total Costs (Break-even Path) ---
plt.figure(figsize=(10, 6))
plt.plot(years, revenue, label='Total Revenue', marker='s', color='#27ae60', linewidth=3)
plt.plot(years, total_costs, label='Total Operating Costs', marker='x', color='#c0392b', linewidth=3)

# Fill EBITDA Area
plt.fill_between(years, revenue, total_costs, color='#e9f7ef', alpha=0.7, label='Operating Profit (EBITDA)')

# Data Annotations
plt.annotate(f'2030 EBITDA: €{ebitda[-1]:.1f}M', 
             xy=(2030, revenue[-1]), xytext=(2028, revenue[-1] * 0.8),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6),
             fontsize=11, fontweight='bold', color='#1e8449')

plt.title("Revenue vs. Total Costs: Profitability Path (2026-2030)", fontsize=14, fontweight='bold')
plt.xlabel("Year", fontsize=12)
plt.ylabel("Million EUR (€)", fontsize=12)
plt.xticks(years, years)
plt.grid(True, linestyle=':', alpha=0.5)
plt.legend(loc='upper left', frameon=True, shadow=True)
plt.tight_layout()
plt.savefig('breakeven_chart.png', dpi=300)
print("Updated: breakeven_chart.png")
