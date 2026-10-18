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
    st.divider()
    st.markdown(f""":primary[Summary:] Identify countries with unusually high flu activity.
    Only :primary[top {int(ss.top_n)}] per data source is shown here.
    """)
    st.markdown(f""":primary[Methods:] Historical baseline threshold (green line) computed per-county and source.
    Traces show latest {int(ss.time_range_trace)} weeks.
    Nb weeks above threshold derived from latest {int(ss.time_range_stats)} weeks.
    See **Methods** page for details.
    """)

# apply user's choice 
df_metri_bl = ss.df_metri_merged[ss.df_metri_merged["ISO_WEEKSTARTDATE"] >= sel_date]

# quick fix - supress stats if N was too small
df_metri_bl.loc[df_metri_bl["N_VALID"] < 3, "REL_BURDEN"] = pd.NA

# make traces list
df_trace = [filter_a_data_source(ss.df_trace_bl, a)  for a in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]]
# select top N 
df_metri = [filter_a_data_source(df_metri_bl, a) for a in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]]
df_metri = [select_top_n_highest_slope(a, n=ss.top_n, sorting_var = 'REL_BURDEN') for a in df_metri]

# plot metrics and mini traces 
for col, label in zip(st.columns(3), ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]):
    with col:
        st.subheader(label)

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