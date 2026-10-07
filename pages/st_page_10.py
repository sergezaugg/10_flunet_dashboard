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

# store max slope (per_source) to keep plot x axis stable
x_max = ss.df_metri_ma.groupby('ORIGIN_SOURCE')["SLOPE"].max()

with st.sidebar:
    source_options = ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]
    sel_source = st.selectbox("Choose a source:", options=source_options, placeholder="Type or select ...", key="k_p10_01")
    all_recent_dates = pd.Series(ss.df_metri_ma["ISO_WEEKSTARTDATE"].unique()).sort_values()
    sel_date = st.select_slider("Filter by recency", options=all_recent_dates, format_func=lambda x: x.strftime("%y-%m-%d"))

df_metri_ma = ss.df_metri_ma[ss.df_metri_ma["ISO_WEEKSTARTDATE"] >= sel_date]

df_dat00 = df_metri_ma[df_metri_ma["ORIGIN_SOURCE"] == "SENTINEL"]
df_dat01 = df_metri_ma[df_metri_ma["ORIGIN_SOURCE"] == "NONSENTINEL"]
df_dat02 = df_metri_ma[df_metri_ma["ORIGIN_SOURCE"] == "NOTDEFINED"]

df_dat00 = prepre_for_pages_10_13(df_dat00, xvar = "SLOPE")
df_dat01 = prepre_for_pages_10_13(df_dat01, xvar = "SLOPE")
df_dat02 = prepre_for_pages_10_13(df_dat02, xvar = "SLOPE")


if sel_source == "SENTINEL":
    df_dat_map = df_dat00
if sel_source == "NONSENTINEL":
    df_dat_map = df_dat01
if sel_source == "NOTDEFINED":
    df_dat_map = df_dat02



fig = make_geo_map(df_dat_map, "SLOPE", "Viridis")

c0, c1, c2 = st.columns([2.5, 1, 0.4])
# map 
with c0:
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)

with c1:
    if df_dat_map.shape[0] > 0:
        fig = make_bar_plot_pages_10_13(df_dat_map, xvar = "SLOPE", xlabel = "New Cases Per Week", x_max = x_max['SENTINEL'])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})








