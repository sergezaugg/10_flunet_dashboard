#--------------------             
# Author : Serge Zaugg
# Description : classic time traces 
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
import pandas as pd
from utils import filter_data
from utils_plots import make_facet_line_plot

# build control items in sidebar
with st.sidebar:
    itz_regions = st.pills("ITZ region", options = ss.ITZ_levels, selection_mode="multi", key="k_itz_03")
    prop_na_tol = st.slider("Required proportion non-NAs", min_value=0.0, max_value=1.0, step=0.05, format="%.2f", key="k_itz_04") 
    mean_count_tol = st.slider("Required Average count", min_value=0, max_value=100, step=1, format="%d", key="k_itz_05")  
    country_info = st.empty() 

# apply user's data filter to data 
df_plot, n_countries = filter_data(df = ss.df_data, 
    prop_non_na_tol = prop_na_tol, mean_count_tol = mean_count_tol, 
    who_regions = ss.WHOREGION_levels.to_numpy().tolist(), 
    fse_regions = ss.FLUSEASON_levels.to_numpy().tolist(), 
    itz_regions = itz_regions)

# plot if n countries not too large
if n_countries[0] > ss.MAX_COUNTRIES_IN_PLOTS:
    country_info.text(f"N Countries too large!  = {n_countries[0]}")
else:
    country_info.text(f"N Countries = {n_countries[0]}")
    # handle NAs before plot
    df_plot.loc[df_plot["INF_ALL"].isna(), "ISO_WEEKSTARTDATE"] = pd.NaT
    fig = make_facet_line_plot(df = df_plot, n_countr = n_countries[0])
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})



