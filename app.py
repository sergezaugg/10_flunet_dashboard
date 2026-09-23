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
df_dat, df_meta = download_flunet_data()
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

# defaults for WHOREGION
ss.setdefault("k_who_01", ss.WHOREGION_levels.to_numpy().tolist())
ss.setdefault("k_who_02", ss.FLUSEASON_levels.to_numpy().tolist())
ss.setdefault("k_who_04", 0.80)
ss.setdefault("k_who_05", 30)

# defaults for ITZ
ss.setdefault("k_itz_03", ss.ITZ_levels.to_numpy().tolist())
ss.setdefault("k_itz_04", 0.80)
ss.setdefault("k_itz_05", 30)

# 2. ONE LOOP TO RULE THEM ALL: Protects every key from being deleted
for key in list(st.session_state.keys()):
    st.session_state[key] = st.session_state[key]

# build control items in sidebar
with st.sidebar:
    st.markdown(":primary[**Interactive Exploration of FluNet data**]") 
    st.info(ss.date_range)
    
# make navigation
p0 = st.Page("st_page_00.py", title="Flu Trend by Regions")
p1 = st.Page("st_page_01.py", title="Flu Trend by ITZ")
p2 = st.Page("st_page_02.py", title="Flu Wave Onset")

pg = st.navigation([p0, p1, p2], position="top")

pg.run()




















