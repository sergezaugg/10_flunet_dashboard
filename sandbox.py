"""
Exploration of FluNet data
Author: Serge Zaugg
Date: 2026-09-14
"""

import pandas as pd
import plotly.express as px

# --------------------------
# check onset of flu wave 

df_data["ORIGIN_SOURCE"].value_counts()

# df_data2 = df_data[df_data["ORIGIN_SOURCE"] == "NONSENTINEL"]
# df_data2 = df_data[df_data["ORIGIN_SOURCE"] == "SENTINEL"]
df_data2 = df_data[df_data["ORIGIN_SOURCE"] == "SUM_ALL"]

# select only relevant columns 
df_data2 = df_data2[["COUNTRY", "ISO_WEEKSTARTDATE", "ISO_YEAR", "ISO_WEEK", "INF_ALL"]]


#------------------
# New seasonality plot 

df = df_data2.copy()
df["ISO_WEEKSTARTDATE"] = pd.to_datetime(df["ISO_WEEKSTARTDATE"])

# window starts every 1 year
starts = pd.date_range(
    df["ISO_WEEKSTARTDATE"].min(),
    df["ISO_WEEKSTARTDATE"].max() - pd.DateOffset(months=18),
    freq="YS"
)

windows = []
for start in starts:
    end = start + pd.DateOffset(months=18)

    d = df[
        (df["ISO_WEEKSTARTDATE"] >= start) &
        (df["ISO_WEEKSTARTDATE"] < end)
    ].copy()

    d["window"] = start.year
    d["relative_date"] = (
        d["ISO_WEEKSTARTDATE"] - start
    ).dt.days

    windows.append(d)

df_windows = pd.concat(windows)

df_windows.shape


fig = px.line(
    df_windows,
    x="relative_date",
    y="INF_ALL",
    color="window",
    facet_row="COUNTRY",
    facet_row_spacing=0.003,
    height=4000
)

fig.update_yaxes(matches=None)     # optional: independent y-scales
fig.update_layout(showlegend=True)

for annotation in fig.layout.annotations:
    annotation.text = annotation.text.replace("COUNTRY=", "")
    annotation.textangle = 0

fig.update_xaxes(
    title="Time from window start (days)"
)

fig.show()
















