"""
DS4200 Group Project — Viz 2: Discount vs. Profit
Author: Yuansi Jiang

Narrative beat : "At the line level, how does discount relate to profit?"
Chart type     : Scatter plot (one point per order line)
Interactions   : Legend click to highlight by Category + hover tooltip
Output         : viz2_discount_profit.json  ← Ryan embeds this in index.html

Fixes:
    - Added jitter on Discount so points don't stack in vertical lines
    - Clamped y-axis to [-2000, 2500] to suppress extreme outliers

Usage:
    python data_cleaning.py        # run first to generate superstore_clean.csv
    python viz2_discount_profit.py
"""

import numpy as np
import pandas as pd
import altair as alt

INPUT_FILE  = "superstore_clean.csv"
OUTPUT_FILE = "viz2_discount_profit.json"

TEAL      = "#2A9D8F"
STEEL     = "#457B9D"
ORANGE    = "#E76F51"
LOSS_RED  = "#E63946"
GRAY      = "#A8AAAD"
DARK_BLUE = "#1D3557"


df = pd.read_csv(INPUT_FILE, parse_dates=["Month", "Order Date"])

rng = np.random.default_rng(42)
df["Discount_jitter"] = df["Discount"] + rng.uniform(-0.018, 0.018, size=len(df))



# Interaction 1: Legend click as highlight one Category, fade others
category_select = alt.selection_point(fields=["Category"], bind="legend")

scatter = (
    alt.Chart(df)
    .mark_circle(size=45)
    .encode(
        x=alt.X(
            "Discount_jitter:Q",
            title="Discount Rate",
            axis=alt.Axis(format=".0%", values=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]),
            scale=alt.Scale(domain=[-0.05, 0.88])
        ),
        y=alt.Y(
            "Profit:Q",
            title="Profit (USD)",
            axis=alt.Axis(format="$,.0f"),
            scale=alt.Scale(domain=[-2000, 2500], clamp=True)
        ),
        color=alt.Color(
            "Category:N",
            scale=alt.Scale(
                domain=["Furniture", "Office Supplies", "Technology"],
                range=[ORANGE, STEEL, TEAL]
            ),
            title="Category"
        ),
        # Fade unselected categories
        opacity=alt.condition(
            category_select,
            alt.value(0.6),
            alt.value(0.07)
        ),
        # Interaction 2: Hover tooltip
        tooltip=[
            alt.Tooltip("Product Name:N", title="Product"),
            alt.Tooltip("Category:N",     title="Category"),
            alt.Tooltip("Sub-Category:N", title="Sub-Category"),
            alt.Tooltip("Region:N",       title="Region"),
            alt.Tooltip("Discount:Q",     title="Discount",  format=".0%"),
            alt.Tooltip("Profit:Q",       title="Profit",    format="$,.2f"),
            alt.Tooltip("Sales:Q",        title="Sales",     format="$,.2f"),
        ]
    )
    .add_params(category_select)
    .properties(width=700, height=420)
)

# Zero profit reference line
zero_line = (
    alt.Chart(pd.DataFrame({"y": [0]}))
    .mark_rule(color=LOSS_RED, strokeDash=[5, 3], strokeWidth=1.8, opacity=0.8)
    .encode(y="y:Q")
)

# Break-even annotation
zero_label = (
    alt.Chart(pd.DataFrame({"y": [120], "x": [0.78], "text": ["Break-even"]}))
    .mark_text(color=LOSS_RED, fontSize=11, align="right", fontStyle="italic")
    .encode(x="x:Q", y="y:Q", text="text:N")
)

viz2 = (
    (scatter + zero_line + zero_label)
    .properties(
        title=alt.TitleParams(
            "Discount Rate vs. Profit by Category",
            subtitle="Orders with discount > 20% frequently result in losses — especially in Furniture",
            fontSize=16,
            subtitleFontSize=12,
            color=DARK_BLUE,
            subtitleColor=GRAY,
        )
    )
    .configure_view(strokeWidth=0)
    .configure_axis(labelFont="sans-serif", titleFont="sans-serif")
    .configure_legend(
        titleFontSize=12,
        labelFontSize=11,
        symbolSize=120
    )
)


viz2.save(OUTPUT_FILE)