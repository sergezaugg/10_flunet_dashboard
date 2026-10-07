#--------------------             
# Author : Serge Zaugg
# Description : classic time traces 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from src.utils import filter_data_region, filter_several_countries
from src.utils_plots import make_facet_line_plot

# filter by region
with st.sidebar:
    fse_regions = st.multiselect("Pre-select Flu Region", options = ss.FLUSEASON_levels, key="k_who_02")
    who_regions = st.multiselect("Pre-select WHO region", options = ss.WHOREGION_levels, key="k_who_01")
    country_info_temp = st.empty() 
# apply user's data filter to data 
df_plot_temp, n_countries_temp = filter_data_region(df = ss.df_data, who_regions = who_regions, fse_regions = fse_regions, itz_regions = ss.ITZ_levels)
country_info_temp.text(f"N Countries = {n_countries_temp[0]}")

# filter by country  
all_countries = df_plot_temp['COUNTRY'].unique()
with st.sidebar:
    sel_countries = st.multiselect("Countries", options=sorted(all_countries), default=[], placeholder="Select countries", key="k_who_06")
    country_info = st.empty() 
# apply user's data filter to data 
df_plot, n_countries = filter_several_countries(df_plot_temp, sel_countries)





# plot if n countries not too large
if n_countries[0] > ss.MAX_COUNTRIES_IN_PLOTS:
    country_info.text(f"Too many countries: {n_countries[0]} \n Max allowed: {ss.MAX_COUNTRIES_IN_PLOTS}")
    st.stop()
country_info.text(f"N Countries = {n_countries[0]}")

# plot 
fig = make_facet_line_plot(df = df_plot, n_countr = n_countries[0], outcome = "INF_ALL")
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
