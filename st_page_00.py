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

    with st.expander("WHO regions", expanded=False):
        who_regions = st.multiselect("WHO region", options = ss.WHOREGION_levels, key="k_who_01")

    print(type(who_regions))    

    with st.expander("Flu Season regions", expanded=False):
        fse_regions = st.multiselect("Flu Season region", options = ss.FLUSEASON_levels, key="k_who_02")

    with st.expander("Data quality filters", expanded=False):
        prop_na_tol = st.slider("Required proportion non-NAs", min_value=0.0, max_value=1.0,  step=0.05, format="%.2f", key="k_who_04") 
        mean_count_tol = st.slider("Required Average count", min_value=0, max_value=100, step=1, format="%d", key="k_who_05")  

    country_info = st.empty() 

# apply user's data filter to data 
ss.df_data_reg, n_countries = filter_data(df = ss.df_data, 
    prop_non_na_tol = prop_na_tol, mean_count_tol = mean_count_tol, 
    who_regions = who_regions, 
    fse_regions = fse_regions, 
    itz_regions = ss.ITZ_levels.to_numpy().tolist())

# plot if n countries not too large
if n_countries[0] > ss.MAX_COUNTRIES_IN_PLOTS:
    country_info.text(f"N Countries too large!  = {n_countries[0]}")
else:
    country_info.text(f"N Countries = {n_countries[0]}")
    # handle NAs before plot
    ss.df_data_reg.loc[ss.df_data_reg["INF_ALL"].isna(), "ISO_WEEKSTARTDATE"] = pd.NaT
    fig = make_facet_line_plot(df = ss.df_data_reg, n_countr = n_countries[0])
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})



