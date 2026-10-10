#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

import numpy as np
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import streamlit as st
from src.utils import filter_a_country

indx = int(np.where(ss.ALL_COUNTRIES == "CHE")[0][0])

# build control items in sidebar
with st.sidebar:
    selected_country = st.selectbox("Choose a country:", options=ss.ALL_COUNTRIES, placeholder="Type or select a country...", index=indx, key="xxxxx")
    sel_data_source = st.radio(label = "Data Source", options = ["SENTINEL", "NONSENTINEL", "NOTDEFINED"], index=0)
    st.divider()
    st.markdown(f""":primary[Summary:] Inspect the data used in this app.""")

# load data to local page 
df = ss.df_data.copy()
df = df[df["ORIGIN_SOURCE"] == sel_data_source]
df_display = filter_a_country(df, selected_country)


c1, c2 = st.columns([30, 1])
with c1:
    st.text(" ")
    st.dataframe(df_display, height = 600, hide_index=True)





