#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

import numpy as np 
from streamlit import session_state as ss
import streamlit as st
from src.utils_plots import display_df_page_08, make_geo_map

# load data to local page 
df_lat = ss.df_latest_data.copy()

# build control items in sidebar
with st.sidebar:
    st.markdown(f""":primary[Summary: ] Assess data freshness by country relative to the reference date.""")
    st.divider()
    who_regions = st.multiselect("Select WHO regions", options = ss.WHOREGION_levels, key="k_rec_01")


#-------------------------------------------------------------
# data processing  

# select based on WHOREGION
df_lat = df_lat[df_lat["WHOREGION"].isin(who_regions)]
# set initial row order
df_lat = df_lat.sort_values("days_since", ascending = True)

# prepare overview 
df_lat["stale_data"] = np.where(df_lat["days_since"] > ss.nw_global*7, "Stale", "Fresh",)

# drop unused columns 
df_lat = df_lat.drop(columns = ["ISO_WEEKSTARTDATE", "WHOREGION", "FLUSEASON", "stale_data"])

# prepare 3 dfs in a list for display
df_sel = [df_lat[df_lat['ORIGIN_SOURCE'] == a] for a in ['SENTINEL', 'NONSENTINEL', 'NOTDEFINED']]
df_sel = [a.drop(columns = "ORIGIN_SOURCE") for a in df_sel]

#----------------------------------------------
# display detes
c1, c2, c3, _ = st.columns([20,20,20,10])
with c1:
    st.text('SENTINEL')
    display_df_page_08(df_sel[0], nw_cutoff = ss.nw_global*7, height = 600)
with c2:
    st.text('NONSENTINEL')
    display_df_page_08(df_sel[1], nw_cutoff = ss.nw_global*7, height = 600)
with c3:
    st.text('NOTDEFINED')
    display_df_page_08(df_sel[2], nw_cutoff = ss.nw_global*7, height = 600)
