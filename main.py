"""
Exploration of FluNet data
Author: Serge Zaugg
Date: 2026-09-14
"""

import pandas as pd
import plotly.express as px


#---------------------------------
# download data
url_data = "https://xmart-api-public.who.int/FLUMART/VIW_FNT?$format=csv"
url_meta = "https://xmart-api-public.who.int/FLUMART/VIW_FLU_METADATA?$format=csv&$filter=contains(DatasetName,%20%27FluNet%27)"
df_dat = pd.read_csv(url_data)
df_meta = pd.read_csv(url_meta)
df_dat.shape
df_meta.shape







#---------------------------------
# pre-process

# select only relevant columns 
df_data = df_dat[[
    "WHOREGION", "FLUSEASON", "ITZ", # "Influenza transmission zone"
    "COUNTRY_AREA_TERRITORY", 
    "ORIGIN_SOURCE", 
    "ISO_YEAR", "ISO_WEEK", "ISO_WEEKSTARTDATE", 
    "INF_A", "INF_B", "INF_ALL"]]

# re-name variables 
df_data = df_data.rename(columns={"COUNTRY_AREA_TERRITORY": "COUNTRY"})

# convert str to datetime 
df_data["ISO_WEEKSTARTDATE"] = pd.to_datetime(df_data["ISO_WEEKSTARTDATE"],errors="coerce")























# total over ORIGIN_SOURCE of 'INF_A', 'INF_B', 'INF_ALL' per country and week
df_sum = (
    df_data
    .groupby(["COUNTRY", "ISO_WEEKSTARTDATE"], as_index=False)
    .agg(
        **{col: (col, "sum") for col in ['INF_A', 'INF_B', 'INF_ALL']},
        ISO_YEAR  = ("ISO_YEAR",  "min"),
        ISO_WEEK  = ("ISO_WEEK",  "min"),
        WHOREGION = ("WHOREGION", "first"), 
        FLUSEASON = ("FLUSEASON", "first"),
        ITZ       = ("ITZ",       "first"),
    )
)

df_sum["ORIGIN_SOURCE"] = "SUM_ALL"
df_sum.shape
df_data.shape
df_data = pd.concat([df_data, df_sum], ignore_index=True)
del(df_sum)
df_data.shape






















#---------------------------------
# filters 

# select date from 2015
df_data.shape
df_data = df_data[df_data["ISO_WEEKSTARTDATE"] >= "2015-01-01"]
df_data.shape

# exclude country with too many missings 
df_data["na_prop"] = (df_data.groupby(["COUNTRY", ])["INF_ALL"].transform(lambda s: s.isna().mean()))
# Filter out country-years above threshold
df_data = df_data[df_data["na_prop"] <= 0.30].copy()
df_data.shape

# filter out countries with low mean count
df_data["mean_count_per_country"] = (df_data.groupby(["COUNTRY"])["INF_ALL"].transform(lambda s: s.mean()))
df_data["mean_count_per_country"].unique()
# Filter out country-years above threshold
df_data = df_data[df_data["mean_count_per_country"] > 40].copy()
df_data.shape

# select only countries with sufficient data overall
country_counts = df_data["COUNTRY"].value_counts()
countries = country_counts[country_counts >= 700].index
df_data = df_data[df_data["COUNTRY"].isin(countries)]
df_data.shape

# check
all_selected_countries = df_data["COUNTRY"].value_counts()
all_selected_countries.shape
print(all_selected_countries.to_string())



#---------------------------------
# basic plot  

fig = px.line(
    df_data,
    x="ISO_WEEKSTARTDATE",
    y="INF_ALL",
    color="ORIGIN_SOURCE",
    facet_row="COUNTRY",      # one row per country
    facet_row_spacing=0.003,
    height=4000
)

fig.update_yaxes(matches=None)     # optional: independent y-scales
fig.update_layout(showlegend=True)

for annotation in fig.layout.annotations:
    annotation.text = annotation.text.replace("COUNTRY=", "")
    annotation.textangle = 0

fig.show()













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
















