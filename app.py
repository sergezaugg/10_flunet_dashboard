#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# run locally : streamlit run stmain.py
#--------------------

import os
import numpy as np
import pandas as pd
import streamlit as st
from streamlit import session_state as ss
from src.utils import download_flunet_data, get_ts_today, preprocess_flunet_data, get_latest_date_per_group, select_global_date_range
from src.utils import get_recency_slope, keep_n_most_recent_weeks_2, polyreg_by_country_source
from src.utils import get_baseline_count
from datetime import datetime

pd.set_option('display.max_rows', 500)

st.set_page_config(layout = "wide", initial_sidebar_state = "expanded")
st.logo(image='pics/z_logo_red.png', size="large", link="https://github.com/sergezaugg")

ss.setdefault("ts_today", get_ts_today())

# download and pre-process (do once)
df_dat, ts_download = download_flunet_data()
df_data_all = preprocess_flunet_data(df = df_dat)

# initialise global dates parameters
ss.setdefault("date_init", [df_data_all["ISO_WEEKSTARTDATE"].min(), df_data_all["ISO_WEEKSTARTDATE"].max()])
ss.setdefault("k_set_01",  [df_data_all["ISO_WEEKSTARTDATE"].min(), df_data_all["ISO_WEEKSTARTDATE"].max()])

# update global time range
df_data = select_global_date_range(df_data_all, sta = ss.k_set_01[0], end = ss.k_set_01[1])
df_latest_data = get_latest_date_per_group(df_data, ts_today = ss.ts_today)

ss.latest_week = df_data['ISO_WEEKSTARTDATE'].max()


#--------------------------------------
# (1) advanced pre-processing (Slope)

ss.nw_ma = 20 # 15
ss.ma_bin_size = 4
ss.ma_degree = 1
ss.nw_slo = 5 # 4

# load data to local page 
df_ma = df_data.copy()
df_ma = df_ma[['COUNTRY', 'ORIGIN_SOURCE', 'ISO_WEEKSTARTDATE', 'INF_ALL']]
df_ma, trace_x_range_ma = keep_n_most_recent_weeks_2(df_ma, ref_date = ss.ts_today, keep_n_weeks = ss.nw_ma)
df_trace_ma = polyreg_by_country_source(df_ma, bin_size = ss.ma_bin_size, deg = ss.ma_degree)

# regression - advanced pre-processing (used in pages 05 and 10)
df0 = df_trace_ma.copy()
df_metri_ma = [(get_recency_slope(
            df0[df0["ORIGIN_SOURCE"] == a], 
            latest_week = ss.latest_week, 
            slope_thld = 0.1, 
            n_weeks_for_slope = ss.nw_slo
        )) for a in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]]

df_metri_ma = pd.concat(df_metri_ma, ignore_index=True)

# save to ss
ss.df_trace_ma = df_trace_ma
ss.trace_x_range_ma = trace_x_range_ma
ss.df_metri_ma = df_metri_ma
del(df_ma, df0, df_trace_ma, trace_x_range_ma, df_metri_ma)
#--------------------------------------







#--------------------------------------
# (2) advanced pre-processing (above Baseline)

# define time ranges in weeks 
ss.time_range_basli = 52*5
ss.quantile_val = 0.65
ss.time_range_trace = 24
ss.time_range_stats = 6

# load data to local page 
df_bl = df_data.copy()

# keep last 5 years to compute baseline 
df_bl, _ = keep_n_most_recent_weeks_2(df_bl, ref_date = ss.ts_today, keep_n_weeks = ss.time_range_basli)
# get flu baseline counts (for all countries)
bl_thld = get_baseline_count(df_bl, q = ss.quantile_val)

# reduce to fewer recent weeks for trace plots
df_trace, trace_x_range = keep_n_most_recent_weeks_2(df_bl, ref_date = ss.ts_today, keep_n_weeks = ss.time_range_trace)

# reduce even fewer recent weeks for recent stats (below)
df00, stats_x_range = keep_n_most_recent_weeks_2(df_trace, ref_date = ss.ts_today, keep_n_weeks = ss.time_range_stats)

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

# save to ss
ss.df_metri_bl = df_metri
ss.df_trace_bl = df_trace
ss.trace_x_range_bl = trace_x_range
ss.stats_x_range_bl = stats_x_range
# clean-up namespace
del(df00, df_bl, bl_thld, df_metri, df_trace, trace_x_range, stats_x_range)
#--------------------------------------







# update data dependent objects
ss.df_data = df_data
ss.df_latest_data = df_latest_data

ss.ts_latest_data = df_data['ISO_WEEKSTARTDATE'].max()
ss.date_range_dt = [df_data["ISO_WEEKSTARTDATE"].min().date(), df_data["ISO_WEEKSTARTDATE"].max().date()]

# get top 3 weeks and delay to today 
ss.top3_weeks =  df_data["ISO_WEEKSTARTDATE"].drop_duplicates().sort_values(ascending=False).head(3)

ss.delays_days = ((ss.ts_today - ss.top3_weeks).dt.days).tolist()

ss.all_iso_week_start_dates = sorted(df_data["ISO_WEEKSTARTDATE"].dropna().unique())


# initialize session state (constant values)
ss.setdefault("colors_recency", ["#00ff55", "yellow", "orange", "red"])
ss.setdefault("MAX_COUNTRIES_IN_PLOTS", 20)
ss.setdefault("ITZ_levels_AFR", ['EST_AFR', 'MID_AFR', 'NRT_AFR', 'STH_AFR', 'WST_AFR'])
ss.setdefault("ITZ_levels_AMC", ['CNT_AMC', 'NRT_AMR', 'TEMP_SAMR', 'TRP_SAMR'])
ss.setdefault("ITZ_levels_ASI", ['CNT_ASIA', 'EST_ASIA', 'SE_ASIA', 'STH_ASIA', 'WST_ASIA'])
ss.setdefault("ITZ_levels_EUR", ['EST_EUR', 'NTH_EUR', 'SW_EUR'])
ss.setdefault("ITZ_levels_OCE", ['OCE_MEL_POL'])

# initialize session state (data dependent values that need initialized once)
ss.setdefault("WHOREGION_levels", df_data["WHOREGION"].unique())
ss.setdefault("FLUSEASON_levels", df_data["FLUSEASON"].unique())
ss.setdefault("ITZ_levels", df_data["ITZ"].unique().tolist())
ss.setdefault("ALL_COUNTRIES", df_data['COUNTRY'].unique())


#------------------------------
# widget defaults

# defaults for WHOREGION (page 00)
ss.setdefault("k_who_01", ss.WHOREGION_levels.tolist())
ss.setdefault("k_who_02", ss.FLUSEASON_levels.tolist())
ss.setdefault("k_who_04", 0.80)
ss.setdefault("k_who_05", 30)
ss.setdefault("k_who_06", [])

# defaults for recency (page 08)
ss.setdefault("k_rec_01", ss.WHOREGION_levels.tolist())
ss.setdefault("k_rec_02", ss.FLUSEASON_levels.tolist())

# defaults for WHOREGION - positivity (page 06)
ss.setdefault("k_who_pos_01", ss.WHOREGION_levels.tolist())
ss.setdefault("k_who_pos_02", ss.FLUSEASON_levels.tolist())
ss.setdefault("k_who_pos_04", 0.80)
ss.setdefault("k_who_pos_05", 30)

# defaults for ITZ (page 01)
ss.setdefault("k_itz_04", 0.30)
ss.setdefault("k_itz_05", 10)

# defaults for wave onset (page 02)
ss.setdefault("k_wave_01", 10)
ss.setdefault("k_wave_02", ss.date_range_dt)
ss.setdefault("k_wave_03", True)
ss.setdefault("k_wave_04", True)
ss.setdefault("k_wave_05", 125)

# defaults for A vs B (page 03)
ss.setdefault("k_ab_01", 10)
ss.setdefault("k_ab_02", 600)
ss.setdefault("k_ab_03", 50)

# defaults for moving average explorer (page 04)
ss.setdefault("k_tre_02", 5)
ss.setdefault("k_tre_03", 1)
ss.setdefault("k_tre_04", 1)
ss.setdefault("k_tre_05", 0.66)

# Protects every key from being deleted (for multi-page consistency across clicks)
for key in list(st.session_state.keys()):
    st.session_state[key] = st.session_state[key]

# build sidebar
with st.sidebar:
    st.markdown(f""":primary[**Interactive Exploration of FluNet data**]  
    Ref date: \t{ss.ts_today.strftime("%Y-%m-%d")}  
    Downloaded: \t{ts_download}  
    Latest data: \t{ss.ts_latest_data.strftime("%Y-%m-%d")}
    """)
    st.divider()
    
# make navigation
p0 = st.Page("pages/st_page_00.py", title="💡 By Regions")
# p1 = st.Page("pages/st_page_01.py", title="💡 By ITZ") # this one is redundant with p0
p2 = st.Page("pages/st_page_02.py", title="🔎 Wave Onset")
p3 = st.Page("pages/st_page_03.py", title="🔎 Type A vs B")
p4 = st.Page("pages/st_page_04.py", title="🔎 Explore")
p5 = st.Page("pages/st_page_05.py", title="🔥 Top Risers")
# p6 = st.Page("pages/st_page_06.py", title="💡 Positivity by Regions") # not show yet, under developments
p7 = st.Page("pages/st_page_07.py", title="🔬 Tabular")
p8 = st.Page("pages/st_page_08.py", title="🔬 Data age")
p9 = st.Page("pages/st_page_09.py", title="⚙️ Settings")
p10 = st.Page("pages/st_page_10.py", title="💡 All Risers")
p11 = st.Page("pages/st_page_11.py", title="🔥 Top High")
p12 = st.Page("pages/st_page_12.py", title="📋 Info")
p13 = st.Page("pages/st_page_13.py", title="💡 All High")

p_dev = st.Page("pages/st_dev.py", title="💀 Dev")

pg = st.navigation([p5, p11, p10, p13, p0, p2, p3, p4, p7, p8, p9, p12, p_dev], position="top")
pg.run()















