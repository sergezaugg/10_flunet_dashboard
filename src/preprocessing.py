#--------------------             
# Author : Serge Zaugg
# Description : advanced preprocessing functions 
#--------------------

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

@st.cache_data()
def keep_n_most_recent_weeks_2(df, ref_date, keep_n_weeks):
    """ keep only n most recent weeks with respect to values in current df"""
    cutoff_week = ref_date - pd.Timedelta(weeks=keep_n_weeks, days=1)
    df = df[df["ISO_WEEKSTARTDATE"] > cutoff_week]
    # return time range 
    xrange = [ref_date - pd.Timedelta(weeks=keep_n_weeks, days=1), ref_date]
    return df, xrange

@st.cache_data
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
def polyreg_by_country_source(df, bin_size, deg):
    df = df.sort_values(["ORIGIN_SOURCE", "COUNTRY", "ISO_WEEKSTARTDATE"]).copy()
    df["INF_MA"] = (
        df.groupby(["ORIGIN_SOURCE", "COUNTRY"])["INF_ALL"]
          .rolling(bin_size, min_periods=bin_size)
          .apply(lambda y: cond_expect_last_polyfit(y, deg), raw=True)
          .reset_index(level=[0, 1], drop=True)
    )
    # ad-hoc corrections
    df.loc[df["INF_MA"] < 0.0, "INF_MA"] = 0.0 # replace neg val by 0.0
    # df["INF_MA"] = df["INF_MA"].fillna(0.0) # replace NAs by 0.0 (probably bad idea)
    return df

@st.cache_data
def get_recency_slope(df):
    """
    TBD
    """
    # keep most recent per country (legacy - probably not needed)
    df0 = df # .sort_values("ISO_WEEKSTARTDATE", ascending=False).groupby("COUNTRY").head(n_weeks_for_slope) 
    df0 = df0.sort_values(["COUNTRY", "ISO_WEEKSTARTDATE"], ascending=[True, False])
    # compute slope from linear regression
    df0["SLOPE"] = (df0.groupby("COUNTRY").apply(
           lambda g: (
               np.polyfit((
                   g.loc[g["INF_MA"].notna(), "ISO_WEEKSTARTDATE"] - g["ISO_WEEKSTARTDATE"].min()).dt.days / 7, # x normalize to 1 unit = week
                   g.loc[g["INF_MA"].notna(), "INF_MA"], # that is y
                   1 # degree 1 = linear regression
               )[0] # this is b1 = slope
               if g["INF_MA"].notna().sum() >= 3
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
    df_slopes_all = df1.sort_values("SLOPE", ascending=False)
    
    return df_slopes_all

@st.cache_data
def get_baseline_count(df, q):
    """
    fill-in 0.0 where "INF_ALL" is NA or make new row with "INF_ALL"=0.0 where WEEKSTARTDATE row is missing      
    then compute quantile of "INF_ALL" for each "COUNTRY" x "ORIGIN_SOURCE"
    """
    df = df[["ORIGIN_SOURCE", "COUNTRY", "CNTRY", "ISO_WEEKSTARTDATE", "INF_ALL"]].copy()

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

#-----------------------------
# main functions 

@st.cache_data
def compute_recent_slope(df_data, nw_ma, ma_bin_size, ma_degree, nw_slo, ref_date):
    """ advanced pre-processing (Slope) """
    df_ma = df_data # .copy()
    df_ma = df_ma[['COUNTRY', 'CNTRY' , 'ORIGIN_SOURCE', 'ISO_WEEKSTARTDATE', 'INF_ALL']]
    df_ma, trace_x_range_ma = keep_n_most_recent_weeks_2(df_ma, ref_date = ref_date, keep_n_weeks = nw_ma)
    df_trace_ma = polyreg_by_country_source(df_ma, bin_size = ma_bin_size, deg = ma_degree)
    # regression
    df0 = df_trace_ma.copy()
    df0, stats_x_range = keep_n_most_recent_weeks_2(df0, ref_date = ref_date, keep_n_weeks = nw_slo)
    df_metri_ma = [get_recency_slope(df0[df0["ORIGIN_SOURCE"] == a]) for a in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]]
    df_metri_ma = pd.concat(df_metri_ma, ignore_index=True)
    return df_trace_ma, trace_x_range_ma, df_metri_ma, stats_x_range

@st.cache_data
def compute_recent_level(df_data, time_range_basli, quantile_val, time_range_trace, time_range_stats, ref_date):
    """ """
    df_bl = df_data # .copy()
    # keep last 5 years to compute baseline 
    df_bl, _ = keep_n_most_recent_weeks_2(df_bl, ref_date = ref_date, keep_n_weeks = time_range_basli)
    # get flu baseline counts (for all countries)
    bl_thld = get_baseline_count(df_bl, q = quantile_val)
    # reduce to fewer recent weeks for trace plots
    df_trace, trace_x_range = keep_n_most_recent_weeks_2(df_bl, ref_date = ref_date, keep_n_weeks = time_range_trace)
    # reduce even fewer recent weeks for recent stats (below)
    df00, stats_x_range = keep_n_most_recent_weeks_2(df_trace, ref_date = ref_date, keep_n_weeks = time_range_stats)
    # merge-in baseline threshold 
    df00 = df00.merge(bl_thld, on=["COUNTRY", "ORIGIN_SOURCE"], how="left")
    # get stats to display in metric boxes
    df_metri = (df00
        # remove when all-na for "INF_ALL" 
        .loc[df00.groupby(["COUNTRY", "ORIGIN_SOURCE"])["INF_ALL"].transform("count").gt(0)]  
        .assign(ABOVE_BASELINE=lambda x: x["INF_ALL"] >= x["INF_ALL_BASELINE"]) # create boolean for 'above bl'
        .groupby(["COUNTRY", "ORIGIN_SOURCE"], as_index=False) # extract summaries by group
        .agg(N_ABOVE_BASELINE=("ABOVE_BASELINE", "sum"),
            INF_ALL_BASELINE=("INF_ALL_BASELINE", "first"),
            ISO_WEEKSTARTDATE=("ISO_WEEKSTARTDATE", "max"),
            CNTRY=("CNTRY", "first"),
            )
        .sort_values("N_ABOVE_BASELINE", ascending=False) # sort   
    )
    return(df_trace, trace_x_range, df_metri, stats_x_range)

@st.cache_data
def combine_bl_and_slope_summaries(dfma_temp, dfbl_temp):
    dfma_temp = dfma_temp.dropna(subset=["SLOPE"])
    dfmerged = dfbl_temp.merge(dfma_temp, on=["COUNTRY", "ORIGIN_SOURCE"], how="outer", suffixes=("_bl", "_slo"))
    # keep only one "latest date" column
    dfmerged["ISO_WEEKSTARTDATE"] = (dfmerged[["ISO_WEEKSTARTDATE_slo", "ISO_WEEKSTARTDATE_bl"]].bfill(axis=1).iloc[:, 0])
    dfmerged = dfmerged.drop(columns = ["ISO_WEEKSTARTDATE_slo", "ISO_WEEKSTARTDATE_bl"])
    # remove redundant columns
    dfmerged = dfmerged.drop(columns = ['CNTRY_bl'])
    dfmerged = dfmerged.rename(columns={"CNTRY_slo": "CNTRY"})
    # safeguard - keep where BL-threshold enough above 0
    dfmerged = dfmerged[dfmerged["INF_ALL_BASELINE"] >= 2] 
    # compute percent change 
    attenuation_term = 4.0
    dfmerged['PERC_CHANGE'] = (100*(dfmerged['SLOPE']  / (dfmerged['INF_ALL_BASELINE']+attenuation_term))).round(1)
    return dfmerged

