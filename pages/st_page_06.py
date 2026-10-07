#--------------------             
# Author : Serge Zaugg
# Description : classic time traces 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from src.utils import filter_data
from src.utils_plots import make_facet_line_plot

# build control items in sidebar
with st.sidebar:
    who_regions = st.multiselect("WHO region", options = ss.WHOREGION_levels, key="k_who_pos_01")
    fse_regions = st.multiselect("Flu Season region", options = ss.FLUSEASON_levels, key="k_who_pos_02")
    prop_na_tol = st.slider("Required proportion non-NAs", min_value=0.0, max_value=1.0,  step=0.05, format="%.2f", key="k_who_pos_04") 
    mean_count_tol = st.slider("Required Average count", min_value=0, max_value=100, step=1, format="%d", key="k_who_pos_05")  
    country_info = st.empty() 

# apply user's data filter to data 
df_plot, n_countries = filter_data(df = ss.df_data, 
    prop_non_na_tol = prop_na_tol, mean_count_tol = mean_count_tol, 
    who_regions = who_regions, 
    fse_regions = fse_regions, 
    itz_regions = ss.ITZ_levels)

# plot if n countries not too large
if n_countries[0] > ss.max_countries_in_plots:
    country_info.text(f"Too many countries: {n_countries[0]} \n Max allowed: {ss.max_countries_in_plots}")
    st.stop()
country_info.text(f"N Countries = {n_countries[0]}")

# plot 
fig = make_facet_line_plot(df = df_plot, n_countr = n_countries[0], outcome = "POSITIVITY")
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
