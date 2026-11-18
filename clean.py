"""
Exercise: Clean and Visualize
Module 2 — Advanced Python & Data Handling
Estimated time: 45 minutes

Objective: Clean a messy DataFrame using pandas, then create and save
at least 2 charts using matplotlib.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # saves to file without needing a display
import matplotlib.pyplot as plt

# ============================================================
# Input data — do not modify this
# ============================================================

messy = pd.DataFrame({
    "product": ["Widget A", "Widget B", "widget a", "Widget C", "Widget B",
                "Widget A", " Widget C", "Widget D", None, "Widget A"],
    "sales":   ["150", "200", "175", "300", "200",
                "180", "250", "abc", "100", "-50"],
    "date":    ["2025-01-01", "2025-01-01", "2025-01-02", "2025-01-02", "2025-01-03",
                "2025-01-03", "2025-01-04", "2025-01-04", "2025-01-05", "2025-01-05"],
    "region":  ["North", "South", "north", "East", "South",
                "West", "east", "North", "South", "West"],
})

print("=" * 60)
print("BEFORE CLEANING")
print("=" * 60)
print(f"Shape: {messy.shape}")
print(messy.to_string(index=False))


# ============================================================
# TASK 1 — CLEAN the data
# Work on a copy so the original `messy` is preserved.
# ============================================================

df = messy.copy()   # work on a copy to preserve the original messy DataFrame


df = df.dropna(subset=["product"])      # drop rows where product is missing


df["product"] = df["product"].str.strip().str.title()   # standardize product names
    

df["region"] = df["region"].str.strip().str.title()     # standardize region names
    

df["sales"] = pd.to_numeric(df["sales"], errors="coerce")   # convert sales to numeric, invalid parsing will be set as NaN
df = df.dropna(subset=["sales"])                             # drop rows where sales could not be converted

df = df[df["sales"] >= 0]                                     # remove rows with negative sales

df = df.drop_duplicates()                                     # remove duplicate rows


df["date"] = pd.to_datetime(df["date"])                     # convert date column to datetime type
    
print("\n" + "=" * 60)
print("AFTER CLEANING")
print("=" * 60)

print(f"Shape: {df.shape}")    # print the shape of the cleaned DataFrame
print(df.to_string(index=False))    # print the cleaned DataFrame without the index

# ============================================================
# TASK 2 — ANALYZE & VISUALIZE
# Create at least 2 charts using plt.subplots().
# ============================================================



total_by_product = df.groupby("product")["sales"].sum().sort_values(ascending=False)
daily_sales = df.groupby("date")["sales"].sum()

print("Analysis")
print("=" * 60)
print(f"Total sales by product:")
print(total_by_product.to_string())
print("\nDaily sales totals:")
print(daily_sales.to_string())


fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Widget Sales Analysis", fontsize=14, fontweight="bold")
# Chart 1: Bar chart — total sales by product

axes[0].bar(total_by_product.index, total_by_product.values, color="orange", edgecolor="black")  # create bar chart for total sales by product
axes[0].set_title("Total Sales by Product")    # set title for the first chart
axes[0].set_xlabel("Product")    # set x-axis label for the first chart
axes[0].set_ylabel("Total Sales")  # set y-axis label for the first chart
axes[0].tick_params(axis='x', rotation=15)    # rotate x-axis labels for better readability
# Chart 2: Line chart — daily sales trend

axes[1].plot(daily_sales.index, daily_sales.values, color="green", marker="o", linestyle="-")  # create line chart for daily sales trend
axes[1].set_title("Daily Sales Trend")    # set title for the second chart
axes[1].set_xlabel("Date")               # set x-axis label for the second chart
axes[1].set_ylabel("Daily Total Sales")  # set y-axis label for the second chart
axes[1].tick_params(axis='x', rotation=20)    # rotate x-axis labels for better readability
# Chart 3 (Bonus): Histogram — sales distribution

axes[2].hist(df["sales"], bins=5, color="skyblue", edgecolor="black")  # create histogram for sales distribution
axes[2].set_title("Sales Distribution")    # set title for the third chart
axes[2].set_xlabel("Sales")                # set x-axis label for the third chart
axes[2].set_ylabel("Count")                # set y-axis label for the third chart

plt.tight_layout()

# ============================================================
# TASK 3 — SAVE the chart
# ============================================================

output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "charts.png")


plt.savefig(output_path, dpi=120, bbox_inches="tight")    # save the chart to the specified output path

plt.close()    # close the current figure to free up memory

print(f"Charts saved to: {output_path}")    # print the location where the charts were saved