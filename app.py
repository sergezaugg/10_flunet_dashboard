#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# run locally : streamlit run stmain.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
from utils import download_flunet_data, preprocess_flunet_data, include_rows_for_total_flunet_data
from utils import filter_data, filter_by_date_range
# import numpy as np
# import plotly.express as px

st.set_page_config(layout = "wide", initial_sidebar_state = "expanded")

MAX_COUNTRIES_IN_PLOTS = 30

# download and pre-process (do once)
df_dat, df_meta = download_flunet_data()
df_data = preprocess_flunet_data(df = df_dat)
df_data = include_rows_for_total_flunet_data(df = df_data)

# get global data dependent parameters  
min_date = df_data["ISO_WEEKSTARTDATE"].min().date().strftime("%Y-%m-%d")
max_date = df_data["ISO_WEEKSTARTDATE"].max().date().strftime("%Y-%m-%d")

WHOREGION_levels = df_data["WHOREGION"].unique()
FLUSEASON_levels = df_data["FLUSEASON"].unique()
ITZ_levels       = df_data["ITZ"].unique()




# initialize ss 
if "date_range" not in ss:
    ss.date_range = "Data range: " + min_date + " to " + max_date
if "df_data_plot" not in ss:
    ss.df_data_plot = df_data



# build control items 
with st.sidebar:
    st.markdown(":primary[**Interactive Exploration of FluNet data**]") 

    st.info(ss.date_range)

    with st.expander("WHO regions", expanded=False):
        who_regions = st.multiselect("WHO region", options = WHOREGION_levels, default = WHOREGION_levels)

    with st.expander("Flu Season regions", expanded=False):
        fse_regions = st.multiselect("Flu Season region", options = FLUSEASON_levels, default = FLUSEASON_levels)

    with st.expander("Influenza transmission zones", expanded=False):
        itz_regions = st.pills("ITZ region", options = ITZ_levels, selection_mode="multi", default = ITZ_levels)

    with st.expander("Data quality filters", expanded=False):
        prop_na_tol = st.slider("Required proportion non-NAs", min_value=0.0, max_value=1.0, value=0.80, step=0.05, format="%.2f") 
        mean_count_tol = st.slider("Required Average count", min_value=0, max_value=100, value=30, step=1, format="%d")  

    country_info = st.empty() 




# apply user input to data 
df_data_temp, n_countries = filter_data(df = df_data, 
    prop_non_na_tol = prop_na_tol, mean_count_tol = mean_count_tol, 
    who_regions = who_regions, fse_regions = fse_regions, itz_regions = itz_regions)

if n_countries[0] <= MAX_COUNTRIES_IN_PLOTS:
    ss.df_data_plot = df_data_temp.copy()
    country_info.text(f"Countries N = {n_countries[0]}")
else:
    country_info.text(f"Countries N too large  = {n_countries[0]}")







# make navigation
p0 = st.Page("st_page_00.py", title="Count vs Time")
p1 = st.Page("st_page_01.py", title="tbd")
pg = st.navigation([p0, p1])
pg.run()




















