#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

import pandas as pd
import numpy as np 
from streamlit import session_state as ss
import streamlit as st
import plotly.express as px
from src.utils_plots import display_df_page_08

# load data to local page 
df_lat = ss.df_latest_data.copy()

with st.sidebar:
    st.markdown(f"""Data series are considered :primary[stale] if older than :primary[{ss.nw_global*7} days] and not shown on other pages.""")
    st.divider()

# build control items in sidebar
with st.sidebar:
    who_regions = st.multiselect("WHO region", options = ss.WHOREGION_levels, key="k_rec_01")
   








#-------------------------------------------------------------
# data processing  

# select based on WHOREGION
df_lat = df_lat[df_lat["WHOREGION"].isin(who_regions)]
# # drop unused columns 
# df_lat = df_lat.drop(columns = ["ISO_WEEKSTARTDATE", "WHOREGION", "FLUSEASON"])
# set initial row order
df_lat = df_lat.sort_values("days_since", ascending = True)

# prepare overview 
df_lat["stale_data"] = np.where(df_lat["days_since"] > ss.nw_global*7, "Stale", "Fresh",)
table = (df_lat.groupby(["ORIGIN_SOURCE", "stale_data"]).size().reset_index(name="count"))
table = table.sort_values(['stale_data', 'ORIGIN_SOURCE'], ascending= [True, False])

# drop unused columns 
df_lat = df_lat.drop(columns = ["ISO_WEEKSTARTDATE", "WHOREGION", "FLUSEASON", "stale_data"])

# prepare 3 dfs in a list for display
df_sel = [df_lat[df_lat['ORIGIN_SOURCE'] == a] for a in ['SENTINEL', 'NONSENTINEL', 'NOTDEFINED']]
df_sel = [a.drop(columns = "ORIGIN_SOURCE") for a in df_sel]


#-------------------------------------------------------------
# display 

# quick overview of stale and fresh data 
c1, c2, c3, c4 = st.columns([20,20,20,10])
with c1:
    st.dataframe(table, hide_index  = True,
        column_config={
            "ORIGIN_SOURCE": st.column_config.TextColumn("Data Source", width="small", alignment="center",),
            "stale_data": st.column_config.TextColumn("Data Status", width="small", alignment="center",),
            "count": st.column_config.NumberColumn("Nb Countries", width="small", alignment="center",),
        },)



# display data frames 
c1, c2, c3, c4 = st.columns([20,20,20,40])
with c1:
    st.text('SENTINEL')
    display_df_page_08(df_sel[0], nw_cutoff = ss.nw_global*7)
   
with c2:
    st.text('NONSENTINEL')
    display_df_page_08(df_sel[1], nw_cutoff = ss.nw_global*7)

with c3:
    st.text('NOTDEFINED')
    display_df_page_08(df_sel[2], nw_cutoff = ss.nw_global*7)









