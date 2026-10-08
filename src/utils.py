#--------------------             
# Author : Serge Zaugg
# Description : functions - streamlit chunks
#--------------------

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from config import FLUNET_DATA_URL, FLUNET_META_URL
import requests
from io import BytesIO
from datetime import datetime

@st.cache_data(ttl=12*60*60) # refresh every 12 hours 
def download_flunet_data():
    """Download FluNet data"""
    # step-by-step import 
    try:
        response = requests.get(FLUNET_DATA_URL, timeout=60)
        response.raise_for_status()
        # Keep downloaded CSV in memory
        csv_data = BytesIO(response.content)
        # convert to DataFrame
        df_dat = pd.read_csv(csv_data, engine="c", on_bad_lines="skip", low_memory=False )
        # get a timestamp
        ts = datetime.now().strftime("%Y-%m-%d")
    except (requests.RequestException, pd.errors.ParserError):
        # handle if not downloaded
        df_dat = pd.read_csv("historical_data/VIW_FNT_20261003.csv", engine="c", on_bad_lines="skip", low_memory=False )
        ts = "Historical data (could not download)"
    if df_dat.shape[1] != 53:
        # handle if download successful but content is shit (FLUNET_DATA_URL sometimes does it)
        df_dat = pd.read_csv("historical_data/VIW_FNT_20261003.csv", engine="c", on_bad_lines="skip", low_memory=False )
        ts = "Historical data (issue with downloaded data)"
    return(df_dat, ts)


@st.cache_data(ttl=12*60*60) # refresh every 12 hours 
def get_ts_today():
    return datetime.now()


@st.cache_data()
def preprocess_flunet_data(df):
    """pre-process FluNet dataframe : select variable, rename, convert formats"""
    # select only relevant columns 
    columns = [
        "WHOREGION","FLUSEASON", "ITZ", 
        "COUNTRY_AREA_TERRITORY",
        "ORIGIN_SOURCE", 
        "COUNTRY_CODE",
        "ISO_YEAR", "ISO_WEEK", "ISO_WEEKSTARTDATE",
        "SPEC_PROCESSED_NB",
        "INF_A", "INF_B", "INF_ALL",
        ]
    df = df[columns].copy()
    # re-name variables 
    df = df.rename(columns={"COUNTRY_CODE": "COUNTRY"})
    df = df.rename(columns={"COUNTRY_AREA_TERRITORY": "CNTRY"})
    # convert str to datetime 
    df["ISO_WEEKSTARTDATE"] = pd.to_datetime(df["ISO_WEEKSTARTDATE"],errors="coerce")
    # shorten lon countrynames to 3 words
    df["COUNTRY"] = df["COUNTRY"].str.split().str[:3].str.join(" ")
    # shorten itz levels
    df['ITZ'] = df['ITZ'].str.replace("FLU_", "", regex=False)
    # set na where INF_ALL > SPEC_PROCESSED_NB
    df.loc[df["INF_ALL"] > df["SPEC_PROCESSED_NB"], "SPEC_PROCESSED_NB"] = pd.NA
    # compute positivity 
    df["POSITIVITY"] = np.where(df["SPEC_PROCESSED_NB"] >= 10, (100 * df["INF_ALL"] / df["SPEC_PROCESSED_NB"]), np.nan)
    # remove dups 
    df = df.drop_duplicates(subset=["COUNTRY", "ORIGIN_SOURCE", "ISO_WEEKSTARTDATE"],keep="last")
    # sort nicely 
    df = df.sort_values(by=["COUNTRY", "ORIGIN_SOURCE", "ISO_WEEKSTARTDATE"])
    return(df)


@st.cache_data()
def filter_by_date_range(df, date_range):
    """ aaaa """
    df = df.copy()
    # select date 
    df = df[df["ISO_WEEKSTARTDATE"].between(pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]))]
    return(df) 


@st.cache_data() # filter_data
def filter_data_region(df, who_regions = ['EUR'], fse_regions = ['aa'], itz_regions = ['bb']):
    """
    aaaa 
    """
    df = df.copy()
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
def filter_data_quality(df, prop_non_na_tol = 0.50, mean_count_tol = 40):
    """
    aaaa 
    """
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
    # check
    n_countries = pd.Series(df["COUNTRY"].unique()).value_counts().shape
    return(df, n_countries) 


@st.cache_data()
def filter_several_countries(df, countries):
    df = df[df["COUNTRY"].isin(countries)]
    n_countries = pd.Series(df["COUNTRY"].unique()).value_counts().shape
    return df, n_countries


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
    return(df)


@st.cache_data()
def filter_a_data_source(df, c):
    df = df[df["ORIGIN_SOURCE"] == c]
    return(df)






#-----------------------------------------
# rolling functions 
# @st.cache_data
# def polyreg_by_country_only(df, bin_size, deg):
#     df = df.sort_values(["COUNTRY", "ISO_WEEKSTARTDATE"]).copy()
#     df["INF_MA"] = (
#         df.groupby("COUNTRY")["INF_ALL"]
#           .rolling(bin_size, min_periods=bin_size)
#           .apply(lambda y: cond_expect_last_polyfit(y, deg), raw=True)
#           .reset_index(level=0, drop=True)
#     )
#     return df





@st.cache_data()
def get_latest_date_per_group(df, ts_today):
    """
    Get latest date of available data per COUNTRY and ORIGIN_SOURCE
    """
    df = df[["COUNTRY" , "ORIGIN_SOURCE", "WHOREGION", "FLUSEASON", "ISO_WEEKSTARTDATE" , "INF_ALL",]]
    df = df.dropna(subset=["INF_ALL"])
    # df = df.loc[df                                     .groupby(["COUNTRY", "ORIGIN_SOURCE"])["ISO_WEEKSTARTDATE"].idxmax()]
    df = df.loc[df.dropna(subset=["ISO_WEEKSTARTDATE"]).groupby(["COUNTRY", "ORIGIN_SOURCE"])["ISO_WEEKSTARTDATE"].idxmax()]
    df = df.drop(columns = ["INF_ALL"])
    # derive variable and convert types
    df["days_since"] = (ts_today - df["ISO_WEEKSTARTDATE"]).dt.days
    df["Latest date"] = (df["ISO_WEEKSTARTDATE"].dt.strftime("%Y-%m-%d"))

    return df


@st.cache_data
def det_regions(x, t):
    """
    Detect threshold regions in a Series using hysteresis.
    Parameters
    x : (pd.Series) Continuous input values.
    t : (float) Threshold value.
    Returns
    (pd.Series) Boolean Series with the same index as x.
    """
    lower = t*0.95
    upper = t*1.05
    state = False
    regions = []
    for value in x:
        if not state and value > upper:
            state = True
        elif state and value < lower:
            state = False
        regions.append(state)
    regions = pd.Series(regions, index=x.index)
    return regions


@st.cache_data
def get_start_stop_of_region(regions, time):
    """
    Identify onset and offset of contiguous True regions.
    ingests output of det_regions()
    Parameters
    regions : (pd.Series) Boolean Series indicating the regions.
    time : (pd.Series) Time values corresponding to regions.
    Returns
    (tuple of pd.Series) Two Series containing the start and end times of each region.
    """
    starts = regions & ~regions.shift(fill_value=False)
    ends = regions & ~regions.shift(-1, fill_value=False)
    sta = time[starts]
    end = time[ends]
    return(sta,end)


@st.cache_data
def select_top_n_highest_slope(df, n): 
    """ select top-n with highest slope in df """
    df = df.sort_values('SLOPE', ascending=False)
    df = df.dropna(subset=['SLOPE'])
    df = df.iloc[0:n].reset_index(drop=True) 
    return df


@st.cache_data
def select_top_n_highest_val_by_origin(df, n, var):
    df = (df.dropna(subset=[var])
      .sort_values(var, ascending=False)
      .groupby("ORIGIN_SOURCE", group_keys=False)
      .head(n).reset_index(drop=True))
    return df


@st.cache_data
def prepre_for_pages_10_13(df, xvar):
    df = df.dropna(subset=[xvar])
    df["ISO_WEEKSTARTDATE_str"] = ("" + df["ISO_WEEKSTARTDATE"].dt.strftime("%Y-%m-%d"))
    df = df.sort_values(xvar, ascending = False)
    return(df)

