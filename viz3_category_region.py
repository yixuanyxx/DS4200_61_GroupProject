import pandas as pd
import altair as alt

INPUT_FILE  = "superstore_clean.csv"
OUTPUT_FILE = "viz3_category_region.json"

GRAY      = "#A8AAAD"
DARK_BLUE = "#1D3557"

STATE_FIPS = {
    'Alabama': 1, 'Alaska': 2, 'Arizona': 4, 'Arkansas': 5, 'California': 6,
    'Colorado': 8, 'Connecticut': 9, 'Delaware': 10, 'Florida': 12, 'Georgia': 13,
    'Hawaii': 15, 'Idaho': 16, 'Illinois': 17, 'Indiana': 18, 'Iowa': 19,
    'Kansas': 20, 'Kentucky': 21, 'Louisiana': 22, 'Maine': 23, 'Maryland': 24,
    'Massachusetts': 25, 'Michigan': 26, 'Minnesota': 27, 'Mississippi': 28,
    'Missouri': 29, 'Montana': 30, 'Nebraska': 31, 'Nevada': 32, 'New Hampshire': 33,
    'New Jersey': 34, 'New Mexico': 35, 'New York': 36, 'North Carolina': 37,
    'North Dakota': 38, 'Ohio': 39, 'Oklahoma': 40, 'Oregon': 41, 'Pennsylvania': 42,
    'Rhode Island': 44, 'South Carolina': 45, 'South Dakota': 46, 'Tennessee': 47,
    'Texas': 48, 'Utah': 49, 'Vermont': 50, 'Virginia': 51, 'Washington': 53,
    'West Virginia': 54, 'Wisconsin': 55, 'Wyoming': 56, 'District of Columbia': 11
}

df = pd.read_csv(INPUT_FILE)
df['fips'] = df['State'].map(STATE_FIPS)

fur_subcats = sorted(df[df['Category']=='Furniture']['Sub-Category'].unique().tolist())
off_subcats = sorted(df[df['Category']=='Office Supplies']['Sub-Category'].unique().tolist())
tec_subcats = sorted(df[df['Category']=='Technology']['Sub-Category'].unique().tolist())
all_subcats = fur_subcats + off_subcats + tec_subcats

rows = []
for state, g in df.groupby('State'):
    row = {
        'State': state,
        'fips': int(g['fips'].iloc[0]),
        'All': round(g['Profit'].sum(), 2),
        'Furniture': round(g[g['Category']=='Furniture']['Profit'].sum(), 2),
        'Office_Supplies': round(g[g['Category']=='Office Supplies']['Profit'].sum(), 2),
        'Technology': round(g[g['Category']=='Technology']['Profit'].sum(), 2),
    }
    for subcat in all_subcats:
        row[subcat] = round(g[g['Sub-Category']==subcat]['Profit'].sum(), 2)
    rows.append(row)

states_wide = pd.DataFrame(rows).fillna(0)

options = ['All', 'Furniture', 'Office_Supplies', 'Technology'] + all_subcats
labels  = ['All Categories', 'Furniture', 'Office Supplies', 'Technology'] + \
    [f'  Furniture › {s}' for s in fur_subcats] + \
    [f'  Office Supplies › {s}' for s in off_subcats] + \
    [f'  Technology › {s}' for s in tec_subcats]

sel = alt.param(
    name='sel', value='All',
    bind=alt.binding_select(options=options, labels=labels, name='Filter: ')
)

# FIX: use pinned vega-datasets version and reduce width to fit container
TOPO_URL = 'https://cdn.jsdelivr.net/npm/vega-datasets@1.31.1/data/us-10m.json'
lookup_fields = ['State', 'All', 'Furniture', 'Office_Supplies', 'Technology'] + all_subcats

background = (
    alt.Chart(alt.topo_feature(TOPO_URL, 'states'))
    .mark_geoshape(fill='#e0e0e0', stroke='white', strokeWidth=0.5)
    .project('albersUsa')
    .properties(width=640, height=400)
)

choropleth = (
    alt.Chart(alt.topo_feature(TOPO_URL, 'states'))
    .mark_geoshape(stroke='white', strokeWidth=0.5)
    .transform_lookup(
        lookup='id',
        from_=alt.LookupData(states_wide, 'fips', lookup_fields)
    )
    .transform_calculate(SelectedProfit="datum[sel]")
    .encode(
        color=alt.Color(
            'SelectedProfit:Q',
            title='Net Profit (USD)',
            scale=alt.Scale(scheme='redyellowgreen', domainMid=0),
            legend=alt.Legend(orient='bottom', gradientLength=280,
                              titleFontSize=11, labelFontSize=10)
        ),
        tooltip=[
            alt.Tooltip('State:N',          title='State'),
            alt.Tooltip('SelectedProfit:Q', title='Net Profit', format='$,.0f'),
        ]
    )
    .add_params(sel)
    .project('albersUsa')
    .properties(width=640, height=400)
)

(
    (background + choropleth)
    .properties(
        title=alt.TitleParams(
            'Net Profit by State',
            subtitle='Filter by category or sub-category — red = loss, green = gain',
            fontSize=16, subtitleFontSize=12,
            color=DARK_BLUE, subtitleColor=GRAY,
        )
    )
    .configure_view(strokeWidth=0)
    .configure_legend(titleFontSize=11, labelFontSize=10)
).save(OUTPUT_FILE)

print("saved", OUTPUT_FILE)