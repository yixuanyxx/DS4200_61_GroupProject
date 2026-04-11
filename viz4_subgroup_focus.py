import pandas as pd
import numpy as np
import altair as alt

INPUT_FILE = "superstore_clean.csv"

GRAY      = "#A8AAAD"
DARK_BLUE = "#1D3557"

df = pd.read_csv(INPUT_FILE, parse_dates=["Order Date"])
df["ProfitMargin"] = df["Profit"] / df["Sales"]

stats = (
    df.groupby(["Ship Mode", "Category"])["ProfitMargin"]
    .mean().reset_index()
)
stats.columns = ["Ship Mode", "Category", "Mean"]

SHIP_ORDER = ["Standard Class", "Second Class", "First Class", "Same Day"]
CAT_ORDER  = ["Furniture", "Office Supplies", "Technology"]
CAT_COLORS = ["#E76F51", "#F72585", "#2A9D8F"]

cat_sel = alt.selection_point(
    name="cat_sel_v4", fields=["Category"], bind="legend"
)

bars = (
    alt.Chart(stats)
    .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
    .encode(
        y=alt.Y("Ship Mode:N", sort=SHIP_ORDER, title=None),
        x=alt.X("Mean:Q", title="Avg Profit Margin",
                axis=alt.Axis(format=".0%"),
                scale=alt.Scale(domain=[0, 0.28])),
        color=alt.Color(
            "Category:N",
            scale=alt.Scale(domain=CAT_ORDER, range=CAT_COLORS),
            title="Category"
        ),
        yOffset=alt.YOffset("Category:N", sort=CAT_ORDER),
        opacity=alt.condition(cat_sel, alt.value(0.85), alt.value(0.1)),
        tooltip=[
            alt.Tooltip("Ship Mode:N", title="Ship Mode"),
            alt.Tooltip("Category:N",  title="Category"),
            alt.Tooltip("Mean:Q",      title="Avg Margin", format=".1%"),
        ]
    )
    .add_params(cat_sel)
    .properties(width=500, height=260)
)

(
    bars
    .properties(
        title=alt.TitleParams(
            "Profit Margin by Ship Mode and Category",
            subtitle="Second Class yields the highest margin — Standard Class, despite being most used, earns the least · Click legend to filter",
            fontSize=16, subtitleFontSize=12,
            color=DARK_BLUE, subtitleColor=GRAY,
        )
    )
    .configure_view(strokeWidth=0)
    .configure_axis(labelFont="sans-serif", titleFont="sans-serif")
    .configure_legend(titleFontSize=12, labelFontSize=11, orient="bottom")
).save("viz4_subgroup_focus.json")

print("saved viz4_subgroup_focus.json")