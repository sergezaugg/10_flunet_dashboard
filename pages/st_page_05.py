#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

from streamlit import session_state as ss
import plotly.express as px
import streamlit as st
from src.utils import filter_a_data_source
from src.utils import select_top_n_highest_slope
from src.utils_plots import make_metric_items_slope, make_mini_trace_slope


trace_x_range = ss.trace_x_range_ma
# unpack smoothed traces dfs
df_trace = [filter_a_data_source(ss.df_trace_ma, a) for a in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]]
# for metrics boxes (unpack list and take top 10)
df_metri = [select_top_n_highest_slope(ss.df_metri_ma[a], n=10) for a in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]]



# plot metrics and mini traces 
for col, label in zip(st.columns(3), ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]):
    with col:
        st.text(label)

c1, c2, c3, c4, c5, c6 = st.columns([50, 90, 50 , 90, 50, 90])

rowheight = 160

for i, row in df_metri[0].iterrows():
    with c1:
        make_metric_items_slope(row, height_row = rowheight)
    with c2:
        make_mini_trace_slope(row, height_row = rowheight, df_for_trace = df_trace[0], n_slope = ss.nw_slo, xrange = trace_x_range)

for i, row in df_metri[1].iterrows():
    with c3:
        make_metric_items_slope(row, height_row = rowheight)
    with c4:
        make_mini_trace_slope(row, height_row = rowheight, df_for_trace = df_trace[1], n_slope = ss.nw_slo, xrange = trace_x_range)  

for i, row in df_metri[2].iterrows():
    with c5:
        make_metric_items_slope(row, height_row = rowheight)
    with c6:
        make_mini_trace_slope(row, height_row = rowheight, df_for_trace = df_trace[2], n_slope = ss.nw_slo, xrange = trace_x_range)  
