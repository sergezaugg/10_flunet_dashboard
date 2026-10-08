#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

import numpy as np
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import streamlit as st
from src.utils import filter_a_data_source
from src.utils import select_top_n_highest_val_by_origin
from src.utils_plots import make_metric_items_baseline, make_mini_trace_baseline

with st.sidebar:
    st.markdown(f""" BL from :primary[{ss.quantile_val} quantile] taken over :primary[{int(ss.time_range_basli)} weeks.]
    Traces show latest :primary[{int(ss.time_range_trace)} weeks.]
    Stats from latest :primary[{int(ss.time_range_stats)} weeks.]    
    """)

# select top 10 
df_metri = select_top_n_highest_val_by_origin(ss.df_metri_merged, n = 10, var ="N_ABOVE_BASELINE")
# organize by data source 
df_metri = [filter_a_data_source(df_metri, a) for a in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]]
df_trace = [filter_a_data_source(ss.df_trace_bl, a)  for a in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]]

# plot metrics and mini traces 
for col, label in zip(st.columns(3), ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]):
    with col:
        st.text(label)

c1, c2, c3, c4, c5, c6 = st.columns([50, 90, 50 , 90, 50, 90])

rowheight = 160


for i, row in df_metri[0].iterrows():
    with c1:
        make_metric_items_baseline(row, rowheight, ss.time_range_stats)
    with c2:
        make_mini_trace_baseline(row, rowheight, df_trace[0], ss.trace_x_range_bl, ss.stats_x_range_bl)

for i, row in df_metri[1].iterrows():
    with c3:
        make_metric_items_baseline(row, rowheight, ss.time_range_stats)
    with c4:
        make_mini_trace_baseline(row, rowheight, df_trace[1], ss.trace_x_range_bl, ss.stats_x_range_bl)

for i, row in df_metri[2].iterrows():
    with c5:
        make_metric_items_baseline(row, rowheight, ss.time_range_stats)
    with c6:
        make_mini_trace_baseline(row, rowheight, df_trace[2], ss.trace_x_range_bl, ss.stats_x_range_bl)        