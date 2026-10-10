#!/usr/bin/env python3
"""
E-commerce Sales Analysis + RFM Customer Segmentation
Dataset: Tableau Sample Superstore (2014-2017)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Project root = parent of scripts/ folder
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"

# ============================================================
# 1. DATA LOADING & CLEANING
# ============================================================

print("=" * 70)
print("1. DATA CLEANING & PREPARATION")
print("=" * 70)

df = pd.read_excel(DATA_DIR / 'Sample_Superstore.xlsx')
print(f"Raw shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Basic info
print("\n--- Missing values ---")
print(df.isnull().sum()[df.isnull().sum() > 0] if df.isnull().sum().sum() > 0 else "No missing values")

print("\n--- Duplicates ---")
print(f"Duplicate rows: {df.duplicated().sum()}")

# Clean
df_clean = df.copy()
df_clean = df_clean.drop_duplicates()
df_clean = df_clean.dropna(subset=['Customer ID', 'Order Date', 'Sales', 'Profit'])

# Ensure correct dtypes
df_clean['Order Date'] = pd.to_datetime(df_clean['Order Date'])
df_clean['Ship Date'] = pd.to_datetime(df_clean['Ship Date'])
df_clean['Postal Code'] = df_clean['Postal Code'].astype(str).str.replace(r'\.0$', '', regex=True)

# Feature engineering
df_clean['Year'] = df_clean['Order Date'].dt.year
df_clean['Month'] = df_clean['Order Date'].dt.month
df_clean['Month_Name'] = df_clean['Order Date'].dt.strftime('%b')
df_clean['Quarter'] = df_clean['Order Date'].dt.quarter
df_clean['Year_Month'] = df_clean['Order Date'].dt.to_period('M').astype(str)
df_clean['Profit_Margin_Pct'] = np.where(df_clean['Sales'] != 0, 
                                          (df_clean['Profit'] / df_clean['Sales']) * 100, 0)
df_clean['Discount_Pct'] = df_clean['Discount'] * 100
df_clean['Order_Value'] = df_clean['Sales']  # line level; will aggregate later

print(f"\nCleaned shape: {df_clean.shape}")
print(f"Date range: {df_clean['Order Date'].min().date()} to {df_clean['Order Date'].max().date()}")
print(f"Unique customers: {df_clean['Customer ID'].nunique()}")
print(f"Unique orders: {df_clean['Order ID'].nunique()}")

# Save cleaned dataset
df_clean.to_csv(DATA_DIR / 'superstore_cleaned.csv', index=False)
print("\nSaved: data/superstore_cleaned.csv")

# ============================================================
# 2. SALES PERFORMANCE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("2. SALES PERFORMANCE ANALYSIS")
print("=" * 70)

# Overall KPIs
total_sales = df_clean['Sales'].sum()
total_profit = df_clean['Profit'].sum()
total_qty = df_clean['Quantity'].sum()
num_orders = df_clean['Order ID'].nunique()
num_customers = df_clean['Customer ID'].nunique()
aov = total_sales / num_orders
overall_margin = (total_profit / total_sales) * 100

print(f"\n--- Overall KPIs ---")
print(f"Total Sales:        ${total_sales:,.2f}")
print(f"Total Profit:       ${total_profit:,.2f}")
print(f"Profit Margin:      {overall_margin:.2f}%")
print(f"Total Quantity:     {total_qty:,}")
print(f"Number of Orders:   {num_orders:,}")
print(f"Number of Customers:{num_customers:,}")
print(f"Average Order Value:${aov:,.2f}")

# Sales & Profit by Year
print("\n--- Yearly Trend ---")
yearly = df_clean.groupby('Year').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Order ID', 'nunique'),
    Quantity=('Quantity', 'sum')
).round(2)
yearly['Profit_Margin_%'] = (yearly['Profit'] / yearly['Sales'] * 100).round(2)
print(yearly)

# Monthly trend (last year for example)
print("\n--- Monthly Sales Trend (All Years) ---")
monthly = df_clean.groupby(['Year', 'Month']).agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum')
).reset_index()
print(monthly.tail(12).to_string(index=False))

# By Category
print("\n--- Sales & Profit by Category ---")
cat = df_clean.groupby('Category').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Quantity=('Quantity', 'sum'),
    Orders=('Order ID', 'nunique')
).round(2)
cat['Profit_Margin_%'] = (cat['Profit'] / cat['Sales'] * 100).round(2)
cat = cat.sort_values('Sales', ascending=False)
print(cat)

# By Sub-Category
print("\n--- Top 10 Sub-Categories by Sales ---")
sub = df_clean.groupby(['Category', 'Sub-Category']).agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Quantity=('Quantity', 'sum')
).round(2)
sub['Profit_Margin_%'] = (sub['Profit'] / sub['Sales'] * 100).round(2)
sub = sub.sort_values('Sales', ascending=False)
print(sub.head(10))

print("\n--- Bottom 5 Sub-Categories by Profit ---")
print(sub.sort_values('Profit').head(5))

# By Region
print("\n--- Sales & Profit by Region ---")
reg = df_clean.groupby('Region').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Order ID', 'nunique'),
    Customers=('Customer ID', 'nunique')
).round(2)
reg['Profit_Margin_%'] = (reg['Profit'] / reg['Sales'] * 100).round(2)
reg = reg.sort_values('Sales', ascending=False)
print(reg)

# By Segment
print("\n--- Sales & Profit by Customer Segment ---")
seg = df_clean.groupby('Segment').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Order ID', 'nunique'),
    Customers=('Customer ID', 'nunique')
).round(2)
seg['Profit_Margin_%'] = (seg['Profit'] / seg['Sales'] * 100).round(2)
print(seg.sort_values('Sales', ascending=False))

# Top / Bottom Products
print("\n--- Top 10 Products by Sales ---")
prod = df_clean.groupby('Product Name').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Quantity=('Quantity', 'sum')
).round(2)
prod['Profit_Margin_%'] = (prod['Profit'] / prod['Sales'] * 100).round(2)
print(prod.sort_values('Sales', ascending=False).head(10))

print("\n--- Bottom 10 Products by Profit (biggest losses) ---")
print(prod.sort_values('Profit').head(10))

# Discount impact
print("\n--- Impact of Discount on Profit ---")
df_clean['Discount_Bucket'] = pd.cut(df_clean['Discount'], 
                                      bins=[-0.01, 0, 0.2, 0.4, 0.6, 1.0],
                                      labels=['0%', '1-20%', '21-40%', '41-60%', '61-100%'])
disc = df_clean.groupby('Discount_Bucket', observed=True).agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Order ID', 'nunique'),
    Avg_Margin=('Profit_Margin_Pct', 'mean')
).round(2)
disc['Profit_Margin_%'] = (disc['Profit'] / disc['Sales'] * 100).round(2)
print(disc)

# Shipping Mode
print("\n--- Shipping Mode Performance ---")
ship = df_clean.groupby('Ship Mode').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Order ID', 'nunique'),
    Avg_Days=('Ship Date', lambda x: (x - df_clean.loc[x.index, 'Order Date']).dt.days.mean())
).round(2)
ship['Profit_Margin_%'] = (ship['Profit'] / ship['Sales'] * 100).round(2)
print(ship.sort_values('Sales', ascending=False))

# ============================================================
# 3. RFM CUSTOMER SEGMENTATION
# ============================================================

print("\n" + "=" * 70)
print("3. RFM CUSTOMER SEGMENTATION")
print("=" * 70)

# Analysis date = day after last order
snapshot_date = df_clean['Order Date'].max() + timedelta(days=1)
print(f"Snapshot date for Recency: {snapshot_date.date()}")

# Aggregate to customer level
# First aggregate to order level then customer
order_level = df_clean.groupby(['Customer ID', 'Order ID', 'Order Date']).agg(
    Order_Sales=('Sales', 'sum'),
    Order_Profit=('Profit', 'sum'),
    Order_Qty=('Quantity', 'sum')
).reset_index()

rfm = order_level.groupby('Customer ID').agg(
    Recency=('Order Date', lambda x: (snapshot_date - x.max()).days),
    Frequency=('Order ID', 'nunique'),
    Monetary=('Order_Sales', 'sum')
).reset_index()

print(f"\nRFM table shape: {rfm.shape}")
print(rfm.describe().round(2))

# Score 1-5 (quintiles)
# Recency: lower is better → reverse score
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)

rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
rfm['RFM_Total'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']

# Segment mapping (classic RFM segments)
def rfm_segment(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif r >= 3 and f >= 3 and m >= 3:
        return 'Loyal Customers'
    elif r >= 4 and f <= 2:
        return 'Potential Loyalists'
    elif r >= 3 and f <= 2 and m >= 3:
        return 'Promising'
    elif r >= 4 and f >= 2 and m <= 2:
        return 'New Customers'
    elif r <= 2 and f >= 3 and m >= 3:
        return 'At Risk'
    elif r <= 2 and f >= 2 and m >= 2:
        return 'Need Attention'
    elif r <= 2 and f <= 2 and m >= 3:
        return 'About to Sleep'
    elif r <= 2 and f <= 2 and m <= 2:
        return 'Hibernating'
    else:
        return 'Others'

rfm['Segment'] = rfm.apply(rfm_segment, axis=1)

# Better / more standard segment labels often used
def segment_label(row):
    score = row['RFM_Total']
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif r >= 3 and f >= 4 and m >= 4:
        return 'Loyal Customers'
    elif r >= 4 and f >= 2 and m >= 2:
        return 'Potential Loyalists'
    elif r >= 4 and f <= 2:
        return 'New Customers'
    elif r >= 3 and f <= 2 and m <= 2:
        return 'Promising'
    elif r <= 2 and f >= 3 and m >= 3:
        return 'At Risk'
    elif r <= 2 and f >= 2:
        return 'Need Attention'
    elif r <= 2 and f <= 2 and m >= 3:
        return 'About to Sleep'
    elif r <= 2 and f <= 2 and m <= 2:
        return 'Hibernating / Lost'
    else:
        return 'Others'

rfm['Segment'] = rfm.apply(segment_label, axis=1)

print("\n--- Segment Distribution ---")
seg_summary = rfm.groupby('Segment').agg(
    Customers=('Customer ID', 'count'),
    Avg_Recency=('Recency', 'mean'),
    Avg_Frequency=('Frequency', 'mean'),
    Avg_Monetary=('Monetary', 'mean'),
    Total_Revenue=('Monetary', 'sum')
).round(2)
seg_summary['Pct_Customers'] = (seg_summary['Customers'] / seg_summary['Customers'].sum() * 100).round(1)
seg_summary['Pct_Revenue'] = (seg_summary['Total_Revenue'] / seg_summary['Total_Revenue'].sum() * 100).round(1)
seg_summary = seg_summary.sort_values('Total_Revenue', ascending=False)
print(seg_summary)

# Pareto check
rfm_sorted = rfm.sort_values('Monetary', ascending=False)
rfm_sorted['Cum_Revenue'] = rfm_sorted['Monetary'].cumsum()
rfm_sorted['Cum_Pct'] = rfm_sorted['Cum_Revenue'] / rfm_sorted['Monetary'].sum() * 100
top20_idx = int(len(rfm_sorted) * 0.2)
top20_rev_pct = rfm_sorted.iloc[top20_idx]['Cum_Pct']
print(f"\n--- Pareto (80/20) Check ---")
print(f"Top 20% customers contribute {top20_rev_pct:.1f}% of total revenue")

# Merge segment back for enriched customer view
customer_info = df_clean.groupby('Customer ID').agg(
    Customer_Name=('Customer Name', 'first'),
    Segment_Demo=('Segment', lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0]),
    Region=('Region', lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0]),
    Preferred_Category=('Category', lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0])
).reset_index()

rfm_full = rfm.merge(customer_info, on='Customer ID', how='left')
rfm_full.to_csv(DATA_DIR / 'rfm_scored_customers.csv', index=False)
print("\nSaved: data/rfm_scored_customers.csv")

# Segment summary for dashboard
seg_summary.to_csv(DATA_DIR / 'rfm_segment_summary.csv')
print("Saved: data/rfm_segment_summary.csv")

# ============================================================
# 4. BUSINESS INSIGHTS
# ============================================================

print("\n" + "=" * 70)
print("4. KEY BUSINESS INSIGHTS & RECOMMENDATIONS")
print("=" * 70)

insights = []

# Insight 1
insights.append(
    f"1. Overall Performance: The Superstore generated ${total_sales:,.0f} in sales and "
    f"${total_profit:,.0f} in profit ({overall_margin:.1f}% margin) across {num_orders:,} orders "
    f"from {num_customers:,} customers. Average Order Value is ${aov:.2f}."
)

# Insight 2 - Category
tech_profit = cat.loc['Technology', 'Profit'] if 'Technology' in cat.index else 0
furn_margin = cat.loc['Furniture', 'Profit_Margin_%'] if 'Furniture' in cat.index else 0
insights.append(
    f"2. Category Profitability: Technology is the most profitable category. "
    f"Furniture has high sales but the lowest profit margin ({furn_margin:.1f}%), "
    f"largely driven by heavy discounting on Tables and Bookcases."
)

# Insight 3 - Region
best_region = reg.index[0]
insights.append(
    f"3. Regional Performance: {best_region} is the top-performing region by sales. "
    f"Focus growth and inventory investments there while investigating under-performing regions "
    f"for pricing, assortment, or shipping issues."
)

# Insight 4 - Discount
high_disc_margin = disc.loc['41-60%', 'Profit_Margin_%'] if '41-60%' in disc.index else -50
insights.append(
    f"4. Discount Impact: Discounts above 20% sharply erode margins. Orders with 41-60% discount "
    f"show significantly negative or near-zero profit margins. Implement stricter discount guardrails "
    f"and consider value-based promotions instead of deep cuts."
)

# Insight 5 - RFM Pareto
insights.append(
    f"5. Customer Concentration (Pareto): The top 20% of customers generate approximately "
    f"{top20_rev_pct:.0f}% of total revenue. Prioritize retention and exclusive offers for Champions "
    f"and Loyal Customers."
)

# Insight 6 - At Risk
at_risk = seg_summary.loc[seg_summary.index.str.contains('At Risk|Need Attention', case=False, na=False)]
if not at_risk.empty:
    ar_cust = at_risk['Customers'].sum()
    ar_rev = at_risk['Total_Revenue'].sum()
    insights.append(
        f"6. At-Risk / Need Attention Segments: These customers still represent meaningful revenue "
        f"(~${ar_rev:,.0f}). Targeted win-back campaigns (personalized offers, free shipping, "
        f"loyalty points) can recover high-value relationships at relatively low cost."
    )
else:
    insights.append(
        "6. At-Risk Customers: A meaningful portion of previously frequent buyers have not purchased "
        "recently. Re-engagement campaigns focused on their preferred categories can recover revenue."
    )

# Insight 7 - Shipping
insights.append(
    "7. Shipping Mode: Standard Class dominates volume. Same Day and First Class have higher "
    "per-order costs but may support higher-margin Technology products. Optimize shipping rules "
    "by product margin and customer segment."
)

# Insight 8 - Recommendations summary
insights.append(
    "8. Recommended Actions:\n"
    "   • Protect Champions & Loyalists with VIP programs and early access.\n"
    "   • Run targeted re-activation for At Risk / Hibernating high-monetary customers.\n"
    "   • Reduce deep discounts on Furniture (especially Tables/Bookcases); test bundles.\n"
    "   • Double down on Technology assortment and West region inventory.\n"
    "   • Monitor AOV and introduce order-value thresholds for free shipping / free gifts."
)

for i in insights:
    print(f"\n{i}")

# Save insights
with open(DOCS_DIR / 'business_insights.md', 'w') as f:
    f.write("# Business Insights & Recommendations\n\n")
    f.write(f"**Dataset:** Tableau Sample Superstore (Order dates {df_clean['Order Date'].min().date()} – {df_clean['Order Date'].max().date()})\n\n")
    f.write("## Key Metrics\n")
    f.write(f"- Total Sales: ${total_sales:,.2f}\n")
    f.write(f"- Total Profit: ${total_profit:,.2f}\n")
    f.write(f"- Profit Margin: {overall_margin:.2f}%\n")
    f.write(f"- Orders: {num_orders:,}\n")
    f.write(f"- Customers: {num_customers:,}\n")
    f.write(f"- AOV: ${aov:.2f}\n\n")
    f.write("## Insights\n\n")
    for ins in insights:
        f.write(ins + "\n\n")

print("\nSaved: docs/business_insights.md")

# ============================================================
# 5. EXPORTS FOR DASHBOARD / POWER BI
# ============================================================

print("\n" + "=" * 70)
print("5. EXPORTING FILES FOR DASHBOARD")
print("=" * 70)

# Monthly sales for trend
monthly_export = df_clean.groupby(['Year', 'Month', 'Year_Month']).agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Quantity=('Quantity', 'sum'),
    Orders=('Order ID', 'nunique')
).reset_index()
monthly_export.to_csv(DATA_DIR / 'monthly_sales.csv', index=False)

# Category x Region
cat_reg = df_clean.groupby(['Category', 'Region']).agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Quantity=('Quantity', 'sum')
).reset_index()
cat_reg.to_csv(DATA_DIR / 'category_region.csv', index=False)

# Product performance
prod_export = prod.reset_index().sort_values('Sales', ascending=False)
prod_export.to_csv(DATA_DIR / 'product_performance.csv', index=False)

print("Exported supporting CSVs for Power BI / Tableau:")
print("  - monthly_sales.csv")
print("  - category_region.csv")
print("  - product_performance.csv")
print("  - rfm_scored_customers.csv")
print("  - rfm_segment_summary.csv")
print("  - superstore_cleaned.csv")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
