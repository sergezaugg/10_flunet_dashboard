#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# run locally : streamlit run stmain.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
from utils import download_flunet_data, preprocess_flunet_data, include_rows_for_total_flunet_data

st.set_page_config(layout = "wide", initial_sidebar_state = "expanded")

# download and pre-process (do once)
df_dat, df_meta, download_ts = download_flunet_data()
df_data = preprocess_flunet_data(df = df_dat)
df_data = include_rows_for_total_flunet_data(df = df_data)

# get global data dependent parameters  
min_date         = df_data["ISO_WEEKSTARTDATE"].min().date().strftime("%Y-%m-%d")
max_date         = df_data["ISO_WEEKSTARTDATE"].max().date().strftime("%Y-%m-%d")
min_date_dt      = df_data["ISO_WEEKSTARTDATE"].min().date()
max_date_dt      = df_data["ISO_WEEKSTARTDATE"].max().date()

WHOREGION_levels = df_data["WHOREGION"].unique()
FLUSEASON_levels = df_data["FLUSEASON"].unique()
ITZ_levels       = df_data["ITZ"].unique()
MAX_COUNTRIES_IN_PLOTS = 30

# initialize session state
ss.setdefault("date_range", f"Data range: {min_date} to {max_date}")
ss.setdefault("date_range_dt", [min_date_dt, max_date_dt])
ss.setdefault("df_data", df_data)
ss.setdefault("df_data_reg", df_data.iloc[[0]])
ss.setdefault("df_data_itz", df_data.iloc[[0]])
ss.setdefault("WHOREGION_levels", WHOREGION_levels)
ss.setdefault("FLUSEASON_levels", FLUSEASON_levels)
ss.setdefault("ITZ_levels", ITZ_levels)
ss.setdefault("MAX_COUNTRIES_IN_PLOTS", MAX_COUNTRIES_IN_PLOTS)

# defaults for WHOREGION (page 00)
ss.setdefault("k_who_01", ss.WHOREGION_levels.to_numpy().tolist())
ss.setdefault("k_who_02", ss.FLUSEASON_levels.to_numpy().tolist())
ss.setdefault("k_who_04", 0.80)
ss.setdefault("k_who_05", 30)

# defaults for ITZ (page 01)
ss.setdefault("k_itz_03", ss.ITZ_levels.to_numpy().tolist())
ss.setdefault("k_itz_04", 0.80)
ss.setdefault("k_itz_05", 30)

# defaults for wave onset (page 02)
ss.setdefault("k_wave_01", 10)
ss.setdefault("k_wave_02", ss.date_range_dt)
ss.setdefault("k_wave_03", True)
ss.setdefault("k_wave_04", True)
ss.setdefault("k_wave_05", 125)



# Protects every key from being deleted
for key in list(st.session_state.keys()):
    st.session_state[key] = st.session_state[key]

# build control items in sidebar
with st.sidebar:
    st.markdown(":primary[**Interactive Exploration of FluNet data**]") 
    
# make navigation
p0 = st.Page("st_page_00.py", title="Flu Trend by Regions")
p1 = st.Page("st_page_01.py", title="Flu Trend by ITZ")
p2 = st.Page("st_page_02.py", title="Flu Wave Onset")
p3 = st.Page("st_page_03.py", title="Type A vs B")
pg = st.navigation([p0, p1, p2, p3], position="top")
pg.run()

# add info on sidebar
with st.sidebar:
    st.text("  ")
    st.text("Download on: " + str(download_ts))
    st.text(f"First data:  {(ss.date_range_dt[0])}")
    st.text(f"Latest data: {(ss.date_range_dt[1])}")














