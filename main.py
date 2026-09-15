
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

# df_dat['COUNTRY_CODE'].unique().shape
# df_dat['COUNTRY_AREA_TERRITORY'].unique().shape

# select only relevant columns 
df_data = df_dat[["COUNTRY_AREA_TERRITORY", 
                    "ORIGIN_SOURCE", 
                    "ISO_YEAR", "ISO_WEEK", "ISO_WEEKSTARTDATE", 
                    "SPEC_RECEIVED_NB", "SPEC_PROCESSED_NB",
                    "INF_A", "INF_B", "INF_ALL"]]


df_data = df_data.rename(columns={"COUNTRY_AREA_TERRITORY": "COUNTRY"})

# convert str to datetime 
df_data["ISO_WEEKSTARTDATE"] = pd.to_datetime(df_data["ISO_WEEKSTARTDATE"],errors="coerce")


# Columns to sum
inf_cols = df_data.filter(regex=r"^INF_").columns

# Keep one row per country and date
group_cols = ["COUNTRY", "ISO_WEEKSTARTDATE"]

df_sum = (
    df_data
    .groupby(group_cols, as_index=False)[inf_cols]
    .sum(min_count=1)      # keeps NaN if all values are NaN
)

df_sum.shape
df_data.shape

df_sum["ORIGIN_SOURCE"] = "SUM_ALL"

df_data = pd.concat([df_data, df_sum], ignore_index=True)


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

df_data2 = df_data[df_data["ORIGIN_SOURCE"] == "NONSENTINEL"]
df_data2 = df_data[df_data["ORIGIN_SOURCE"] == "SENTINEL"]

# re center
df_data2["week_plot"] = (df_data2["ISO_WEEK"] - 30) 

fig = px.line(
    df_data2,
    x="week_plot",
    y="INF_ALL",
    color="ISO_YEAR",
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



#------------------------







