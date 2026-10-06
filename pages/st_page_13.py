#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

from streamlit import session_state as ss
import plotly.express as px
import pandas as pd
import streamlit as st
from src.utils import prepre_for_pages_10_13, make_bar_plot_pages_10_13

df_dat00 = ss.df_metri_bl[ss.df_metri_bl["ORIGIN_SOURCE"] == "SENTINEL"]
df_dat01 = ss.df_metri_bl[ss.df_metri_bl["ORIGIN_SOURCE"] == "NONSENTINEL"]
df_dat02 = ss.df_metri_bl[ss.df_metri_bl["ORIGIN_SOURCE"] == "NOTDEFINED"]

df_dat00 = prepre_for_pages_10_13(df_dat00, xvar = "N_ABOVE_BASELINE")
df_dat01 = prepre_for_pages_10_13(df_dat01, xvar = "N_ABOVE_BASELINE")
df_dat02 = prepre_for_pages_10_13(df_dat02, xvar = "N_ABOVE_BASELINE")

# quick fix
df_dat00 = df_dat00[df_dat00["N_ABOVE_BASELINE"] > 0]
df_dat01 = df_dat01[df_dat01["N_ABOVE_BASELINE"] > 0]
df_dat02 = df_dat02[df_dat02["N_ABOVE_BASELINE"] > 0]

# df_dat00.shape
# df_dat01.shape
# df_dat02.shape

# plot 
for col, label in zip(st.columns(3), ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]):
    with col:
        st.text(label)

c1, c2, c3 = st.columns([50,50,50])

with c1:
    fig = make_bar_plot_pages_10_13(df_dat00, xvar = "N_ABOVE_BASELINE")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c2:
    fig = make_bar_plot_pages_10_13(df_dat01, xvar = "N_ABOVE_BASELINE")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c3:
    fig = make_bar_plot_pages_10_13(df_dat02, xvar = "N_ABOVE_BASELINE")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})







