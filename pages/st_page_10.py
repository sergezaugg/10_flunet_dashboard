#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

from streamlit import session_state as ss
import plotly.express as px
import pandas as pd
import streamlit as st
from src.utils import prepre_for_pages_10_13
from src.utils_plots import make_bar_plot_pages_10_13


all_recent_dates = pd.Series(ss.df_metri_ma["ISO_WEEKSTARTDATE"].unique()).sort_values()

with st.sidebar:
    sel_date = st.select_slider("Filter by recency", options=all_recent_dates, format_func=lambda x: x.strftime("%y-%m-%d"))

df_metri_ma = ss.df_metri_ma[ss.df_metri_ma["ISO_WEEKSTARTDATE"] >= sel_date]


df_dat00 = df_metri_ma[df_metri_ma["ORIGIN_SOURCE"] == "SENTINEL"]
df_dat01 = df_metri_ma[df_metri_ma["ORIGIN_SOURCE"] == "NONSENTINEL"]
df_dat02 = df_metri_ma[df_metri_ma["ORIGIN_SOURCE"] == "NOTDEFINED"]

df_dat00 = prepre_for_pages_10_13(df_dat00, xvar = "SLOPE")
df_dat01 = prepre_for_pages_10_13(df_dat01, xvar = "SLOPE")
df_dat02 = prepre_for_pages_10_13(df_dat02, xvar = "SLOPE")


# plot 
for col, label in zip(st.columns(3), ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]):
    with col:
        st.text(label)

c1, c2, c3 = st.columns([50,50,50])

with c1:
    fig = make_bar_plot_pages_10_13(df_dat00, xvar = "SLOPE", xlabel = "New Cases Per Week")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c2:
    fig = make_bar_plot_pages_10_13(df_dat01, xvar = "SLOPE", xlabel = "New Cases Per Week")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c3:
    fig = make_bar_plot_pages_10_13(df_dat02, xvar = "SLOPE", xlabel = "New Cases Per Week")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})







