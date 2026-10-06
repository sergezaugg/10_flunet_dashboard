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


df_dat00 = prepre_for_pages_10_13(ss.df_metri_ma["SENTINEL"],    xvar = "SLOPE")
df_dat01 = prepre_for_pages_10_13(ss.df_metri_ma["NONSENTINEL"], xvar = "SLOPE")
df_dat02 = prepre_for_pages_10_13(ss.df_metri_ma["NOTDEFINED"],  xvar = "SLOPE")








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







