#--------------------             
# Author : Serge Zaugg
# Description : functions - stremlit chunks

#--------------------

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from config import FLUNET_DATA_URL, FLUNET_META_URL
import requests
from io import BytesIO
from datetime import datetime

@st.cache_data(ttl=86400) 
def download_flunet_data():
    """Download FluNet data and metadata."""
    
    df_meta = pd.read_csv(FLUNET_META_URL)

    # old method - pd wrapper
    # df_dat = pd.read_csv(FLUNET_DATA_URL)
    # step-by-step import 
    response = requests.get(FLUNET_DATA_URL, timeout=60)
    response.raise_for_status()
    # Keep downloaded CSV in memory
    csv_data = BytesIO(response.content)
    # convert to DataFrame
    df_dat = pd.read_csv(csv_data, engine="python")

    download_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return(df_dat, df_meta, download_ts)


@st.cache_data()
def preprocess_flunet_data(df):
    """pre-process FluNet dataframe : select variable, rename, convert formats"""
    # select only relevant columns 
    columns = [
        "WHOREGION","FLUSEASON", "ITZ", # Influenza transmission zone
        "COUNTRY_AREA_TERRITORY","ORIGIN_SOURCE",
        "ISO_YEAR", "ISO_WEEK", "ISO_WEEKSTARTDATE",
        "INF_A", "INF_B", "INF_ALL",
        ]
    df = df[columns].copy()
    # re-name variables 
    df = df.rename(columns={"COUNTRY_AREA_TERRITORY": "COUNTRY"})
    # convert str to datetime 
    df["ISO_WEEKSTARTDATE"] = pd.to_datetime(df["ISO_WEEKSTARTDATE"],errors="coerce")
    # shorten lon countrynames to 3 words
    df["COUNTRY"] = df["COUNTRY"].str.split().str[:3].str.join(" ")
    return(df)





@st.cache_data()
def include_rows_for_total_flunet_data(df):
    """total over ORIGIN_SOURCE of 'INF_A', 'INF_B', 'INF_ALL' per country and week"""
    df_sum = (
        df.groupby(["COUNTRY", "ISO_WEEKSTARTDATE"], as_index=False)
        .agg(**{col: (col, lambda s: s.sum(min_count=1)) for col in ["INF_A", "INF_B", "INF_ALL"]},
            ISO_YEAR=("ISO_YEAR", "first"),
            ISO_WEEK=("ISO_WEEK", "first"),
            WHOREGION=("WHOREGION", "first"),
            FLUSEASON=("FLUSEASON", "first"),
            ITZ=("ITZ", "first"),
        )
    )
    df_sum["ORIGIN_SOURCE"] = "SUM_ALL"
    df = pd.concat([df, df_sum], ignore_index=True)
    return(df)





@st.cache_data()
def filter_by_date_range(df, date_range):
    """ aaaa """
    df = df.copy()
    # select date 
    df = df[df["ISO_WEEKSTARTDATE"].between(pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]))]
    return(df) 




@st.cache_data()
def filter_data(df, prop_non_na_tol = 0.50, mean_count_tol = 40, 
                who_regions = ['EUR'], fse_regions = ['aa'], itz_regions = ['bb']):
    """ aaaa """

    df = df.copy()

    # exclude country with too many missings 
    df["prop_non_na"] = (df.groupby("COUNTRY")["INF_ALL"].transform(lambda s: s.notna().mean()))
    df = df[df["prop_non_na"] >= prop_non_na_tol].copy()

    # filter out countries with low mean count
    df["mean_count_per_country"] = (df.groupby(["COUNTRY"])["INF_ALL"].transform(lambda s: s.mean()))
    df = df[df["mean_count_per_country"] > mean_count_tol].copy()

    # select only countries with sufficient data overall
    country_counts = df["COUNTRY"].value_counts()
    countries = country_counts[country_counts >= 700].index
    df = df[df["COUNTRY"].isin(countries)]

    # select based on WHOREGION
    df = df[df["WHOREGION"].isin(who_regions)]

    # select based on FLUSEASON
    df = df[df["FLUSEASON"].isin(fse_regions)]

    # select based on ITZ
    df = df[df["ITZ"].isin(itz_regions)]

    # check
    n_countries = pd.Series(df["COUNTRY"].unique()).value_counts().shape

    return(df, n_countries) 



@st.cache_data()
def re_center_season(df):
    print("check : >>>>", df.shape)
    # Re-define "year" as period from July -> June
    df["SEASON_YEAR"] = (df["ISO_WEEKSTARTDATE"].dt.year - (df["ISO_WEEKSTARTDATE"].dt.month < 7))
    # Reference date = 1 January within that season
    jan1 = pd.to_datetime((df["SEASON_YEAR"] + 1).astype("Int64").astype(str), format="%Y")
    # Set Jan 1 = week 0, previous weeks = -1, -2, ...
    df["SEASON_WEEK"] = ((df["ISO_WEEKSTARTDATE"] - jan1).dt.days // 7) + 0
    return(df)


@st.cache_data()
def filter_a_country(df, c):
    df = df[df["COUNTRY"] == c]
    df = df[df["ORIGIN_SOURCE"] == "SUM_ALL"]
    return(df)

#-----------------------------------------
# rolling functions 

@st.cache_data()
def rolling_consecutive(g, bin_size):
    d = g["ISO_WEEKSTARTDATE"]
    consecutive = d.diff().eq(pd.Timedelta(days=7))
    streak = consecutive.groupby((~consecutive).cumsum()).cumsum() + 1
    ma = g["INF_ALL"].rolling(bin_size, min_periods=bin_size, center=False).mean()
    return ma.where(streak >= bin_size)

@st.cache_data()
def ma_by_country(df, bin_size):
    df = df.sort_values(["COUNTRY", "ISO_WEEKSTARTDATE"]).copy()
    df["INF_MA"] = (df.groupby("COUNTRY", group_keys=False).apply(lambda g: rolling_consecutive(g, bin_size)))
    return df

@st.cache_data
def cond_mean(y, bin_size):
    "conditional mean ¨from regression (degree 1 polyfit)"
    x = np.arange(bin_size)
    b1, b0 = np.polyfit(x, y, 1)   
    return b0 + b1 * (bin_size - 1)   

@st.cache_data
def polyreg_by_country(df, bin_size):
    df = df.sort_values(["COUNTRY", "ISO_WEEKSTARTDATE"]).copy()
    df["INF_MA"] = (
        df.groupby("COUNTRY")["INF_ALL"]
          .rolling(bin_size, min_periods=bin_size)
          .apply(lambda y: cond_mean(y, bin_size), raw=True)
          .reset_index(level=0, drop=True)
    )
    return df
