

markdown
# SaaS Financial Performance, Unit Economics & Revenue Leakage Analysis

## Executive Summary
This project evaluates portfolio revenue durability, contract concentration risk, and churn-driven financial leakage for a SaaS subscription business managing **$5.47M in Annual Recurring Revenue (ARR)** across 7,043 active accounts. 

By combining an optimized Python/Pandas data pipeline with an in-memory ANSI SQL aggregation engine (**DuckDB**), this project bridges technical data engineering and strategic Financial Planning & Analysis (FP&A). The analysis pinpoints core operational bottlenecks—isolating **$1.67M in annual revenue leakage**—and delivers C-suite executive recommendations to stabilize cash flows and improve unit economics.

---

## Technical Stack & Architecture
* **Language:** Python 3.10+
* **Data Manipulation & Vectorization:** `pandas`, `numpy` (Named aggregations, `pd.cut` binning, SIMD-accelerated array math)
* **SQL Aggregation Engine:** `duckdb` (Zero-copy in-memory querying over DataFrame memory pointers)
* **Environment:** Visual Studio Code / Jupyter Notebook

---

## Key Financial Findings

### 1. High Revenue Concentration & Contract Exposure
* **Portfolio Scale:** Total Portfolio ARR stands at **$5.47M** derived from an MRR baseline of **$456.12K**.
* **Contract Risk:** **56.41% ($3.09M ARR)** of total recurring revenue is tied to short-term **Month-to-month** contracts, exposing over half of company cash flows to immediate cancellation risk.

### 2. Severe Financial Leakage ($1.67M ARR Loss)
* **Revenue Churn:** The company suffers an annual financial leakage of **$1.67M ARR (30.50% of total revenue)** driven by 1,869 churned accounts.
* **Premium Tier Decay:** Churned subscribers generate a higher average monthly billing (**$74.44 Avg MRR**) than retained subscribers (**$61.27 Avg MRR**), proving that churn disproportionately impacts high-tier, valuable customer segments.

### 3. Lifecycle & Onboarding Bottlenecks
* **First-Year Friction:** The **0–1 Year (0–12m)** cohort exhibits a critical **47.44% churn rate**, indicating that nearly half of new subscribers cancel before the company recovers its Customer Acquisition Cost (CAC).
* **LTV Expansion:** Retention stabilizes past 24 months. The **4–6 Years** cohort accounts for **36.30% ($1.99M ARR)** of portfolio revenue with an elite **9.51%** churn rate.

### 4. Root Cause Isolation via In-Memory SQL Engine (DuckDB)
* **Contract Leakage Concentration:** **86.86% ($1.45M)** of all lost ARR originates directly from the **Month-to-month** segment (42.71% segment churn rate).
* **Multi-Year Protection:** Two-Year contracts restrict annual loss to just **$49.98K (2.83% churn rate)**, proving the stabilizing power of long-term contract lock-ins.

---

## Executive Summary Table (SQL Output)

| Contract | Total Customers | Churn Count | Churn Rate (%) | Contract ARR ($) | Financial Leakage ARR ($) | Avg MRR ($) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Month-to-month** | 3,875 | 1,655 | 42.71% | $3,087,529.80 | **$1,450,165.20** | $66.40 |
| **One year** | 1,473 | 166 | 11.27% | $1,149,799.20 | $169,421.40 | $65.05 |
| **Two year** | 1,695 | 48 | 2.83% | $1,236,070.20 | $49,983.60 | $60.77 |

---

## Strategic Recommendations for C-Suite Leadership

1. **Incentivize Annual Contract Migration:** Introduce a targeted 5–10% discount for converting Month-to-month subscribers into 1-Year or 2-Year commitments. Converting just 20% of monthly accounts would immediately safeguard **~$290K+ in ARR**.
2. **Overhaul Early Onboarding (0–12m):** Reallocate Customer Success resources toward first-year onboarding programs to reduce the 47.44% initial churn rate, accelerating CAC payback recovery.
3. **Address High-Tier Price Sensitivity:** Conduct a feature-utilization audit on premium packages ($74.44+ MRR) to fix potential value-realization gaps causing top-tier account churn.

```
