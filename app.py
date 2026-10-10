#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# run locally : streamlit run stmain.py
#--------------------

import pandas as pd
import streamlit as st
from streamlit import session_state as ss
from src.utils import download_flunet_data, get_ts_today, preprocess_flunet_data, get_latest_date_per_group
from src.preprocessing import compute_recent_slope, compute_recent_level, combine_bl_and_slope_summaries
from src.styles import apply_global_styles

#------------------------------
# prepare app 
st.set_page_config(layout = "wide", initial_sidebar_state = "expanded")
apply_global_styles() # apply custom CSS styles 
st.logo(image='pics/z_logo_red.png', size="large", link="https://github.com/sergezaugg")
pd.set_option('display.max_rows', 500)

#------------------------------
# initialize session state (constant values)
ss.max_countries_in_plots = 20
ss.nw_global = 6 # weeks from ref to be used for stats 
ss.top_n = 5 # how much to show in 'top' pages
# (1) advanced pre-processing (slope/percent change)
ss.nw_ma = 20 # 15
ss.ma_bin_size = 4
ss.ma_degree = 1
ss.nw_slo = ss.nw_global 
# (2) advanced pre-processing (burden / above Baseline)
ss.time_range_basli = 52*5
ss.quantile_val = 0.65
ss.time_range_trace = 24
ss.time_range_stats = ss.nw_global

#------------------------------
# download and pre-process (do once)
ss.ts_today = get_ts_today()
df_dat, ss.ts_download = download_flunet_data()
ss.df_data = preprocess_flunet_data(df = df_dat)

# initialize data dependent objects in ss
ss.df_latest_data = get_latest_date_per_group(ss.df_data, ts_today = ss.ts_today)

# remove all data that is too old already here 
mask = ss.df_latest_data[['COUNTRY', 'ORIGIN_SOURCE', 'days_since']]
mask = mask[mask['days_since'] <= (ss.nw_global)*7] # 
ss.df_data = ss.df_data.merge(mask, on=["COUNTRY", "ORIGIN_SOURCE"], how="right")

#------------------------------
# advanced pre-processing

# (1) advanced pre-processing (Slope)
obj = compute_recent_slope(ss.df_data, ss.nw_ma, ss.ma_bin_size, ss.ma_degree, ss.nw_slo, ss.ts_today)
ss.df_trace_ma, ss.trace_x_range_ma, dfma_temp, ss.stats_x_range_ma = obj # unwrap

# (2) advanced pre-processing (Flu Burden above Baseline)
obj = compute_recent_level(ss.df_data, ss.time_range_basli, ss.quantile_val, ss.time_range_trace, ss.time_range_stats, ss.ts_today)
ss.df_trace_bl, ss.trace_x_range_bl, dfbl_temp, ss.stats_x_range_bl = obj # unwrap

# (3) combine bl and slope summaries
ss.df_metri_merged = combine_bl_and_slope_summaries(dfma_temp, dfbl_temp)

# temp for p14
ss.dfbl_temp = dfbl_temp


#------------------------------
if "ts_latest_data" not in ss:
    ss.ts_latest_data   = ss.df_data['ISO_WEEKSTARTDATE'].max()
if "date_range_dt" not in ss:
    ss.date_range_dt    = [ss.df_data["ISO_WEEKSTARTDATE"].min().date(), ss.df_data["ISO_WEEKSTARTDATE"].max().date()]
if "top3_weeks" not in ss:
    ss.top3_weeks       =  ss.df_data["ISO_WEEKSTARTDATE"].drop_duplicates().sort_values(ascending=False).head(3)
if "delays_days" not in ss:
    ss.delays_days      = ((ss.ts_today - ss.top3_weeks).dt.days).tolist()
if "WHOREGION_levels" not in ss:
    ss.WHOREGION_levels = ss.df_data["WHOREGION"].unique()
if "FLUSEASON_levels" not in ss:
    ss.FLUSEASON_levels = ss.df_data["FLUSEASON"].unique()
if "ITZ_levels" not in ss:
    ss.ITZ_levels       = ss.df_data["ITZ"].unique().tolist()
if "ALL_COUNTRIES" not in ss:
    ss.ALL_COUNTRIES    = ss.df_data['COUNTRY'].unique()

#------------------------------
# set widget defaults

# defaults for WHOREGION 
ss.setdefault("k_who_01", ss.WHOREGION_levels.tolist())
ss.setdefault("k_who_02", ss.FLUSEASON_levels.tolist())
ss.setdefault("k_who_04", 0.80)
ss.setdefault("k_who_05", 30)
ss.setdefault("k_who_06", ['CHE', 'ESP', 'FRA'])
# defaults for recency 
ss.setdefault("k_rec_01", ss.WHOREGION_levels.tolist())
ss.setdefault("k_rec_02", ss.FLUSEASON_levels.tolist())
# defaults for WHOREGION - positivity 
ss.setdefault("k_who_pos_01", ss.WHOREGION_levels.tolist())
ss.setdefault("k_who_pos_02", ss.FLUSEASON_levels.tolist())
ss.setdefault("k_who_pos_04", 0.80)
ss.setdefault("k_who_pos_05", 30)
# defaults for ITZ 
ss.setdefault("k_itz_04", 0.30)
ss.setdefault("k_itz_05", 10)
# defaults for wave onset 
ss.setdefault("k_wave_01", 10)
ss.setdefault("k_wave_02", ss.date_range_dt)
ss.setdefault("k_wave_03", True)
ss.setdefault("k_wave_04", True)
ss.setdefault("k_wave_05", 125)
# defaults for A vs B 
ss.setdefault("k_ab_01", 10)
ss.setdefault("k_ab_02", "SENTINEL")
ss.setdefault("k_ab_03", 50)
# defaults for moving average explorer 
ss.setdefault("k_tre_02", 5)
ss.setdefault("k_tre_03", 1)
ss.setdefault("k_tre_04", 1)
ss.setdefault("k_tre_05", 0.66)
# defaults slop geo
ss.setdefault("k_p10_01", "MAXCOMBINE")
ss.setdefault("k_p10_03", "Bluered")
# defaults burden geo
ss.setdefault("k_p13_01", "MAXCOMBINE")
ss.setdefault("k_p13_03", "Viridis")

# Protects every key from being deleted (for multi-page consistency across clicks)
for key in list(st.session_state.keys()):
    st.session_state[key] = st.session_state[key]

#------------------------------
# build app's visible  frontend 

# build sidebar
with st.sidebar:
    st.markdown(f""":primary[**Interactive Exploration of FluNet data**]  
    Ref date: \t{ss.ts_today.strftime("%Y-%m-%d")}  
    Downloaded: \t{ss.ts_download}  
    Latest data: \t{ss.ts_latest_data.strftime("%Y-%m-%d")}
    """)
    st.divider()
    
# make navigation
p01 = st.Page("pages/page_age.py", title="🔥 Data Age")
p02 = st.Page("pages/page_slop_metric.py", title="🔥 Flu Trend", default=True)
p03 = st.Page("pages/page_burd_metric.py", title="🔥 Flu Burden")
p04 = st.Page("pages/page_slop_geo.py", title="🌍 Flu Trend")
p05 = st.Page("pages/page_burd_geo.py", title="🌍 Flu Burden")
p06 = st.Page("pages/page_traces.py", title="🔎 Traces")
p07 = st.Page("pages/page_ab_type.py", title="🔎 Type A vs B")
p08 = st.Page("pages/page_method.py", title="🔎 Illustrate Methods")
p09 = st.Page("pages/page_data.py", title="🔬 Data")
p10 = st.Page("pages/page_info.py", title="📋 Info & Disclaimer")

pg = st.navigation([p01, p02, p03, p04, p05, p06, p07, p08, p09, p10,], position="top")
pg.run()

with st.sidebar:
    st.markdown(f""":gray[v0.5.0 (Beta)]  
    """)
    