"""
Exploration of FluNet data
Author: Serge Zaugg
Date: 2026-09-14
"""

import pandas as pd
import plotly.express as px



# # per coutry plot to shoe onset of vave 


# df_data.columns

# # Re-define "year" as period from July -> June
# df_data["SEASON_YEAR"] = (df_data["ISO_WEEKSTARTDATE"].dt.year - (df_data["ISO_WEEKSTARTDATE"].dt.month < 7))

# # Reference date = 1 January within that season
# jan1 = pd.to_datetime((df_data["SEASON_YEAR"] + 1).astype(str) + "-01-01")

# # Set Jan 1 = week 0, previous weeks = -1, -2, ...
# df_data["SEASON_WEEK"] = ((df_data["ISO_WEEKSTARTDATE"] - jan1).dt.days // 7) + 0


# # plot 
# countries = ["Switzerland"]
# df = df_data[df_data["COUNTRY"].isin(countries)]
# df = df[df["ORIGIN_SOURCE"] == "SUM_ALL"]

# fig = px.bar(
#     df,
#     x="SEASON_WEEK",
#     y="INF_ALL",
#     facet_row="SEASON_YEAR",
#     facet_row_spacing=0.004,
#     height = 7000
#     )

# fig.add_vline(
#     x=0,
#     line_dash="dash",
#     line_color="green",
#     line_width=1
# )

# fig.update_yaxes(matches=None)     # optional: independent y-scales

# fig.show()











# --------------------------
# check onset of flu wave 

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
















