#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

from streamlit import session_state as ss
import plotly.express as px
import pandas as pd
import streamlit as st
from src.utils_pages import prepre_for_pages_10_13, rm_if_stat_na_per_source
from src.utils_plots import make_bar_plot_pages_10_13, make_geo_map

with st.sidebar:
    st.markdown(f""":primary[Summary:] Visualize the geographical distribution of flu trend.""")
    st.divider()
    all_recent_dates = pd.Series(ss.df_metri_merged["ISO_WEEKSTARTDATE"].unique()).sort_values()
    sel_date = st.select_slider("Filter by recency", options=all_recent_dates, format_func=lambda x: x.strftime("%y-%m-%d"), key = "k_p10_00")
    source_options = ["COMBINED", "SENTINEL", "NONSENTINEL", "NOTDEFINED", ]
    sel_source = st.radio("Data Source", options=source_options, index=0, key="k_p10_01")
    li_colormaps = ["Bluered", "Viridis", "Plasma", "Balance", "RdYlGn_r", "Reds"]
    sel_colormap = st.selectbox("Colormap", options = li_colormaps, index=0, key="k_p10_03", placeholder="select ...")


# prepare 
df_metri_ma = ss.df_metri_merged[ss.df_metri_merged["ISO_WEEKSTARTDATE"] >= sel_date]

# quick fix - supress stats if N was too small
df_metri_ma.loc[df_metri_ma["N_VALID"] < 3, "N_ABOVE_BASELINE"] = pd.NA

df_dat00 = df_metri_ma[df_metri_ma["ORIGIN_SOURCE"] == "SENTINEL"]
df_dat01 = df_metri_ma[df_metri_ma["ORIGIN_SOURCE"] == "NONSENTINEL"]
df_dat02 = df_metri_ma[df_metri_ma["ORIGIN_SOURCE"] == "NOTDEFINED"]
df_dat03 = df_metri_ma[df_metri_ma["perc_change_is_max"] == True]

# filter only data with a actual stats value 
df_dat00, df_dat01, df_dat02, df_dat03, dat_info = rm_if_stat_na_per_source(df_dat00, df_dat01, df_dat02, df_dat03, "PERC_CHANGE")

df_dat00 = prepre_for_pages_10_13(df_dat00, xvar = "PERC_CHANGE")
df_dat01 = prepre_for_pages_10_13(df_dat01, xvar = "PERC_CHANGE")
df_dat02 = prepre_for_pages_10_13(df_dat02, xvar = "PERC_CHANGE")
df_dat03 = prepre_for_pages_10_13(df_dat03, xvar = "PERC_CHANGE")

if sel_source == "SENTINEL":
    df_dat_map = df_dat00
if sel_source == "NONSENTINEL":
    df_dat_map = df_dat01
if sel_source == "NOTDEFINED":
    df_dat_map = df_dat02
if sel_source == "COMBINED":
    df_dat_map = df_dat03


fig_geo = make_geo_map(df_dat_map, "PERC_CHANGE", sel_colormap, height = 370, range_color = [-55,55], legend_title = "Percent change from BL" ) 
if df_dat_map.shape[0] > 0:
    fig_bar = make_bar_plot_pages_10_13(df_dat_map, xvar = "PERC_CHANGE", xlabel = "Percent change from BL", height = 300, 
        colormap = sel_colormap, range_color = [-55,55])
            
c0, c1 = st.columns([30, 8])
with c0:
    with st.container(border=True, height = 400):
        st.plotly_chart(fig_geo, use_container_width=True)
with c0:
    with st.container(border=True, height = 350):
        if df_dat_map.shape[0] > 0:
            st.plotly_chart(fig_bar)
with c1:
    with st.container(border=True, height = 750 + 15):
        # st.text("Data prep summary" )
        st.markdown(f""":primary[Data Preparation Summary]""")
        st.dataframe(dat_info, hide_index=True)
        st.caption("Fresh: At least 1 value in recent range" )
        st.caption("Analysable: Enough recent data for slope")
    






