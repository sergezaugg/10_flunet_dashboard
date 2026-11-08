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
    who_regions = st.multiselect("Select WHO regions", options = ss.WHOREGION_levels, default = ss.WHOREGION_levels.tolist(), key="k_rec_01")

#-------------------------------------------------------------
# data processing  

# select based on WHOREGION
df_lat = df_lat[df_lat["WHOREGION"].isin(who_regions)]
# set initial row order
df_lat = df_lat.sort_values("days_since", ascending = True)

# # prepare overview 
df_lat["stale_data"] = np.where(df_lat["days_since"] > ss.nw_global*7, "Stale", "Fresh",)

# get overview counts
n_countries_all = df_lat.loc[ :,["COUNTRY"]].drop_duplicates().shape[0]
n_countries_remain = df_lat.loc[df_lat["stale_data"] == "Fresh"  , ["COUNTRY", "stale_data"]].drop_duplicates().shape[0]
n_countries_stale  = n_countries_all - n_countries_remain

# drop unused columns 
df_lat = df_lat.drop(columns = ["ISO_WEEKSTARTDATE", "WHOREGION", "FLUSEASON", "stale_data"])

# prepare 3 dfs in a list for display
df_sel = [df_lat[df_lat['ORIGIN_SOURCE'] == a] for a in ['SENTINEL', 'NONSENTINEL', 'NOTDEFINED']]
df_sel = [a.drop(columns = "ORIGIN_SOURCE") for a in df_sel]

#----------------------------------------------
# create map of data age 

dft = ss.df_latest_data
# select based on WHOREGION
dft = dft[dft["WHOREGION"].isin(who_regions)]
# get series with most recent data (with min of days_since)
df_min = dft.loc[dft.dropna(subset=["days_since"]).groupby("COUNTRY")["days_since"].idxmin()]
# make plot 
fig = make_geo_map(df_min, "days_since", "Bluered", height = 370, range_color = [0, 20+ss.nw_global*7],
    proj = None, 
    legend_title = "Data age [Days]",
    col_bar_horiz = False
    )

#-------------------------------------------------------------
# display 

# create layout 
c11, c12 = st.columns([30,15])

# quick overview of stale and fresh data 
with c11:
    with st.container(border= True, height = 250):

        x1, x2 = st.columns([1,1])
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
        
with c11:
    with st.container(border=True, height = 450):
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c12:
    with st.container(border=True, height = 250+450+16):
        t1, t2, t3 = st.tabs(["SENTINEL", "NONSENTINEL", "NOTDEFINED"], width="stretch", default="SENTINEL")
        with t1:
            display_df_page_08(df_sel[0], nw_cutoff = ss.nw_global*7, height = 600)
        with t2:
            display_df_page_08(df_sel[1], nw_cutoff = ss.nw_global*7, height = 600)
        with t3:
            display_df_page_08(df_sel[2], nw_cutoff = ss.nw_global*7, height = 600)


