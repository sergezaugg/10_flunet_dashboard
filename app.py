#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# run locally : streamlit run stmain.py
#--------------------

import pandas as pd
import streamlit as st
from streamlit import session_state as ss
from src.utils import download_flunet_data, preprocess_flunet_data
from src.utils import sum_over_origin_source, concat_and_sort

st.set_page_config(layout = "wide", initial_sidebar_state = "expanded")
st.logo(image='pics/z_logo_orange.png', size="large", link="https://github.com/sergezaugg")

# download and pre-process (do once)
df_dat, download_ts = download_flunet_data()
df_data = preprocess_flunet_data(df = df_dat)
df_sumall = sum_over_origin_source(df = df_data)
df_data = concat_and_sort(df_data, df_sumall)

# set global params
MAX_COUNTRIES_IN_PLOTS = 30

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
ss.setdefault("df_sumall", df_sumall)

ss.setdefault("df_data_reg", df_data.iloc[[0]])
ss.setdefault("df_data_itz", df_data.iloc[[0]])
ss.setdefault("WHOREGION_levels", WHOREGION_levels)
ss.setdefault("FLUSEASON_levels", FLUSEASON_levels)

ss.setdefault("ITZ_levels", ITZ_levels)
ss.setdefault("ITZ_levels_AFR", ITZ_levels_AFR)
ss.setdefault("ITZ_levels_AMC", ITZ_levels_AMC)
ss.setdefault("ITZ_levels_ASI", ITZ_levels_ASI)
ss.setdefault("ITZ_levels_EUR", ITZ_levels_EUR)
ss.setdefault("ITZ_levels_OCE", ITZ_levels_OCE)

ss.setdefault("MAX_COUNTRIES_IN_PLOTS", MAX_COUNTRIES_IN_PLOTS)

# defaults for WHOREGION (page 00)
ss.setdefault("k_who_01", ss.WHOREGION_levels.tolist())
ss.setdefault("k_who_02", ss.FLUSEASON_levels.tolist())
ss.setdefault("k_who_04", 0.80)
ss.setdefault("k_who_05", 30)

# defaults for ITZ (page 01)
# ss.setdefault("k_itz_03", ss.ITZ_levels.to_numpy().tolist()) # we want it empty 
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

# Protects every key from being deleted (for multipage consistency)
for key in list(st.session_state.keys()):
    st.session_state[key] = st.session_state[key]

# build control items in sidebar
with st.sidebar:
    st.markdown(f""":primary[**Interactive Exploration of FluNet data**]
    Download: {download_ts}""")
    
# make navigation
p0 = st.Page("pages/st_page_00.py", title="Case History by Regions")
p1 = st.Page("pages/st_page_01.py", title="Case History by ITZ")
p2 = st.Page("pages/st_page_02.py", title="Wave Onset")
p3 = st.Page("pages/st_page_03.py", title="Type A vs B")
p4 = st.Page("pages/st_page_04.py", title="Explore Mov. Avge")
p5 = st.Page("pages/st_page_05.py", title="Top inc. cases")

pg = st.navigation([p5, p0, p1, p2, p3, p4], position="top")
pg.run()


   
   












