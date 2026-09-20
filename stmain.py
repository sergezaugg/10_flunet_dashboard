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

# download and pre-process (do once)
df_dat, df_meta = download_flunet_data()
df_data = preprocess_flunet_data(df = df_dat)
df_data = include_rows_for_total_flunet_data(df = df_data)

# get global data dependent parameters  
min_date = df_data["ISO_WEEKSTARTDATE"].min().date()
max_date = df_data["ISO_WEEKSTARTDATE"].max().date()

# initialize ss 
if "date_range" not in ss:
    ss.date_range = (min_date, max_date)
if "df_data" not in ss:
    ss.df_data = df_data
if "n_countries" not in ss:
    ss.n_countries = 0


# build control items 
with st.sidebar:
    st.markdown(":primary[**Interactive Exploration of FluNet data**]") 
    date_range  = st.slider("Date range", min_value=min_date, max_value=max_date, value = ss.date_range, format="YYYY-MM-DD")     
    prop_na_tol = st.slider("Proportion NA tolerance", min_value=0.0, max_value=1.0, value=0.30, step=0.05, format="%.2f", 
                            help = "Max allowed proportion on NA week in a country") 
    mean_count_tol = st.slider("Average count tolerance", min_value=0, max_value=100, value=20, step=1, format="%d", 
                                help = "aaaaaaaaaaaaa")  
    country_info = st.empty() 
 
# apply user input to data 
df_data = filter_by_date_range(df = df_data, date_range = date_range)
df_data, n_countries = filter_data(df = df_data, prop_na_tol = prop_na_tol, mean_count_tol = mean_count_tol)
ss.df_data = df_data
ss.n_countries = n_countries

country_info.text(f"Countries N = {ss.n_countries[0]}")


# make navigation
p0 = st.Page("st_page_00.py", title="Count vs Time")
p1 = st.Page("st_page_01.py", title="tbd")
pg = st.navigation([p0, p1])
pg.run()




















