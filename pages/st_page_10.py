#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

from streamlit import session_state as ss
import plotly.express as px
import pandas as pd
import streamlit as st
from src.utils import prepre_for_pages_10_13
from src.utils_plots import make_bar_plot_pages_10_13, make_geo_map

with st.sidebar:
    source_options = ["MAXCOMBINE", "SENTINEL", "NONSENTINEL", "NOTDEFINED", ]
    sel_source = st.selectbox("Choose a source:", options=source_options, placeholder="Type or select ...", key="k_p10_01")
    all_recent_dates = pd.Series(ss.df_metri_merged["ISO_WEEKSTARTDATE"].unique()).sort_values()
    sel_date = st.select_slider("Filter by recency", options=all_recent_dates, format_func=lambda x: x.strftime("%y-%m-%d"))

# prepare 
df_metri_ma = ss.df_metri_merged[ss.df_metri_merged["ISO_WEEKSTARTDATE"] >= sel_date]

# take max across 3 sources (resonable for this metric)
df_max = df_metri_ma.loc[df_metri_ma.dropna(subset=["PERC_CHANGE"]).groupby("COUNTRY")["PERC_CHANGE"].idxmax()]


df_dat00 = df_metri_ma[df_metri_ma["ORIGIN_SOURCE"] == "SENTINEL"]
df_dat01 = df_metri_ma[df_metri_ma["ORIGIN_SOURCE"] == "NONSENTINEL"]
df_dat02 = df_metri_ma[df_metri_ma["ORIGIN_SOURCE"] == "NOTDEFINED"]

df_dat00 = prepre_for_pages_10_13(df_dat00, xvar = "PERC_CHANGE")
df_dat01 = prepre_for_pages_10_13(df_dat01, xvar = "PERC_CHANGE")
df_dat02 = prepre_for_pages_10_13(df_dat02, xvar = "PERC_CHANGE")
df_max   = prepre_for_pages_10_13(df_max,   xvar = "PERC_CHANGE")

if sel_source == "SENTINEL":
    df_dat_map = df_dat00
if sel_source == "NONSENTINEL":
    df_dat_map = df_dat01
if sel_source == "NOTDEFINED":
    df_dat_map = df_dat02
if sel_source == "MAXCOMBINE":
    df_dat_map = df_max


fig = make_geo_map(df_dat_map, "PERC_CHANGE", "Viridis" ) # "Viridis"

c0, c1 = st.columns([2.5, 0.7])
# map 
with c0:
    with st.container(border=True, height = 500):
        st.plotly_chart(fig, use_container_width=True)

with c0:
    with st.container(border=True, height = 350):
        if df_dat_map.shape[0] > 0:
            fig = make_bar_plot_pages_10_13(df_dat_map, xvar = "PERC_CHANGE", xlabel = "New Cases Per Week", height = 300)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})








