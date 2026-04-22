import pandas as pd
import altair as alt

INPUT_FILE  = "superstore_clean.csv"
OUTPUT_FILE = "viz1_time_series.json"

BLUE      = "#457B9D"
GOLD      = "#E9C46A"
GREEN     = "#2A9D8F"
GRAY      = "#A8AAAD"
DARK_BLUE = "#1D3557"

df = pd.read_csv(INPUT_FILE, parse_dates=["Month", "Order Date"])

monthly = (
    df.groupby(["Month", "Year"], as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
)
monthly["MonthIndex"] = (monthly["Year"] - 2014) * 12 + monthly["Month"].dt.month

monthly_long = monthly.melt(
    id_vars=["Month", "Year", "MonthIndex"],
    value_vars=["Sales", "Profit"],
    var_name="Metric",
    value_name="Amount"
)

COLOR_SCALE = alt.Scale(domain=["Sales", "Profit"], range=[BLUE, GOLD])

start_slider = alt.param(
    name="start_month", value=1,
    bind=alt.binding_range(min=1, max=48, step=1, name="Start: ")
)
end_slider = alt.param(
    name="end_month", value=48,
    bind=alt.binding_range(min=1, max=48, step=1, name="End:   ")
)

START_EXPR = "timeFormat(datetime(2014 + floor((start_month-1)/12), (start_month-1)%12, 1), '%b %Y')"
END_EXPR   = "timeFormat(datetime(2014 + floor((end_month-1)/12),   (end_month-1)%12,   1), '%b %Y')"

label_df = pd.DataFrame({"placeholder": [1]})

date_label = (
    alt.Chart(label_df)
    .transform_calculate(label=f"'Range: ' + {START_EXPR} + ' → ' + {END_EXPR}")
    .mark_text(align="left", fontSize=12, fontWeight="bold", color=DARK_BLUE,
               dx=0, dy=0)
    .encode(
        x=alt.value(10),
        y=alt.value(18),
        text="label:N"
    )
)

lines = (
    alt.Chart(monthly_long)
    .mark_line(point=True, strokeWidth=2.5)
    .encode(
        x=alt.X("Month:T", title="Order Month",
                axis=alt.Axis(format="%b %Y", labelAngle=-45)),
        y=alt.Y("Amount:Q", title="USD ($)",
                axis=alt.Axis(format="$,.0f")),
        color=alt.Color("Metric:N", scale=COLOR_SCALE, title="Metric"),
        tooltip=[
            alt.Tooltip("Month:T",  title="Month",  format="%B %Y"),
            alt.Tooltip("Metric:N", title="Metric"),
            alt.Tooltip("Amount:Q", title="Amount", format="$,.0f"),
        ]
    )
    .transform_filter(
        "datum.MonthIndex >= start_month && datum.MonthIndex <= end_month"
    )
    .properties(width=660, height=320)
)

zero_line = (
    alt.Chart(monthly_long)
    .mark_rule(strokeDash=[4, 2], color=GREEN, opacity=0.8, strokeWidth=1.8)
    .encode(y=alt.datum(0))
    .transform_filter(
        "datum.MonthIndex >= start_month && datum.MonthIndex <= end_month"
    )
)

zero_label = (
    alt.Chart(monthly_long)
    .mark_text(color=GREEN, fontSize=10, align="left", dx=6, dy=-6)
    .encode(
        x=alt.X("min(Month):T"),
        y=alt.datum(0),
        text=alt.value("← break-even $0"),
    )
    .transform_filter(
        "datum.MonthIndex >= start_month && datum.MonthIndex <= end_month"
    )
)

viz1 = (
    alt.layer(lines, zero_line, zero_label, date_label)
    .add_params(start_slider, end_slider)
    .properties(
        width=660, height=320,
        title=alt.TitleParams(
            "Monthly Sales and Profit Over Time (2014–2017)",
            subtitle="Profit consistently trails Sales — slide to select any time range",
            fontSize=16, subtitleFontSize=12,
            color=DARK_BLUE, subtitleColor=GRAY,
        )
    )
    .configure_view(strokeWidth=0)
    .configure_axis(labelFont="sans-serif", titleFont="sans-serif")
    .configure_legend(titleFontSize=12, labelFontSize=11)
)

viz1.save(OUTPUT_FILE)