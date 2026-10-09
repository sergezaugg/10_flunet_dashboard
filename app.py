#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# run locally : streamlit run stmain.py
#--------------------

import pandas as pd
import streamlit as st
from streamlit import session_state as ss
from src.utils import download_flunet_data, get_ts_today, preprocess_flunet_data, get_latest_date_per_group
from src.preprocessing import compute_recent_slope, compute_recent_level

st.set_page_config(layout = "wide", initial_sidebar_state = "expanded")
st.logo(image='pics/z_logo_red.png', size="large", link="https://github.com/sergezaugg")
pd.set_option('display.max_rows', 500)


# weeks from ref to be used for stats 
ss.nw_global = 6
ss.top_n = 5 # how much to show in 'top' pages

#------------------------------
# initialize session state (constant values)
ss.max_countries_in_plots = 20
# (1) advanced pre-processing (Slope)
ss.nw_ma = 20 # 15
ss.ma_bin_size = 4
ss.ma_degree = 1
ss.nw_slo = ss.nw_global 
# (2) advanced pre-processing (above Baseline)
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


# new - remove all data that is too old already here 
mask = ss.df_latest_data[['COUNTRY', 'ORIGIN_SOURCE', 'days_since']]
mask = mask[mask['days_since'] <= (ss.nw_global)*7] # 
ss.df_data = ss.df_data.merge(mask, on=["COUNTRY", "ORIGIN_SOURCE"], how="right")












# (1) advanced pre-processing (Slope)
obj = compute_recent_slope(ss.df_data, ss.nw_ma, ss.ma_bin_size, ss.ma_degree, ss.nw_slo, ss.ts_today)
ss.df_trace_ma, ss.trace_x_range_ma, dfma_temp, ss.stats_x_range_ma = obj # unwrap

# (2) advanced pre-processing (above Baseline)
obj = compute_recent_level(ss.df_data, ss.time_range_basli, ss.quantile_val, ss.time_range_trace, ss.time_range_stats, ss.ts_today)
ss.df_trace_bl, ss.trace_x_range_bl, dfbl_temp, ss.stats_x_range_bl = obj # unwrap

# temp for p14
ss.dfbl_temp = dfbl_temp





# dev ---- 
# merge slope and BL dfs
dfma_temp = dfma_temp.dropna(subset=["SLOPE"])
dfmerged = dfbl_temp.merge(dfma_temp, on=["COUNTRY", "ORIGIN_SOURCE"], how="outer", suffixes=("_bl", "_slo"))
# keep only one "latest date" column
dfmerged["ISO_WEEKSTARTDATE"] = (dfmerged[["ISO_WEEKSTARTDATE_slo", "ISO_WEEKSTARTDATE_bl"]].bfill(axis=1).iloc[:, 0])
dfmerged = dfmerged.drop(columns = ["ISO_WEEKSTARTDATE_slo", "ISO_WEEKSTARTDATE_bl"])
# keep only one country full name column
dfmerged = dfmerged.drop(columns = ['CNTRY_bl'])
dfmerged = dfmerged.rename(columns={"CNTRY_slo": "CNTRY"})
# safeguard - keep where BL enough above 0
dfmerged = dfmerged[dfmerged["INF_ALL_BASELINE"] >= 2] 
# compute percent change 
attenuation_term = 4.0
dfmerged['PERC_CHANGE'] = (100*(dfmerged['SLOPE']  / (dfmerged['INF_ALL_BASELINE']+attenuation_term))).round(1)
# assign to ss 
ss.df_metri_merged = dfmerged

# st.dataframe(dfmerged)





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
# widget defaults
# defaults for WHOREGION (page 00)
ss.setdefault("k_who_01", ss.WHOREGION_levels.tolist())
ss.setdefault("k_who_02", ss.FLUSEASON_levels.tolist())
ss.setdefault("k_who_04", 0.80)
ss.setdefault("k_who_05", 30)
ss.setdefault("k_who_06", ['CHE', 'ESP', 'FRA'])
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
    Downloaded: \t{ss.ts_download}  
    Latest data: \t{ss.ts_latest_data.strftime("%Y-%m-%d")}
    """)
    st.divider()
    
# make navigation
p00 = st.Page("pages/st_page_00.py", title="🔎 By Regions")
# p02 = st.Page("pages/st_page_02.py", title="🔎 Wave Onset")
# p03 = st.Page("pages/st_page_03.py", title="🔎 Type A vs B")
p04 = st.Page("pages/st_page_04.py", title="🔎 Methods")
p05 = st.Page("pages/st_page_05.py", title="🔥 Top Trend", default=True)
# p06 = st.Page("pages/st_page_06.py", title="💡 Positivity by Regions") # not show yet, under developments
p07 = st.Page("pages/st_page_07.py", title="🔬 Tabular")
p08 = st.Page("pages/st_page_08.py", title="🔥 Data age")
p10 = st.Page("pages/st_page_10.py", title="🌍 Map Trend")
p11 = st.Page("pages/st_page_11.py", title="🔥 Top Burden")
p12 = st.Page("pages/st_page_12.py", title="📋 Info & Disclaimer")
p13 = st.Page("pages/st_page_13.py", title="🌍 Map Burden")
# p14 = st.Page("pages/st_page_14.py", title="☠️ Dev I")
# p_dev = st.Page("pages/st_dev.py", title="💀 Dev II")

# reduce vertical space between navig and items(content
st.markdown("""
    <style> [data-testid="stMainBlockContainer"] {padding-top: 4rem; padding-left: 3rem;} </style>
    """, unsafe_allow_html=True
)



pg = st.navigation([p08, p05, p11, p10, p13, p00, p04, p07, p12], position="top")
pg.run()















