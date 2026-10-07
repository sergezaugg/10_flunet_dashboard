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
        # "COUNTRY_AREA_TERRITORY",
        "ORIGIN_SOURCE", 
        "COUNTRY_CODE",
        "ISO_YEAR", "ISO_WEEK", "ISO_WEEKSTARTDATE",
        "SPEC_PROCESSED_NB",
        "INF_A", "INF_B", "INF_ALL",
        ]
    df = df[columns].copy()
    # re-name variables 
    df = df.rename(columns={"COUNTRY_CODE": "COUNTRY"})
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


@st.cache_data()
def filter_data(df, prop_non_na_tol = 0.50, mean_count_tol = 40, 
                who_regions = ['EUR'], fse_regions = ['aa'], itz_regions = ['bb']):
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
    return(df)

@st.cache_data()
def filter_a_data_source(df, c):
    df = df[df["ORIGIN_SOURCE"] == c]
    return(df)

#-----------------------------------------
# rolling functions 

# @st.cache_data()
# def rolling_consecutive(g, bin_size):
#     d = g["ISO_WEEKSTARTDATE"]
#     consecutive = d.diff().eq(pd.Timedelta(days=7))
#     streak = consecutive.groupby((~consecutive).cumsum()).cumsum() + 1
#     ma = g["INF_ALL"].rolling(bin_size, min_periods=bin_size, center=False).mean()
#     return ma.where(streak >= bin_size)

def cond_expect_last_polyfit(y, deg=1):
    """
    Conditional expectaion at last week from polynomial regression.
    To be used by polyreg_by_country for curve smoothing 
    """
    n = len(y)
    x = np.arange(n)
    coef = np.polyfit(x, y, deg)
    return np.polyval(coef, n - 1)



@st.cache_data
def polyreg_by_country_only(df, bin_size, deg):
    df = df.sort_values(["COUNTRY", "ISO_WEEKSTARTDATE"]).copy()
    df["INF_MA"] = (
        df.groupby("COUNTRY")["INF_ALL"]
          .rolling(bin_size, min_periods=bin_size)
          .apply(lambda y: cond_expect_last_polyfit(y, deg), raw=True)
          .reset_index(level=0, drop=True)
    )
    return df


@st.cache_data
def polyreg_by_country_source(df, bin_size, deg):
    df = df.sort_values(["ORIGIN_SOURCE", "COUNTRY", "ISO_WEEKSTARTDATE"]).copy()
    df["INF_MA"] = (
        df.groupby(["ORIGIN_SOURCE", "COUNTRY"])["INF_ALL"]
          .rolling(bin_size, min_periods=bin_size)
          .apply(lambda y: cond_expect_last_polyfit(y, deg), raw=True)
          .reset_index(level=[0, 1], drop=True)
    )
    # ad-hoc corrections
    df.loc[df["INF_MA"] < 0.0, "INF_MA"] = 0.0
    df["INF_MA"] = df["INF_MA"].fillna(0.0)
    return df


@st.cache_data
def get_baseline_count(df, q):
    """
    fill-in 0.0 where "INF_ALL" is NA or make new row with "INF_ALL"=0.0 where WEEKSTARTDATE row is missing      
    then compute quantile of "INF_ALL" for each "COUNTRY" x "ORIGIN_SOURCE"
    """
    df = df[["ORIGIN_SOURCE", "COUNTRY", "ISO_WEEKSTARTDATE", "INF_ALL"]].copy()

    df["ISO_WEEKSTARTDATE"] = pd.to_datetime(df["ISO_WEEKSTARTDATE"])

    # Ensure one row per source × country × week
    df = (
        df.groupby(
            ["ORIGIN_SOURCE", "COUNTRY", "ISO_WEEKSTARTDATE"],
            as_index=False
        )["INF_ALL"]
        .sum(min_count=1)
    )

    # Add missing weeks and replace NA with 0
    df = (
        df.set_index("ISO_WEEKSTARTDATE")
        .groupby(["ORIGIN_SOURCE", "COUNTRY"])["INF_ALL"]
        .apply(
            lambda x: x.reindex(
                pd.date_range(
                    x.index.min(),
                    x.index.max(),
                    freq="W-MON"
                )
            ).fillna(0.0)
        )
        .rename("INF_ALL")
        .reset_index()
    )

    # Quantile baseline
    baseline_thlds = (
        df.groupby(["COUNTRY", "ORIGIN_SOURCE"])["INF_ALL"]
        .quantile(q)
        .reset_index(name="INF_ALL_BASELINE")
    )

    return baseline_thlds


@st.cache_data()
def get_latest_date_per_group(df, ts_today):
    """
    Get latest date of available data per COUNTRY and ORIGIN_SOURCE
    """
    df = df[["COUNTRY" , "ORIGIN_SOURCE", "WHOREGION", "FLUSEASON", "ISO_WEEKSTARTDATE" , "INF_ALL",]]
    df = df.dropna(subset=["INF_ALL"])
    df = df.loc[df.groupby(["COUNTRY", "ORIGIN_SOURCE"])["ISO_WEEKSTARTDATE"].idxmax()]
    df = df.drop(columns = ["INF_ALL"])
    # derive variable and convert types
    df["days_since"] = (ts_today - df["ISO_WEEKSTARTDATE"]).dt.days
    df["Latest date"] = (df["ISO_WEEKSTARTDATE"].dt.strftime("%Y-%m-%d"))

    return df


@st.cache_data()
def select_global_date_range(df, sta, end):
    df = df[df["ISO_WEEKSTARTDATE"].between(sta, end)]
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
def get_3_dfs_by_recency_for_top_n_slope(df, latest_week, slope_thld = 0.0, n_weeks_for_slope = 4):
    """
    TBD
    """
    # take 5 most recent weeks per country  
    week_0 = latest_week - pd.Timedelta(weeks=5)
    df0 = df[df['ISO_WEEKSTARTDATE'] >= week_0]
    
    # keep 3 most recent per country
    df0 = df0.sort_values("ISO_WEEKSTARTDATE", ascending=False).groupby("COUNTRY").head(n_weeks_for_slope) 
    df0 = df0.sort_values(["COUNTRY", "ISO_WEEKSTARTDATE"], ascending=[True, False])

    # compute slope from linear regression
    df0["SLOPE"] = (df0.groupby("COUNTRY").apply(
           lambda g: (
               np.polyfit((
                   # x normalize to 1 unit = week
                   g.loc[g["INF_MA"].notna(), "ISO_WEEKSTARTDATE"] - g["ISO_WEEKSTARTDATE"].min()).dt.days / 7,
                   # that is y
                   g.loc[g["INF_MA"].notna(), "INF_MA"],
                   # degree 1 = linear regression
                   1
               )[0] # this is b1 = slope
               if g["INF_MA"].notna().sum() >= 2
               else np.nan
           ),
           include_groups=False
       )
       .reindex(df0["COUNTRY"])
       .to_numpy()
    )

    # keep only latest row per country
    df1 = df0.sort_values("ISO_WEEKSTARTDATE", ascending=False).groupby("COUNTRY").head(1) 
    df1 = df1.sort_values(["COUNTRY"], ascending=[True])

    # prepare overview df for another use
    df_slopes_all = df1.copy()
    df_slopes_all = df_slopes_all[df_slopes_all['SLOPE'] > slope_thld]
    df_slopes_all = df_slopes_all.sort_values("SLOPE", ascending=False)
    
    return df_slopes_all


# @st.cache_data()
# def keep_n_most_recent_weeks(df, keep_n_weeks):
#     """ keep only n most recent weeks with respect to values in current df"""
#     cutoff_week = df['ISO_WEEKSTARTDATE'].max() - pd.Timedelta(weeks=keep_n_weeks, days=1)
#     df = df[df["ISO_WEEKSTARTDATE"] > cutoff_week]
#     return df

@st.cache_data()
def keep_n_most_recent_weeks_2(df, ref_date, keep_n_weeks):
    """ keep only n most recent weeks with respect to values in current df"""
    cutoff_week = ref_date - pd.Timedelta(weeks=keep_n_weeks, days=1)
    df = df[df["ISO_WEEKSTARTDATE"] > cutoff_week]
    # return time range 
    xrange = [ref_date - pd.Timedelta(weeks=keep_n_weeks, days=1), ref_date]
    return df, xrange




@st.cache_data
def prepre_for_pages_10_13(df, xvar):
    df = df.dropna(subset=[xvar])
    df["ISO_WEEKSTARTDATE_str"] = ("Updated " + df["ISO_WEEKSTARTDATE"].dt.strftime("%Y-%m-%d"))
    df = df.sort_values(xvar, ascending = False)
    return(df)

