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
from src.utils import download_flunet_data, preprocess_flunet_data, get_latest_date_per_group, select_global_date_range
from src.utils import keep_n_most_recent_weeks, polyreg_by_country_only, get_3_dfs_by_recency_for_top_n_slope
from datetime import datetime

pd.set_option('display.max_rows', 500)

st.set_page_config(layout = "wide", initial_sidebar_state = "expanded")
st.logo(image='pics/z_logo_red.png', size="large", link="https://github.com/sergezaugg")

# download and pre-process (do once)
df_dat, ts_download = download_flunet_data()
df_data_all = preprocess_flunet_data(df = df_dat)

# initialise global dates parameters
ss.setdefault("date_init", [df_data_all["ISO_WEEKSTARTDATE"].min(), df_data_all["ISO_WEEKSTARTDATE"].max()])
ss.setdefault("k_set_01",  [df_data_all["ISO_WEEKSTARTDATE"].min(), df_data_all["ISO_WEEKSTARTDATE"].max()])

# update global time range ()
df_data = select_global_date_range(df_data_all, sta = ss.k_set_01[0], end = ss.k_set_01[1])
df_latest_data = get_latest_date_per_group(df_data)

ss.latest_week = df_data['ISO_WEEKSTARTDATE'].max()


# advanced pre-processing
slope_dfs_by_source = {}
for dasou in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]:
    df = df_data
    df = df[df["ORIGIN_SOURCE"] == dasou]
    df = keep_n_most_recent_weeks(df, keep_n_weeks = 15)
    df = polyreg_by_country_only(df, bin_size = 4, deg = 1)
    nw_slo = 5
    df_dat00, df_dat01, df_dat02, df_slopes_all = get_3_dfs_by_recency_for_top_n_slope(df, ss.latest_week, 
        slope_thld = 0.1, n_weeks_for_slope = nw_slo)
    slope_dfs_by_source[dasou] = [df_dat00, df_dat01, df_dat02, df_slopes_all]


# update data dependent objects
ss.df_data = df_data
ss.df_latest_data = df_latest_data

ss.slope_dfs_by_source = slope_dfs_by_source

ss.ts_latest_data = df_data['ISO_WEEKSTARTDATE'].max()
ss.date_range_dt = [df_data["ISO_WEEKSTARTDATE"].min().date(), df_data["ISO_WEEKSTARTDATE"].max().date()]

# get top 3 weeks and delay to today 
ss.top3_weeks =  df_data["ISO_WEEKSTARTDATE"].drop_duplicates().sort_values(ascending=False).head(3)
ss.setdefault("ts_today", datetime.now())
ss.delays_days = ((ss.ts_today - ss.top3_weeks).dt.days).tolist()


ss.all_iso_week_start_dates = sorted(df_data["ISO_WEEKSTARTDATE"].dropna().unique())


# initialize session state (constant values)
ss.setdefault("colors_recency", ["#00ff55", "yellow", "orange", "red"])
ss.setdefault("MAX_COUNTRIES_IN_PLOTS", 30)
ss.setdefault("ITZ_levels_AFR", ['EST_AFR', 'MID_AFR', 'NRT_AFR', 'STH_AFR', 'WST_AFR'])
ss.setdefault("ITZ_levels_AMC", ['CNT_AMC', 'NRT_AMR', 'TEMP_SAMR', 'TRP_SAMR'])
ss.setdefault("ITZ_levels_ASI", ['CNT_ASIA', 'EST_ASIA', 'SE_ASIA', 'STH_ASIA', 'WST_ASIA'])
ss.setdefault("ITZ_levels_EUR", ['EST_EUR', 'NTH_EUR', 'SW_EUR'])
ss.setdefault("ITZ_levels_OCE", ['OCE_MEL_POL'])

# initialize session state (data dependent values that need initialized once)
ss.setdefault("ts_download", ts_download)
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
    Today: \t{ss.ts_today.strftime("%Y-%m-%d")}  
    Downloaded: \t{ts_download.strftime("%Y-%m-%d")}  
    Latest data: \t{ss.ts_latest_data.strftime("%Y-%m-%d")}
    """)
    st.divider()
    
# make navigation
p0 = st.Page("pages/st_page_00.py", title="Cases by Regions")
p1 = st.Page("pages/st_page_01.py", title="Cases by ITZ")
p2 = st.Page("pages/st_page_02.py", title="Wave Onset")
p3 = st.Page("pages/st_page_03.py", title="Type A vs B")
p4 = st.Page("pages/st_page_04.py", title="Explore Mov. Avg")
p5 = st.Page("pages/st_page_05.py", title="Top Risers!")
p6 = st.Page("pages/st_page_06.py", title="Positivity by Regions")
p7 = st.Page("pages/st_page_07.py", title="Tabular Explorer")
p8 = st.Page("pages/st_page_08.py", title="Data recency")
p9 = st.Page("pages/st_page_09.py", title="Settings")
p10 = st.Page("pages/st_page_10.py", title="Flu inc overview")
p_dev = st.Page("pages/st_dev.py", title="Devel")

pg = st.navigation([p5, p10, p8, p0, p1, p6, p2, p3, p4, p7, p9, p_dev], position="top")
pg.run()


   












