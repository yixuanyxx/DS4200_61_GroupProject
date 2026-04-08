"""
DS4200 Group Project — Viz 4: Subgroup Focus
Author: Yuansi Jiang

Narrative beat : "Name the problem case — high sales, bad profit"
Chart type     : Two side-by-side horizontal bar charts (Sales | Profit)
                 Furniture only, color by Region, dropdown filter
Interaction    : Region dropdown + hover tooltip
Output         : viz4_subgroup_focus.json

Usage:
    python data_cleaning.py
    python viz4_subgroup_focus.py
"""

import pandas as pd
import altair as alt

INPUT_FILE  = "superstore_clean.csv"
OUTPUT_FILE = "viz4_subgroup_focus.json"

TEAL      = "#2A9D8F"
LOSS_RED  = "#E63946"
STEEL     = "#457B9D"
ORANGE    = "#E76F51"
GRAY      = "#A8AAAD"
DARK_BLUE = "#1D3557"

df = pd.read_csv(INPUT_FILE, parse_dates=["Order Date"])
furniture = df[df["Category"] == "Furniture"]

agg = (
    furniture.groupby(["Sub-Category", "Region"], as_index=False)
    .agg(
        TotalSales  = ("Sales",    "sum"),
        TotalProfit = ("Profit",   "sum"),
        AvgDiscount = ("Discount", "mean"),
        OrderCount  = ("Order ID", "count"),
    )
)

SUBCAT_SORT  = ["Tables", "Bookcases", "Furnishings", "Chairs"]
REGION_SCALE = alt.Scale(
    domain=["Central", "East", "South", "West"],
    range=[ORANGE, STEEL, "#F4A261", TEAL]
)

region_filter = alt.selection_point(
    fields=["Region"],
    bind=alt.binding_select(
        options=[None, "East", "West", "Central", "South"],
        labels=["All Regions", "East", "West", "Central", "South"],
        name="Filter by Region: "
    ),
    value=None
)

TOOLTIP = [
    alt.Tooltip("Sub-Category:N", title="Sub-Category"),
    alt.Tooltip("Region:N",       title="Region"),
    alt.Tooltip("TotalSales:Q",   title="Total Sales",  format="$,.0f"),
    alt.Tooltip("TotalProfit:Q",  title="Total Profit", format="$,.0f"),
    alt.Tooltip("AvgDiscount:Q",  title="Avg Discount", format=".1%"),
    alt.Tooltip("OrderCount:Q",   title="Order Lines",  format=","),
]

sales_chart = (
    alt.Chart(agg)
    .mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3)
    .encode(
        y=alt.Y("Sub-Category:N", sort=SUBCAT_SORT, title=None),
        x=alt.X("TotalSales:Q", title="Total Sales (USD)", axis=alt.Axis(format="$,.0f")),
        yOffset=alt.YOffset("Region:N", sort=["Central","East","South","West"]),
        color=alt.Color("Region:N", scale=REGION_SCALE, title="Region"),
        opacity=alt.condition(region_filter, alt.value(0.85), alt.value(0.15)),
        tooltip=TOOLTIP
    )
    .add_params(region_filter)
    .properties(width=280, height=200,
                title=alt.TitleParams("Total Sales", fontSize=13, color=STEEL))
)

profit_bars = (
    alt.Chart(agg)
    .mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3)
    .encode(
        y=alt.Y("Sub-Category:N", sort=SUBCAT_SORT, title=None,
                axis=alt.Axis(labels=False, ticks=False)),
        x=alt.X("TotalProfit:Q", title="Total Profit (USD)", axis=alt.Axis(format="$,.0f")),
        yOffset=alt.YOffset("Region:N", sort=["Central","East","South","West"]),
        color=alt.Color("Region:N", scale=REGION_SCALE, title="Region"),
        opacity=alt.condition(region_filter, alt.value(0.85), alt.value(0.15)),
        tooltip=TOOLTIP
    )
    .add_params(region_filter)
    .properties(width=280, height=200,
                title=alt.TitleParams("Total Profit", fontSize=13, color=TEAL))
)

zero_line = (
    alt.Chart(pd.DataFrame({"x": [0]}))
    .mark_rule(color=LOSS_RED, strokeDash=[4,3], strokeWidth=1.8, opacity=0.9)
    .encode(x=alt.X("x:Q", title="Total Profit (USD)"))
)

profit_panel = alt.layer(profit_bars, zero_line)

viz4 = (
    alt.hconcat(sales_chart, profit_panel, spacing=24)
    .properties(
        title=alt.TitleParams(
            "Furniture: Sales vs. Profit by Sub-Category and Region",
            subtitle="Tables have high sales but the worst profit — driven by heavy discounting",
            fontSize=16, subtitleFontSize=12,
            color=DARK_BLUE, subtitleColor=GRAY,
        )
    )
    .configure_view(strokeWidth=0.5, stroke=GRAY)
    .configure_axis(labelFont="sans-serif", titleFont="sans-serif")
    .configure_legend(titleFontSize=12, labelFontSize=11)
)

viz4.save(OUTPUT_FILE)