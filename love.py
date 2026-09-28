import pandas as pd
import numpy as np

# 1. Step: Load & Clean Data
url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
df = pd.read_csv(url)

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].str.strip(), errors='coerce')
df['TotalCharges'] = df['TotalCharges'].fillna(0)

df['MRR'] = df['MonthlyCharges']
df['ARR'] = df['MonthlyCharges'] * 12

# 2. Step: Contract Grouping
contract_analysis = df.groupby('Contract').agg(
    Customer_Count=('customerID', 'count'),
    Total_ARR=('ARR', 'sum'),
    Avg_MRR=('MRR', 'mean')
).reset_index()

total_company_arr = df['ARR'].sum()
contract_analysis['ARR_Share_%'] = (contract_analysis['Total_ARR'] / total_company_arr) * 100

contract_analysis['Total_ARR'] = contract_analysis['Total_ARR'].round(2)
contract_analysis['Avg_MRR'] = contract_analysis['Avg_MRR'].round(2)
contract_analysis['ARR_Share_%'] = contract_analysis['ARR_Share_%'].round(2)

# --- OUTOUT: MUST USE PRINT STATEMENT ---
#print("\n" + "="*50)
#print("=== Step 2: Revenue Concentration by Contract Type ===")
#print("="*50)
#print(contract_analysis)
#print("="*50 + "\n")

# === STEP 3: Churn & Financial Leakage Analysis ===

# 1. Aggregation Engine
churn_analysis = df.groupby('Churn').agg(
    Customer_Count=('customerID', 'count'),
    Total_ARR=('ARR', 'sum'),
    Avg_MRR=('MRR', 'mean')
).reset_index()

# 2. Vectorized Percentage Computation
total_company_arr = df['ARR'].sum()
churn_analysis['ARR_Share_%'] = (churn_analysis['Total_ARR'] / total_company_arr) * 100

# 3. Floating Point Precision & Formatting
churn_analysis['Total_ARR'] = churn_analysis['Total_ARR'].round(2)
churn_analysis['Avg_MRR'] = churn_analysis['Avg_MRR'].round(2)
churn_analysis['ARR_Share_%'] = churn_analysis['ARR_Share_%'].round(2)

#print(churn_analysis)

# === STEP 4: Customer Cohort & Tenure Analysis ===

# 1. Define Tenure Bins and Labels using pd.cut
bins = [-1, 12, 24, 48, 72]
labels = ['0-1 Year (0-12m)', '1-2 Years (13-24m)', '2-4 Years (25-48m)', '4-6 Years (49-72m)']

df['Tenure_Cohort'] = pd.cut(df['tenure'], bins=bins, labels=labels)

# 2. Aggregation Engine: Cohort-level Financial Breakdown
cohort_analysis = df.groupby('Tenure_Cohort', observed=False).agg(
    Total_Customers=('customerID', 'count'),
    Churned_Customers=('Churn', lambda x: (x == 'Yes').sum()),
    Total_ARR=('ARR', 'sum'),
    Avg_MRR=('MRR', 'mean')
).reset_index()

# 3. Vectorized Rate Computations
cohort_analysis['Churn_Rate_%'] = (cohort_analysis['Churned_Customers'] / cohort_analysis['Total_Customers']) * 100
cohort_analysis['ARR_Share_%'] = (cohort_analysis['Total_ARR'] / df['ARR'].sum()) * 100

# 4. Precision Formatting
cohort_analysis['Churn_Rate_%'] = cohort_analysis['Churn_Rate_%'].round(2)
cohort_analysis['ARR_Share_%'] = cohort_analysis['ARR_Share_%'].round(2)
cohort_analysis['Total_ARR'] = cohort_analysis['Total_ARR'].round(2)
cohort_analysis['Avg_MRR'] = cohort_analysis['Avg_MRR'].round(2)

#print("\n" + "="*70)
#print("=== Step 4: Customer Cohort & Tenure Analysis ===")
#print("="*70)
#print(cohort_analysis)
#print("="*70 + "\n")

import duckdb

# === STEP 5: SQL Automation Engine (DuckDB Integration) ===

# 1. SQL Query for Executive Metric Summaries
sql_query = """
SELECT 
    Contract,
    COUNT(customerID) AS Total_Customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS Churn_Count,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(customerID), 2) AS Churn_Rate_Pct,
    ROUND(SUM(ARR), 2) AS Contract_ARR,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN ARR ELSE 0 END), 2) AS Financial_Leakage_ARR,
    ROUND(AVG(MRR), 2) AS Avg_MRR
FROM df
GROUP BY Contract
ORDER BY Financial_Leakage_ARR DESC;
"""

# 2. Execute SQL query directly against the Pandas DataFrame 'df'
sql_executive_summary = duckdb.query(sql_query).df()

print("\n" + "="*80)
print("=== Step 5: Automated SQL Executive Summary (DuckDB Engine) ===")
print("="*80)
print(sql_executive_summary)
print("="*80 + "\n")