import altair as alt
import polars as pl
import pandas as pd
import argparse
from os.path import join

parser = parser = argparse.ArgumentParser()
parser.add_argument("InputExcelPath", help="The path to the input Excel file", type=str)
parser.add_argument("OutputFolder", help="The path of Output html", type=str)
args = parser.parse_args()

df = pl.read_excel(args.InputExcelPath, sheet_name="Results")
# Transforming data and creating new columns
df = df.with_columns([
    (pl.col("FileName").str.split(by="_").arr.get(
        0).cast(pl.Int64)).alias("RowCount"),
    (pl.col("Approach").str.split(by="FilterUsing").arr.get(1)).alias("Tool"),
])
df = df.with_columns([
    (pl.col("ExecutionTimeSeconds").rank(
        method="max").over(["RowCount"]).alias("Rank")),
])
# Sorting the data for better readability
df = df.sort(["RowCount", "ExecutionTimeSeconds"])

# as altair does not support Polars dataframes converting to pandas dataframe
final_df = df.to_pandas()

output_table = df.select(
    ["Tool", "RowCount", "ExecutionTimeSeconds", "RowsKept", "Rank"]).to_pandas()

# Potential gains to be made when comparing to min and max values per group
pct_group = output_table.groupby(
    ['RowCount'])['ExecutionTimeSeconds'].agg(['max', 'min'])
pct_group['PotentialGainsinPercent'] = (
    (pct_group['max']-pct_group['min'])/pct_group['max'])*100

pct_group = pct_group.reset_index(level=0)
print(pct_group)
# Saving as markdown file
output_table.to_markdown(join(args.OutputFolder,'BenchmarkFilterDatatable.md'), index=False)
pct_group.to_markdown(join(args.OutputFolder,'PotentialGainsinPercent.md'))


""" chart = alt.Chart(final_df, title="Benchmarking Filter Datatable Operation").transform_calculate(
        ToolTip="datum.Tool+'='+datum.ExecutionTimeSeconds").mark_bar().encode(
            
        x=alt.X('Tool:N', axis=alt.Axis(labelAngle=-45, title=None)),
        y=alt.Y('ExecutionTimeSeconds:Q'),
        column=alt.Column('RowCount:N'),
        
        color=alt.Color('Rank:Q', scale=alt.Scale(scheme="greens", reverse=True)),
        tooltip="ToolTip:N",
        order='Rank',
    ).configure_axis(
        grid=True
    ).configure_view(
        strokeWidth=0.4
    ).interactive()
     """

color = "goldgreen"
chart = alt.Chart().transform_calculate(
    ToolTip="datum.Tool+'='+datum.ExecutionTimeSeconds").mark_bar().encode(
    x=alt.X('Tool:N', axis=alt.Axis(labelAngle=-45, title=None)),
    y=alt.Y('ExecutionTimeSeconds:Q'),
    # color=alt.Color('Rank:Q', scale=alt.Scale(scheme="greens", reverse=True)),
    color=alt.Color('Rank:Q', scale=alt.Scale(scheme=color, reverse=True)),
    tooltip="ToolTip:N",
    order='Rank:Q',
)

text = chart.mark_text(
    color='black',
    dy=-5
).encode(
    text=alt.Text(
        'ExecutionTimeSeconds:Q',
        format=',.0f')
)

fig = alt.layer(chart, text, data=final_df).facet(
    column=alt.Column(
        'RowCount:Q',
    )
).configure_facet(
    spacing=20
).configure_axis(
    grid=False
).configure_view(
    strokeWidth=0.4
).interactive()

fig.save(join(args.OutputFolder,'BenchmarkFilterDatatable.html'))


chart = alt.Chart(pct_group).mark_bar().encode(
    x=alt.X('PotentialGainsinPercent:Q', axis=alt.Axis(
        labelAngle=-45, title="Percentage")),
    y=alt.Y('RowCount:N'),
    color=alt.Color('PotentialGainsinPercent:Q',
                    scale=alt.Scale(scheme=color, reverse=False)),
    tooltip="PotentialGainsinPercent:Q",
)

text = chart.mark_text(
    color='black',
    dx=10
).encode(
    text=alt.Text(
        'PotentialGainsinPercent:Q',
        format=',.0f')
)


fig = chart + text
fig.configure_axis(
    grid=False
).configure_scale(
    bandPaddingInner=0.5
).configure_view(
    strokeWidth=0.4
).interactive()

fig.save(join(args.OutputFolder,'PotentialGainsChart.html'))
