import pandas as pd
import altair as alt

INPUT_FILE  = "superstore_clean.csv"
OUTPUT_FILE = "viz2_discount_profit.json"

FURNITURE_COLOR = "#E76F51"
OFFICE_COLOR    = "#F72585"
TECH_COLOR      = "#2A9D8F"
LOSS_RED        = "#E63946"
GRAY            = "#A8AAAD"
DARK_BLUE       = "#1D3557"

df = pd.read_csv(INPUT_FILE, parse_dates=["Order Date"])

df["Discount_Bucket"] = pd.cut(
    df["Discount"],
    bins=[-0.01, 0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.85],
    labels=["0%", "10%", "20%", "30%", "40%", "50%", "60-80%"]
).astype(str)

BUCKET_ORDER = ["0%", "10%", "20%", "30%", "40%", "50%", "60-80%"]

boxes = (
    alt.Chart(df)
    .mark_boxplot(extent=1.5, size=16, outliers=False)
    .encode(
        x=alt.X("Discount_Bucket:O", title="Discount Rate", sort=BUCKET_ORDER),
        y=alt.Y(
            "Profit:Q",
            title="Profit (USD)",
            axis=alt.Axis(format="$,.0f"),
            scale=alt.Scale(domain=[-800, 1200])
        ),
        color=alt.Color(
            "Category:N",
            scale=alt.Scale(
                domain=["Furniture", "Office Supplies", "Technology"],
                range=[FURNITURE_COLOR, OFFICE_COLOR, TECH_COLOR]
            ),
            title="Category"
        ),
        xOffset=alt.XOffset("Category:N"),   # side-by-side per discount bucket
        tooltip=[
            alt.Tooltip("Category:N",        title="Category"),
            alt.Tooltip("Discount_Bucket:O", title="Discount Bucket"),
        ]
    )
    .properties(width=700, height=380)
)

zero_line = (
    alt.Chart(pd.DataFrame({"y": [0]}))
    .mark_rule(color=LOSS_RED, strokeDash=[5, 3], strokeWidth=1.8, opacity=0.85)
    .encode(y="y:Q")
)

zero_label = (
    alt.Chart(pd.DataFrame({"y": [0]}))
    .mark_text(text="break-even $0", color=LOSS_RED, fontSize=10,
               align="left", dx=4, dy=-6)
    .encode(y="y:Q")
)

(
    (boxes + zero_line + zero_label)
    .properties(
        title=alt.TitleParams(
            "Profit Distribution by Discount Rate and Category",
            subtitle="Median profit drops below zero above 30% discount — Furniture hit hardest",
            fontSize=16, subtitleFontSize=12,
            color=DARK_BLUE, subtitleColor=GRAY,
        )
    )
    .configure_view(strokeWidth=0)
    .configure_axis(labelFont="sans-serif", titleFont="sans-serif")
    .configure_legend(titleFontSize=12, labelFontSize=11, symbolSize=150)
).save(OUTPUT_FILE)

print("saved", OUTPUT_FILE)