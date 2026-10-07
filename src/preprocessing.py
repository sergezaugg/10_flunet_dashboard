#--------------------             
# Author : Serge Zaugg
# Description : advanced preprocessing functions 
#--------------------

import streamlit as st
import plotly.express as px
import pandas as pd
from config import cc
from src.utils import keep_n_most_recent_weeks_2, polyreg_by_country_source, get_recency_slope, get_baseline_count

@st.cache_data
def compute_recent_slope(df_data, nw_ma, ma_bin_size, ma_degree, nw_slo, ref_date):
    """ advanced pre-processing (Slope) """
    df_ma = df_data # .copy()
    df_ma = df_ma[['COUNTRY', 'ORIGIN_SOURCE', 'ISO_WEEKSTARTDATE', 'INF_ALL']]
    df_ma, trace_x_range_ma = keep_n_most_recent_weeks_2(df_ma, ref_date = ref_date, keep_n_weeks = nw_ma)
    df_trace_ma = polyreg_by_country_source(df_ma, bin_size = ma_bin_size, deg = ma_degree)
    # regression - advanced pre-processing (used in pages 05 and 10)
    df0 = df_trace_ma.copy()
    df_metri_ma = [(get_recency_slope(
                df0[df0["ORIGIN_SOURCE"] == a], 
                latest_week = ref_date,
                slope_thld = 0.1, 
                n_weeks_for_slope = nw_slo
            )) for a in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]]

    df_metri_ma = pd.concat(df_metri_ma, ignore_index=True)
    return df_trace_ma, trace_x_range_ma, df_metri_ma

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
        .loc[lambda x: x["INF_ALL_BASELINE"] >= 5] # keep where BL enough above 0
        .assign(ABOVE_BASELINE=lambda x: x["INF_ALL"] >= x["INF_ALL_BASELINE"]) # create boolean for 'above bl'
        .groupby(["COUNTRY", "ORIGIN_SOURCE"], as_index=False) # extract summaries by group
        .agg(N_ABOVE_BASELINE=("ABOVE_BASELINE", "sum"),
            INF_ALL_BASELINE=("INF_ALL_BASELINE", "first"),
            ISO_WEEKSTARTDATE=("ISO_WEEKSTARTDATE", "max"),)
        .sort_values("N_ABOVE_BASELINE", ascending=False) # sort   
    )
    return(df_trace, trace_x_range, df_metri, stats_x_range)




