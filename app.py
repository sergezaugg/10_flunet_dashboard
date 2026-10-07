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

# download and pre-process (do once)
df_dat, ts_download = download_flunet_data()
df_data = preprocess_flunet_data(df = df_dat)
ss.ts_today = get_ts_today()




#--------------------------------------
# (1) advanced pre-processing (Slope)
ss.nw_ma = 20 # 15
ss.ma_bin_size = 4
ss.ma_degree = 1
ss.nw_slo = 5 # 4

# compute 
obj = compute_recent_slope(df_data, ss.nw_ma, ss.ma_bin_size, ss.ma_degree, ss.nw_slo, ss.ts_today)
# unwrap
ss.df_trace_ma, ss.trace_x_range_ma, ss.df_metri_ma = obj

#--------------------------------------
# (2) advanced pre-processing (above Baseline)
ss.time_range_basli = 52*5
ss.quantile_val = 0.65
ss.time_range_trace = 24
ss.time_range_stats = 6

# compute 
obj = compute_recent_level(df_data, ss.time_range_basli, ss.quantile_val, ss.time_range_trace, ss.time_range_stats, ss.ts_today)
# unwrap
ss.df_trace_bl, ss.trace_x_range_bl, ss.df_metri_bl, ss.stats_x_range_bl = obj






# update data dependent objects
ss.df_data = df_data
ss.df_latest_data = get_latest_date_per_group(df_data, ts_today = ss.ts_today)
ss.ts_latest_data = df_data['ISO_WEEKSTARTDATE'].max()
ss.date_range_dt = [df_data["ISO_WEEKSTARTDATE"].min().date(), df_data["ISO_WEEKSTARTDATE"].max().date()]

# get top 3 weeks and delay to today 
ss.top3_weeks =  df_data["ISO_WEEKSTARTDATE"].drop_duplicates().sort_values(ascending=False).head(3)
ss.delays_days = ((ss.ts_today - ss.top3_weeks).dt.days).tolist()


# initialize session state (constant values)
ss.setdefault("MAX_COUNTRIES_IN_PLOTS", 20)

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
p00 = st.Page("pages/st_page_00.py", title="💡 By Regions")
p02 = st.Page("pages/st_page_02.py", title="🔎 Wave Onset")
p03 = st.Page("pages/st_page_03.py", title="🔎 Type A vs B")
p04 = st.Page("pages/st_page_04.py", title="🔎 Explore")
p05 = st.Page("pages/st_page_05.py", title="🔥 Top Risers")
# p06 = st.Page("pages/st_page_06.py", title="💡 Positivity by Regions") # not show yet, under developments
p07 = st.Page("pages/st_page_07.py", title="🔬 Tabular")
p08 = st.Page("pages/st_page_08.py", title="🔬 Data age")
p09 = st.Page("pages/st_page_09.py", title="⚙️ Settings")
p10 = st.Page("pages/st_page_10.py", title="💡 All Risers")
p11 = st.Page("pages/st_page_11.py", title="🔥 Top High")
p12 = st.Page("pages/st_page_12.py", title="📋 Info")
p13 = st.Page("pages/st_page_13.py", title="💡 All High")

p_dev = st.Page("pages/st_dev.py", title="💀 Dev")

pg = st.navigation([p05, p11, p10, p13, p00, p02, p03, p04, p07, p08, p09, p12, p_dev], position="top")
pg.run()















