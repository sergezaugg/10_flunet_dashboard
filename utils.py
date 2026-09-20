#--------------------             
# Author : Serge Zaugg
# Description : functions - stremlit chunks

#--------------------

import pandas as pd
import plotly.express as px
import streamlit as st
from config import FLUNET_DATA_URL, FLUNET_META_URL



@st.cache_data(ttl=86400) 
def download_flunet_data():
    """Download FluNet data and metadata."""
    df_dat = pd.read_csv(FLUNET_DATA_URL)
    df_meta = pd.read_csv(FLUNET_META_URL)
    return(df_dat, df_meta)


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
def filter_data(df, prop_non_na_tol = 0.50, mean_count_tol = 40, who_regions = ['EUR']):
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

    # check
    n_countries = df["COUNTRY"].value_counts().shape

    return(df, n_countries) 

