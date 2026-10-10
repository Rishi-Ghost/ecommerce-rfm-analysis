# E-commerce Sales Analysis + RFM Customer Segmentation

**End-to-end retail analytics project** using the classic Tableau Sample Superstore dataset (2014–2017).  
Focus: sales performance deep-dive + actionable RFM customer segmentation to drive revenue growth and retention.

---

## Project Goal

Analyze e-commerce / retail sales data to understand business performance and segment customers using **RFM analysis** so the company can increase revenue and improve customer retention.

---

## Dataset

- **Source**: Tableau Sample Superstore  
- **Period**: 2014-01-03 → 2017-12-30  
- **Rows**: 9,994 order lines  
- **Customers**: 793 unique  
- **Orders**: 5,009  
- **Key fields**: Order Date, Customer ID, Category, Sub-Category, Region, Segment, Ship Mode, Sales, Quantity, Discount, Profit

Raw file: `data/Sample_Superstore.xlsx`  
Cleaned file: `data/superstore_cleaned.csv`

---

## What Was Built

### 1. Data Cleaning & Feature Engineering
- No missing values or duplicates in source
- Created: Year, Month, Quarter, Year-Month, Profit Margin %, Discount %, Order Value helpers

### 2. Sales Performance Analysis
- Overall KPIs (Sales, Profit, Margin, Orders, AOV)
- Yearly & monthly trends
- Performance by Category, Sub-Category, Region, Segment
- Top / Bottom products
- Discount impact on profit
- Shipping mode performance

### 3. RFM Customer Segmentation (Core Deliverable)
For every customer:
| Metric    | Definition                                      |
|-----------|-------------------------------------------------|
| Recency   | Days since last purchase (lower = better)       |
| Frequency | Number of distinct orders                       |
| Monetary  | Total sales value                               |

- Quintile scores (1–5) for R, F, M  
- Combined RFM Score + business segments:
  - Champions
  - Loyal Customers
  - Potential Loyalists
  - New Customers
  - Promising
  - At Risk
  - Need Attention
  - About to Sleep
  - Hibernating / Lost

Segment-level metrics: customer count, revenue contribution, avg monetary, avg frequency, avg recency.

### 4. Business Insights & Recommendations
See `docs/business_insights.md` for the full write-up (8 key insights).

### 5. Dashboard-Ready Data Exports
All CSVs needed to build a 3–4 page interactive dashboard in **Power BI** or **Tableau**:

| File                              | Purpose                                      |
|-----------------------------------|----------------------------------------------|
| `superstore_cleaned.csv`          | Main fact table                              |
| `rfm_scored_customers.csv`        | Customer-level RFM + segment                 |
| `rfm_segment_summary.csv`         | Segment KPIs                                 |
| `monthly_sales.csv`               | Trend charts                                 |
| `category_region.csv`             | Heatmaps / bar charts                        |
| `product_performance.csv`         | Top / bottom products                        |

---

## Key Results (Snapshot)

| Metric                  | Value              |
|-------------------------|--------------------|
| Total Sales             | $2,297,201         |
| Total Profit            | $286,397           |
| Overall Margin          | 12.47%             |
| Orders                  | 5,009              |
| Customers               | 793                |
| Average Order Value     | $458.61            |
| Top Region              | West               |
| Most Profitable Category| Technology (17.4%) |
| Lowest Margin Category  | Furniture (2.5%)   |
| Top 20% Customers Rev.  | ~48% of revenue    |

---

## How to Reproduce

```bash
# 1. Clone / open the repo
cd ecommerce-rfm-project

# 2. Install dependencies
pip install pandas numpy openpyxl

# 3. Run the full analysis
python scripts/ecommerce_analysis.py
# (or run the notebook version if preferred)
```

All outputs are written to `data/` and `docs/`.

---

## Dashboard Build Guide (Power BI / Tableau)

### Recommended Pages

**Page 1 – Sales Overview**
- KPI cards: Total Sales, Profit, # Orders, AOV, Profit Margin %
- Line chart: Sales & Profit by Year-Month
- Bar / Map: Sales by Region
- Stacked bar: Sales by Category
- Table: Top 10 Products

**Page 2 – Customer Segmentation (RFM)**
- Donut / bar: # Customers by Segment
- Bar: Revenue contribution by Segment
- Scatter or bar: Avg Monetary vs Frequency by Segment
- Filters: Year, Region, Category (via relationships)
- Table: Segment summary (customers, revenue %, avg R/F/M)

**Page 3 – Product & Profitability**
- Tree map or bar: Category → Sub-Category sales & profit
- Scatter: Discount % vs Profit Margin (color by Category)
- Table: Lowest profit / loss-making products
- Shipping Mode performance

**Page 4 – Insights & Recommendations** (text + key callouts)
- Paste the 8 insights from `docs/business_insights.md`
- Add action items with owners / priority

**Relationships**
- `superstore_cleaned[Customer ID]` → `rfm_scored_customers[Customer ID]`
- Use `Order Date` for time intelligence

---

## Project Structure

```
ecommerce-rfm-project/
├── data/
│   ├── Sample_Superstore.xlsx          # Raw
│   ├── superstore_cleaned.csv          # Cleaned + engineered
│   ├── rfm_scored_customers.csv        # RFM + segments
│   ├── rfm_segment_summary.csv
│   ├── monthly_sales.csv
│   ├── category_region.csv
│   └── product_performance.csv
├── docs/
│   ├── business_insights.md
│   └── resume_bullets.md
├── scripts/
│   └── ecommerce_analysis.py           # Full reproducible script
├── notebooks/                          # (optional) Jupyter versions
├── dashboard/                          # Place .pbix / .twbx here
└── README.md
```

---

## Tools Used

- Python 3 (pandas, numpy)
- Excel / openpyxl for source
- Designed for Power BI or Tableau (dashboard)

---

## Author Notes

This project demonstrates:
- End-to-end data cleaning & feature engineering
- Classic sales analytics (trends, category, region, discount impact)
- Production-ready RFM scoring and business-oriented segmentation
- Clear, actionable insights that a marketing / sales team can use immediately
- Dashboard-ready data model

Feel free to extend with cohort analysis, CLV estimation, or predictive churn models.
