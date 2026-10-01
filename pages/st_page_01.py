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
    col1, col2 = st.columns(2)
    itz_regions_a = col1.pills("Africa", options = ss.ITZ_levels_AFR, selection_mode="multi", width = 100, wrap = True, key="k_itz_03a")
    itz_regions_b = col2.pills("America", options = ss.ITZ_levels_AMC, selection_mode="multi", width = 100, wrap = True, key="k_itz_03b")
    col1, col2 = st.columns(2)
    itz_regions_c = col1.pills("Asia", options = ss.ITZ_levels_ASI, selection_mode="multi", width = 100, wrap = True, key="k_itz_03c")
    itz_regions_d = col2.pills("Europe", options = ss.ITZ_levels_EUR, selection_mode="multi", width = 100, wrap = True, key="k_itz_03d")
    col1, col2 = st.columns(2)
    itz_regions_e = col1.pills("Oceania", options = ss.ITZ_levels_OCE, selection_mode="multi", width = 100, wrap = True, key="k_itz_03e")
    itz_regions = itz_regions_a + itz_regions_b + itz_regions_c + itz_regions_d + itz_regions_e
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
    country_info.text(f"Too many countries: {n_countries[0]} \n Max allowed: {ss.MAX_COUNTRIES_IN_PLOTS}")
    st.stop()
country_info.text(f"N Countries = {n_countries[0]}")

# plot 
fig = make_facet_line_plot(df = df_plot, n_countr = n_countries[0], outcome = "INF_ALL")
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
