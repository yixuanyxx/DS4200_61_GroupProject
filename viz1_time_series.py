"""
DS4200 Group Project — Viz 1: Sales & Profit Over Time
Author: Yuansi (Person 1)

Narrative beat : "When is the business healthy across time?"
Chart type     : Dual-line time series (monthly aggregation)
Interactions   : Year dropdown filter + hover tooltip
Output         : viz1_time_series.json

Usage:
    python data_cleaning.py
    python viz1_time_series.py
"""

import pandas as pd
import altair as alt

INPUT_FILE  = "superstore_clean.csv"
OUTPUT_FILE = "viz1_time_series.json"

TEAL      = "#2A9D8F"
STEEL     = "#457B9D"
LOSS_RED  = "#E63946"
GRAY      = "#A8AAAD"
DARK_BLUE = "#1D3557"

df = pd.read_csv(INPUT_FILE, parse_dates=["Month", "Order Date"])

monthly = (
    df.groupby(["Month", "Year"], as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
)

monthly_long = monthly.melt(
    id_vars=["Month", "Year"],
    value_vars=["Sales", "Profit"],
    var_name="Metric",
    value_name="Amount"
)

year_filter = alt.selection_point(
    name="year_filter",
    fields=["Year"],
    bind=alt.binding_select(
        options=[None, 2014, 2015, 2016, 2017],
        labels=["All Years", "2014", "2015", "2016", "2017"],
        name="Filter by Year: "
    ),
    value=None
)

color_scale = alt.Scale(domain=["Sales", "Profit"], range=[STEEL, TEAL])

lines = (
    alt.Chart(monthly_long)
    .mark_line(point=True, strokeWidth=2.5)
    .encode(
        x=alt.X(
            "Month:T",
            title="Order Month",
            axis=alt.Axis(format="%b %Y", labelAngle=-45)
        ),
        y=alt.Y(
            "Amount:Q",
            title="USD ($)",
            axis=alt.Axis(format="$,.0f")
        ),
        color=alt.Color("Metric:N", scale=color_scale, title="Metric"),
        strokeDash=alt.condition(
            alt.datum.Metric == "Sales",
            alt.value([4, 2]),
            alt.value([1, 0])
        ),
        tooltip=[
            alt.Tooltip("Month:T",  title="Month",  format="%B %Y"),
            alt.Tooltip("Metric:N", title="Metric"),
            alt.Tooltip("Amount:Q", title="Amount", format="$,.0f"),
        ]
    )
    .add_params(year_filter)
    .transform_filter(year_filter)
    .properties(width=750, height=350)
)

#ZERO LINE
zero_line = (
    alt.Chart(monthly_long)
    .mark_rule(strokeDash=[4, 2], color=LOSS_RED, opacity=0.7, strokeWidth=1.5)
    .encode(y=alt.datum(0))
    .transform_filter(year_filter)
)

# Break-even label
zero_label = (
    alt.Chart(monthly_long)
    .mark_text(color=LOSS_RED, fontSize=10, align="left", dx=6, dy=-6)
    .encode(
        x=alt.X("min(Month):T"),
        y=alt.datum(0),
        text=alt.value("← break-even $0"),
    )
    .transform_filter(year_filter)
)

viz1 = (
    (lines + zero_line + zero_label)
    .properties(
        title=alt.TitleParams(
            "Monthly Sales and Profit Over Time (2014–2017)",
            subtitle="Profit consistently trails Sales — discount spikes often coincide with profit dips",
            fontSize=16,
            subtitleFontSize=12,
            color=DARK_BLUE,
            subtitleColor=GRAY,
        )
    )
    .configure_view(strokeWidth=0)
    .configure_axis(labelFont="sans-serif", titleFont="sans-serif")
)

viz1.save(OUTPUT_FILE)