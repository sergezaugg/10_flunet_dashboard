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
    sel_source = st.selectbox("Choose a source:", options=source_options, placeholder="Type or select ...", key="k_p13_01")
    all_recent_dates = pd.Series(ss.df_metri_merged["ISO_WEEKSTARTDATE"].unique()).sort_values()
    sel_date = st.select_slider("Filter by recency", options=all_recent_dates, format_func=lambda x: x.strftime("%y-%m-%d"))

# prepare 
df_metri_bl = ss.df_metri_merged[ss.df_metri_merged["ISO_WEEKSTARTDATE"] >= sel_date]

# take max across 3 sources (resonable for this metric)
df_max = df_metri_bl.loc[df_metri_bl.dropna(subset=["N_ABOVE_BASELINE"]).groupby("COUNTRY")["N_ABOVE_BASELINE"].idxmax()]

df_dat00 = df_metri_bl[df_metri_bl["ORIGIN_SOURCE"] == "SENTINEL"]
df_dat01 = df_metri_bl[df_metri_bl["ORIGIN_SOURCE"] == "NONSENTINEL"]
df_dat02 = df_metri_bl[df_metri_bl["ORIGIN_SOURCE"] == "NOTDEFINED"]

df_dat00 = prepre_for_pages_10_13(df_dat00, xvar = "N_ABOVE_BASELINE")
df_dat01 = prepre_for_pages_10_13(df_dat01, xvar = "N_ABOVE_BASELINE")
df_dat02 = prepre_for_pages_10_13(df_dat02, xvar = "N_ABOVE_BASELINE")
df_max   = prepre_for_pages_10_13(df_max,   xvar = "N_ABOVE_BASELINE")

if sel_source == "SENTINEL":
    df_dat_map = df_dat00
if sel_source == "NONSENTINEL":
    df_dat_map = df_dat01
if sel_source == "NOTDEFINED":
    df_dat_map = df_dat02
if sel_source == "MAXCOMBINE":
    df_dat_map = df_max



# quick fix
df_dat00_bar = df_dat_map[df_dat_map["N_ABOVE_BASELINE"] > 0]

#----------------------------------------------

fig = make_geo_map(df_dat_map, "N_ABOVE_BASELINE", "Viridis" ) # "Viridis"

c0, c1 = st.columns([2.5, 0.7])
# map 
with c0:
    with st.container(border=True, height = 500):
        st.plotly_chart(fig, use_container_width=True)
# barplots
with c0:
    with st.container(border=True, height = 350):
        if df_dat00_bar.shape[0] > 0:
            figbar = make_bar_plot_pages_10_13(df_dat00_bar, xvar = "N_ABOVE_BASELINE", xlabel = "Nb weeks above BL", height = 300)
            st.plotly_chart(figbar, use_container_width=True, config={"displayModeBar": False})








