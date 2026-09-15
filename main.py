
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
df_data = df_dat[["COUNTRY_CODE", "COUNTRY_AREA_TERRITORY", 
                    "ORIGIN_SOURCE", 
                    "ISO_YEAR", "ISO_WEEK", "ISO_WEEKSTARTDATE", 
                    "SPEC_RECEIVED_NB", "SPEC_PROCESSED_NB",
                    "INF_A", "INF_B", "INF_ALL"]]

# convert str to datetime 
df_data["ISO_WEEKSTARTDATE"] = pd.to_datetime(df_data["ISO_WEEKSTARTDATE"],errors="coerce")

# select date from 2015
df_data.shape
df_data = df_data[df_data["ISO_WEEKSTARTDATE"] >= "2015-01-01"]
df_data.shape



# exclude country yeras with too many missings 
thld = 0.30  

# NA proportion per COUNTRY_CODE 
df_data["na_prop"] = (df_data.groupby(["COUNTRY_CODE", ])["INF_ALL"].transform(lambda s: s.isna().mean()))

# Filter out country-years above threshold
df_data = df_data[df_data["na_prop"] <= thld].copy()
df_data.shape



# select only countries with sufficient data 
country_counts = df_data["COUNTRY_CODE"].value_counts()
countries = country_counts[country_counts >= 500].index
df_data = df_data[df_data["COUNTRY_CODE"].isin(countries)]
# check
df_data.shape


# check
all_selected_countries = df_data["COUNTRY_CODE"].value_counts()
all_selected_countries.shape
print(all_selected_countries.to_string())








for country in df_data["COUNTRY_CODE"].dropna().unique():

    df_cnt = df_data[df_data["COUNTRY_CODE"] == country]

    fig = px.line(
        df_cnt,
        x="ISO_WEEKSTARTDATE",
        y="INF_ALL",
        color="ORIGIN_SOURCE",
        title=f"Weekly Influenza cases — {country}",
        markers=False,
    )

    fig.update_layout(
        xaxis_title="Week",
        yaxis_title="Influenza cases",
        hovermode="x unified",
    )

    fig.show()









