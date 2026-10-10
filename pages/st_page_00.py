#--------------------             
# Author : Serge Zaugg
# Description : classic time traces 
#--------------------

import numpy as np
import streamlit as st
from streamlit import session_state as ss
from src.utils import filter_data_region, filter_several_countries
from src.utils_plots import make_facet_line_plot

# filter by region
with st.sidebar:
    # fse_regions = st.multiselect("Pre-select Flu Region", options = ss.FLUSEASON_levels, key="k_who_02")
    who_regions = st.multiselect("Pre-select WHO Regions", options = ss.WHOREGION_levels, key="k_who_01")
    country_info_temp = st.empty() 
# apply user's data filter to data 
df_plot_temp, n_countries_temp = filter_data_region(df = ss.df_data, who_regions = who_regions, 
                                                    fse_regions = ss.FLUSEASON_levels.tolist(), 
                                                    itz_regions = ss.ITZ_levels)
country_info_temp.text(f"N Countries = {n_countries_temp[0]}")

# filter by country  
all_countries = df_plot_temp['COUNTRY'].unique()
with st.sidebar:
    sel_countries = st.multiselect("Select Countries", options=sorted(all_countries), placeholder="Select countries", key="k_who_06")
    country_info = st.empty() 
# apply user's data filter to data 
df_plot, n_countries = filter_several_countries(df_plot_temp, sel_countries)

with st.sidebar:
    st.divider()
    outcome_var = st.radio(label = "Select Outcome Metric", options = ["INF_ALL", "POSITIVITY"], index=0)
# outcome_var = "INF_ALL"
# outcome_var = "POSITIVITY"

# exclude all from "ORIGIN_SOURCE" level if too few non-na
df_plot = df_plot.groupby("ORIGIN_SOURCE").filter(lambda g: g[outcome_var].notna().sum() >= 10)

if len(df_plot) <= 10:
    country_info.text(f"Please select at least one country")
    st.stop()

# plot if n countries not too large
if n_countries[0] > ss.max_countries_in_plots:
    country_info.text(f"Too many countries: {n_countries[0]} \n Max allowed: {ss.max_countries_in_plots}")
    st.stop()
country_info.text(f"N Countries = {n_countries[0]}")

# plot 
# fig = make_facet_line_plot(df = df_plot, n_countr = n_countries[0], outcome = "INF_ALL")
fig = make_facet_line_plot(df = df_plot, n_countr = n_countries[0], outcome = outcome_var)
c1,c2 = st.columns([30,1])
with c1:
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
