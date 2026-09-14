
"""
Exploration of FluNet data
Author: Serge Zaugg
Date: 2026-09-14
"""

import pandas as pd
import plotly.express as px

# download data
url_data = "https://xmart-api-public.who.int/FLUMART/VIW_FNT?$format=csv"
url_meta = "https://xmart-api-public.who.int/FLUMART/VIW_FLU_METADATA?$format=csv&$filter=contains(DatasetName,%20%27FluNet%27)"
df_dat = pd.read_csv(url_data)
df_meta = pd.read_csv(url_meta)
df_dat.shape
df_meta.shape



# select only relevant columns 
df_data = df_dat[["COUNTRY_CODE", "ORIGIN_SOURCE", "ISO_YEAR", "ISO_WEEK", "MMWR_WEEKSTARTDATE", "INF_A", "INF_B", "INF_ALL"]]

# convert str to datetime 
df_data["date"] = pd.to_datetime(df_data["MMWR_WEEKSTARTDATE"],errors="coerce")

# select date from 2015
df_data.shape
df_data = df_data[df_data["date"] >= "2015-01-01"]
df_data.shape

# select only countries with sufficient data 
country_counts = df_data["COUNTRY_CODE"].value_counts()
countries = country_counts[country_counts >= 1200].index
df_filt = df_data[df_data["COUNTRY_CODE"].isin(countries)]

# check
df_data.shape
df_filt.shape
print(df_filt["COUNTRY_CODE"].value_counts().to_string())

for country in df_filt["COUNTRY_CODE"].dropna().unique():

    df_cnt = df_filt[df_filt["COUNTRY_CODE"] == country]

    fig = px.line(
        df_cnt,
        x="date",
        y="INF_ALL",
        color="ORIGIN_SOURCE",
        title=f"Weekly Influenza cases — {country}",
        markers=False,
    )

    fig.update_layout(
        xaxis_title="Week",
        yaxis_title="Influenza A cases",
        hovermode="x unified",
    )

    fig.show()









