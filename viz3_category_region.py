"""
DS4200 Group Project — Viz 3: Category & Region Profit Comparison
Author: Yuansi Jiang

Narrative beat : "Where do we win or lose structurally?"
Chart type     : Faceted horizontal bar chart (one panel per Category)
                 Bars sorted by profit, colored red/teal by profit sign
Interactions   : Region dropdown filter + hover tooltip
Output         : viz3_category_region.json  ← Ryan embeds this in index.html

Also prints: recommended subgroup for Ryan's D3 deep dive (Viz 5)

Usage:
    python data_cleaning.py        # run first to generate superstore_clean.csv
    python viz3_category_region.py
"""

import pandas as pd
import altair as alt

INPUT_FILE  = "superstore_clean.csv"
OUTPUT_FILE = "viz3_category_region.json"

TEAL      = "#2A9D8F"
LOSS_RED  = "#E63946"
GRAY      = "#A8AAAD"
DARK_BLUE = "#1D3557"


df = pd.read_csv(INPUT_FILE, parse_dates=["Month", "Order Date"])


cat_region = (
    df.groupby(["Category", "Sub-Category", "Region"], as_index=False)
    .agg(
        TotalProfit  = ("Profit",   "sum"),
        TotalSales   = ("Sales",    "sum"),
        AvgDiscount  = ("Discount", "mean"),
        OrderCount   = ("Order ID", "count"),
    )
)
cat_region["ProfitSign"] = cat_region["TotalProfit"].apply(
    lambda x: "Profit" if x >= 0 else "Loss"
)


# Interaction 1: Region dropdown filter
region_filter = alt.selection_point(
    fields=["Region"],
    bind=alt.binding_select(
        options=[None, "East", "West", "Central", "South"],
        labels=["All Regions", "East", "West", "Central", "South"],
        name="Filter by Region: "
    ),
    value=None
)

bars = (
    alt.Chart(cat_region)
    .mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3)
    .encode(
        x=alt.X(
            "TotalProfit:Q",
            title="Total Profit (USD)",
            axis=alt.Axis(format="$,.0f")
        ),
        y=alt.Y(
            "Sub-Category:N",
            sort="-x",
            title=None
        ),
        color=alt.Color(
            "ProfitSign:N",
            scale=alt.Scale(domain=["Profit", "Loss"], range=[TEAL, LOSS_RED]),
            title="Result",
            legend=alt.Legend(orient="bottom")
        ),
        # Interaction 2: Hover tooltip
        tooltip=[
            alt.Tooltip("Sub-Category:N", title="Sub-Category"),
            alt.Tooltip("Category:N",     title="Category"),
            alt.Tooltip("Region:N",       title="Region"),
            alt.Tooltip("TotalProfit:Q",  title="Total Profit",  format="$,.0f"),
            alt.Tooltip("TotalSales:Q",   title="Total Sales",   format="$,.0f"),
            alt.Tooltip("AvgDiscount:Q",  title="Avg Discount",  format=".1%"),
            alt.Tooltip("OrderCount:Q",   title="Order Lines",   format=","),
        ]
    )
    .add_params(region_filter)
    .transform_filter(region_filter)
    .properties(width=200, height=180)
    .facet(
        facet=alt.Facet("Category:N", title=None, header=alt.Header(labelFontSize=13, labelFontWeight="bold")),
        columns=3
    )
    .resolve_scale(y="independent", x="shared")
    .properties(
        title=alt.TitleParams(
            "Profit by Sub-Category and Region",
            subtitle="Tables and Bookcases (Furniture) are structural loss-makers — especially in Central & East",
            fontSize=16,
            subtitleFontSize=12,
            color=DARK_BLUE,
            subtitleColor=GRAY,
        )
    )
)

viz3 = bars.configure_view(stroke=GRAY, strokeWidth=0.5)


viz3.save(OUTPUT_FILE)