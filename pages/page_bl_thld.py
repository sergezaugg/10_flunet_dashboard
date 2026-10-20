#--------------------             
# Author : Serge Zaugg
# Description : assess baseline values
#--------------------

import streamlit as st
from streamlit import session_state as ss
from src.utils import filter_a_data_source, filter_a_country
import plotly.express as px
from src.preprocessing import keep_n_most_recent_weeks_2
import numpy as np

# build control items in sidebar
indx = int(np.where(ss.ALL_COUNTRIES == "CHE")[0][0])
with st.sidebar:
    selected_country = st.selectbox("Choose a Country:", options=ss.ALL_COUNTRIES, placeholder="Type or select a country...", 
                                    index=indx, key="asdvadsasd")
    sel_data_source = st.radio(label = "Data Source", options = ["SENTINEL", "NONSENTINEL", "NOTDEFINED"], index=0, key="jfhgzehrnshdg ")

# get bl thlds
df02 = ss.df_data
df02 = filter_a_data_source(df02, sel_data_source)
df02 = filter_a_country(df02, selected_country)
df02, _ = keep_n_most_recent_weeks_2(df02, ref_date = ss.ts_today , keep_n_weeks = ss.time_range_basli)
df_plot = df02 

df01 = ss.df_metri_merged[[ 'COUNTRY', 'ORIGIN_SOURCE', 'INF_ALL_QUANT', 'INF_ALL_MAD', 'INF_ALL_BASELINE']]
df01 = filter_a_data_source(df01, sel_data_source)
df01 = filter_a_country(df01, selected_country)

st.write(df01)

if df_plot.shape[0] > 0:

    fig = px.line(
        df_plot,
        x="ISO_WEEKSTARTDATE",
        y="INF_ALL",
        height=400,
    )

    qua = df01['INF_ALL_QUANT'].item()
    mad = df01['INF_ALL_MAD'].item()
    hbt = df01['INF_ALL_BASELINE'].item()
    
    st.write("N years back:" , ss.time_range_basli/52)
    st.write("HBT: ", hbt)
    if not np.isnan(hbt):
        fig.add_hline(y=qua, line_width=3, line_dash="dash", line_color="blue")
        fig.add_hline(y=mad, line_width=3, line_dash="dot", line_color="green")
        fig.add_hline(y=hbt, line_width=3, line_dash="dot", line_color="red")


    fig.update_layout(margin=dict(l=40, r=40, t=20, b=20))
    fig.update_yaxes(range=[0, None])
    fig.update_xaxes(showline = True, linewidth=1.8, mirror=True, showticklabels=True, ticks="inside",)
    fig.update_yaxes(showline = True, linewidth=1.8, mirror=True)

    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

