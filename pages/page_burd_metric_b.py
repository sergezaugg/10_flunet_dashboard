#--------------------             
# Author : Serge Zaugg
# Description : flu burden from past few weeks 
#--------------------

import numpy as np
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import streamlit as st
from src.utils import filter_a_data_source
from src.utils import select_top_n_highest_slope
from src.utils_plots import make_metric_items_baseline, make_mini_trace_baseline

with st.sidebar:
    all_recent_dates = pd.Series(ss.df_metri_merged["ISO_WEEKSTARTDATE"].unique()).sort_values()
    sel_date = st.select_slider("Filter by recency", options=all_recent_dates, format_func=lambda x: x.strftime("%y-%m-%d"), key = "k_burd_recency")
    sel_data_source = st.radio(label = "Data Source", options = ["SENTINEL", "NONSENTINEL", "NOTDEFINED"], index=0, key="k_ab_02")
    st.divider()

# apply user's choice 
df_metri_bl = ss.df_metri_merged[ss.df_metri_merged["ISO_WEEKSTARTDATE"] >= sel_date]
df_metri = filter_a_data_source(df_metri_bl, sel_data_source) 
df_trace = filter_a_data_source(ss.df_trace_bl, sel_data_source)  

# quick fix - supress stats if N was too small
df_metri.loc[df_metri["N_VALID"] < 3, "REL_BURDEN"] = pd.NA

df_metri = select_top_n_highest_slope(df_metri, n=200000, sorting_var = 'REL_BURDEN') 

with st.sidebar:
    st.write("N countries", df_metri.shape[0])

rowheight = 160

# smart way to fill in by rows (using st columns )
c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([50, 90, 50 , 90, 50, 90, 50, 90])
col_pairs = [(c1, c2), (c3, c4), (c5, c6), (c7, c8)]
for i, row in df_metri.iterrows():
    c_metric, c_plot = col_pairs[i % 4]
    with c_metric:
        make_metric_items_baseline(row, rowheight, ss.time_range_stats)
    with c_plot:
        make_mini_trace_baseline(row, rowheight, df_trace, ss.trace_x_range_bl, ss.stats_x_range_bl) 

