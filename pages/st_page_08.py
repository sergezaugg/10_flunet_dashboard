#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

from streamlit import session_state as ss
import streamlit as st
import plotly.express as px
from src.utils_plots import display_df_page_08

# build control items in sidebar
with st.sidebar:
    who_regions = st.multiselect("WHO region", options = ss.WHOREGION_levels, key="k_rec_01")
   
# load data to local page 
df_lat = ss.df_latest_data.copy()

# select based on WHOREGION
df_lat = df_lat[df_lat["WHOREGION"].isin(who_regions)]
# drop unused columns 
df_lat = df_lat.drop(columns = ["ISO_WEEKSTARTDATE", "WHOREGION", "FLUSEASON"])
# set initial row order
df_lat = df_lat.sort_values("days_since", ascending = True)

# prepare 3 dfs in a list for display
df_sel = [df_lat[df_lat['ORIGIN_SOURCE'] == a] for a in ['SENTINEL', 'NONSENTINEL', 'NOTDEFINED']]
df_sel = [a.drop(columns = "ORIGIN_SOURCE") for a in df_sel]

# display data frames 
c1, c2, c3, c4 = st.columns([20,20,20,40])

with c1:
    st.text('SENTINEL')
    display_df_page_08(df_sel[0])
   
with c2:
    st.text('NONSENTINEL')
    display_df_page_08(df_sel[1])

with c3:
    st.text('NOTDEFINED')
    display_df_page_08(df_sel[2])









