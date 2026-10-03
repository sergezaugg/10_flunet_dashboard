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
from datetime import datetime

st.set_page_config(layout = "wide", initial_sidebar_state = "expanded")
st.logo(image='pics/z_logo_orange.png', size="large", link="https://github.com/sergezaugg")

# download and pre-process (do once)
df_dat, ts_download = download_flunet_data()
df_data_all = preprocess_flunet_data(df = df_dat)

# initialise global dates parameters
ss.setdefault("date_init", [df_data_all["ISO_WEEKSTARTDATE"].min(), df_data_all["ISO_WEEKSTARTDATE"].max()])
ss.setdefault("k_set_01",  [df_data_all["ISO_WEEKSTARTDATE"].min(), df_data_all["ISO_WEEKSTARTDATE"].max()])

# update global time range ()
df_data = select_global_date_range(df_data_all, sta = ss.k_set_01[0], end = ss.k_set_01[1])
df_latest_data = get_latest_date_per_group(df_data)

# update data objects
ss.df_data = df_data
ss.df_latest_data = df_latest_data

# get some important dates
ts_today = datetime.now().strftime("%Y-%m-%d")
ts_latest_data = df_data['ISO_WEEKSTARTDATE'].max().strftime("%Y-%m-%d")

# get global data dependent parameters  
min_date_dt      = df_data["ISO_WEEKSTARTDATE"].min().date()
max_date_dt      = df_data["ISO_WEEKSTARTDATE"].max().date()
WHOREGION_levels = df_data["WHOREGION"].unique()
FLUSEASON_levels = df_data["FLUSEASON"].unique()
ITZ_levels       = df_data["ITZ"].unique().tolist()

# Handle ITZ regions 
ITZ_levels_AFR = ['EST_AFR', 'MID_AFR', 'NRT_AFR', 'STH_AFR', 'WST_AFR']
ITZ_levels_AMC = ['CNT_AMC', 'NRT_AMR', 'TEMP_SAMR', 'TRP_SAMR']
ITZ_levels_ASI = ['CNT_ASIA', 'EST_ASIA', 'SE_ASIA', 'STH_ASIA', 'WST_ASIA']
ITZ_levels_EUR = ['EST_EUR', 'NTH_EUR', 'SW_EUR']
ITZ_levels_OCE = ['OCE_MEL_POL']

# initialize session state
ss.setdefault("date_range_dt", [min_date_dt, max_date_dt])
ss.setdefault("df_data", df_data)
ss.setdefault("df_latest_data", df_latest_data)
ss.setdefault("ts_today", datetime.now())
ss.setdefault("ts_latest_data", df_data['ISO_WEEKSTARTDATE'].max())
ss.setdefault("ts_download", ts_download)
ss.setdefault("WHOREGION_levels", WHOREGION_levels)
ss.setdefault("FLUSEASON_levels", FLUSEASON_levels)
ss.setdefault("ITZ_levels", ITZ_levels)
ss.setdefault("ITZ_levels_AFR", ITZ_levels_AFR)
ss.setdefault("ITZ_levels_AMC", ITZ_levels_AMC)
ss.setdefault("ITZ_levels_ASI", ITZ_levels_ASI)
ss.setdefault("ITZ_levels_EUR", ITZ_levels_EUR)
ss.setdefault("ITZ_levels_OCE", ITZ_levels_OCE)
ss.setdefault("MAX_COUNTRIES_IN_PLOTS", 30)
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
ss.setdefault("k_tre_05", 0.5)

# Protects every key from being deleted (for multi-page consistency across clicks)
for key in list(st.session_state.keys()):
    st.session_state[key] = st.session_state[key]

# build sidebar
with st.sidebar:
    st.markdown(f""":primary[**Interactive Exploration of FluNet data**]  
    Today: \t{ts_today}  
    Downloaded: \t{ts_download}  
    Latest data: \t{ts_latest_data}
    """)
    st.divider()
    
# make navigation
p0 = st.Page("pages/st_page_00.py", title="Cases by Regions")
p8 = st.Page("pages/st_page_08.py", title="Data recency")
p1 = st.Page("pages/st_page_01.py", title="Cases by ITZ")
p2 = st.Page("pages/st_page_02.py", title="Wave Onset")
p3 = st.Page("pages/st_page_03.py", title="Type A vs B")
p4 = st.Page("pages/st_page_04.py", title="Explore Mov. Avg")
p5 = st.Page("pages/st_page_05.py", title="Top Risers!")
p6 = st.Page("pages/st_page_06.py", title="Positivity by Regions")
p7 = st.Page("pages/st_page_07.py", title="Tabular Explorer")
p9 = st.Page("pages/st_page_09.py", title="Settings")
p_dev = st.Page("pages/st_dev.py", title="Devel")

pg = st.navigation([p5, p8, p0, p1, p6, p2, p3, p4, p7, p9, p_dev], position="top")
pg.run()


   












