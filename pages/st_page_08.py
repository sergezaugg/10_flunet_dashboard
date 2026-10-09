#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

import numpy as np 
from streamlit import session_state as ss
import streamlit as st
from src.utils_plots import display_df_page_08

# load data to local page 
df_lat = ss.df_latest_data.copy()

# build control items in sidebar
with st.sidebar:
    who_regions = st.multiselect("Select WHO regions", options = ss.WHOREGION_levels, key="k_rec_01")
   
#-------------------------------------------------------------
# data processing  

# select based on WHOREGION
df_lat = df_lat[df_lat["WHOREGION"].isin(who_regions)]
# set initial row order
df_lat = df_lat.sort_values("days_since", ascending = True)

# prepare overview 
df_lat["stale_data"] = np.where(df_lat["days_since"] > ss.nw_global*7, "Stale", "Fresh",)
table = (df_lat.groupby(["ORIGIN_SOURCE", "stale_data"]).size().reset_index(name="count"))
table = table.sort_values(['stale_data', 'ORIGIN_SOURCE'], ascending= [True, False])

# get overview counts
n_countries_all = df_lat.loc[ :,["COUNTRY"]].drop_duplicates().shape[0]
n_countries_remain = df_lat.loc[df_lat["stale_data"] == "Fresh"  , ["COUNTRY", "stale_data"]].drop_duplicates().shape[0]
n_countries_stale  = n_countries_all - n_countries_remain

# drop unused columns 
df_lat = df_lat.drop(columns = ["ISO_WEEKSTARTDATE", "WHOREGION", "FLUSEASON", "stale_data"])

# prepare 3 dfs in a list for display
df_sel = [df_lat[df_lat['ORIGIN_SOURCE'] == a] for a in ['SENTINEL', 'NONSENTINEL', 'NOTDEFINED']]
df_sel = [a.drop(columns = "ORIGIN_SOURCE") for a in df_sel]

#-------------------------------------------------------------
# display 

# quick overview of stale and fresh data 
c1, c2, c3 = st.columns([30,30,20])
with c1:
    with st.container(border= True, height = 280):

        x1, x2 = st.columns([30,30])
        with x1:
            st.text("Countries with >=1 series fresh")
            st.markdown(f"<p style='color:green; font-size:1.80rem; font-weight:600;'>N = {int(n_countries_remain)}</p>",
                unsafe_allow_html=True)
            
        with x2:
            st.text("Countries with all series stale")
            st.markdown(f"<p style='color:red; font-size:1.80rem; font-weight:600;'>N = {int(n_countries_stale)}</p>",
                unsafe_allow_html=True)

        st.text("Selected Regions: " + " · ".join(who_regions))

        st.markdown(f"""Data are considered stale if all series ('SENTINEL', 'NONSENTINEL', 'NOTDEFINED') are 
            older than {ss.nw_global*7} days and consequently data summaries are not shown on the other pages.""")
        
with c2:
    with st.container(border= True, height = 280):
        st.dataframe(table, hide_index  = True, 
                    #  height = 260, 
                     height="content",
            column_config={
                "ORIGIN_SOURCE": st.column_config.TextColumn("Data Source", width="auto", alignment="left",),
                "stale_data": st.column_config.TextColumn("Data Status", width="auto", alignment="center",),
                "count": st.column_config.NumberColumn("Nb Countries", width="auto", alignment="center",),
            },)

# display detes
c01, c02, = st.columns([60, 20])
with c01:
    with st.container(border= True, height = 500):
        c1, c2, c3 = st.columns([20,20,20])
        with c1:
            st.text('SENTINEL')
            display_df_page_08(df_sel[0], nw_cutoff = ss.nw_global*7, height = 400)
        
        with c2:
            st.text('NONSENTINEL')
            display_df_page_08(df_sel[1], nw_cutoff = ss.nw_global*7, height = 400)

        with c3:
            st.text('NOTDEFINED')
            display_df_page_08(df_sel[2], nw_cutoff = ss.nw_global*7, height = 400)
