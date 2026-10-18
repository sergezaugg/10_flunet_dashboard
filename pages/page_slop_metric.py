#--------------------             
# Author : Serge Zaugg
# Description : trend (slope) from past few weeks 
#--------------------

from streamlit import session_state as ss
import plotly.express as px
import streamlit as st
from src.utils import filter_a_data_source
from src.utils import select_top_n_highest_slope
from src.utils_plots import make_metric_items_slope, make_mini_trace_slope
import pandas as pd

with st.sidebar:
    all_recent_dates = pd.Series(ss.df_metri_merged["ISO_WEEKSTARTDATE"].unique()).sort_values()
    sel_date = st.select_slider("Filter by recency", options=all_recent_dates, format_func=lambda x: x.strftime("%y-%m-%d"), key = "k_slop_recency")
    st.divider()
    st.markdown(f""":primary[Summary:] Identify countries with the fastest-rising flu activity.
    Only :primary[top {int(ss.top_n)}] per data source are shown here.""")
    st.markdown(f""":primary[Methods:]
    Average change per week (slope) is estimated from latest {int(ss.nw_slo)} weeks via linear regression
    and normalized to percent change via historical baseline threshold (green line).
    See **Methods** page for details.
    """)

# apply user's choice 
df_metri_ma = ss.df_metri_merged[ss.df_metri_merged["ISO_WEEKSTARTDATE"] >= sel_date]

# quick fix - supress stats if N was too small
df_metri_ma.loc[df_metri_ma["N_VALID"] < 3, "N_ABOVE_BASELINE"] = pd.NA




# make traces list
df_trace = [filter_a_data_source(ss.df_trace_ma, a) for a in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]]
# for metrics boxes (unpack list and take top 10)
df_metri = [filter_a_data_source(df_metri_ma, a) for a in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]]
df_metri = [select_top_n_highest_slope(a, n=ss.top_n, sorting_var = 'PERC_CHANGE') for a in df_metri]
df_metri = [a.query("PERC_CHANGE > 0") for a in df_metri] # keep only positeve 'SLOPE' or "PERC_CHANGE"



# pre-render plotly (but it does not really speed rendering on screen  :-(  
rowheight = 160

@st.cache_data(show_spinner="Rendering mini-traces")
def pre_render_mintraces(df_tra, df_met):
    a = [make_mini_trace_slope(row, rowheight, df_tra[0], ss.trace_x_range_ma, ss.stats_x_range_ma) for _, row in df_met[0].iterrows()]
    b = [make_mini_trace_slope(row, rowheight, df_tra[1], ss.trace_x_range_ma, ss.stats_x_range_ma) for _, row in df_met[1].iterrows()]
    c = [make_mini_trace_slope(row, rowheight, df_tra[2], ss.trace_x_range_ma, ss.stats_x_range_ma) for _, row in df_met[2].iterrows()]
    return a, b, c

prerend1, prerend2, prerend3 = pre_render_mintraces(df_tra = df_trace, df_met = df_metri)

# plot metrics and mini traces 
for col, label in zip(st.columns(3), ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]):
    with col:
        st.subheader(label)

c1, c2, c3, c4, c5, c6 = st.columns([50, 90, 50 , 90, 50, 90])

for i, row in df_metri[0].iterrows():
    with c1:
        make_metric_items_slope(row, height_row = rowheight, show_percent = True)
    with c2:
        with st.container(border= True, height = rowheight):
            st.plotly_chart(prerend1[i], use_container_width=True, config={"displayModeBar": False})

for i, row in df_metri[1].iterrows():
    with c3:
        make_metric_items_slope(row, height_row = rowheight, show_percent = True)
    with c4:
        with st.container(border= True, height = rowheight):
            st.plotly_chart(prerend2[i], use_container_width=True, config={"displayModeBar": False})

for i, row in df_metri[2].iterrows():
    with c5:
        make_metric_items_slope(row, height_row = rowheight, show_percent = True)
    with c6:
        with st.container(border= True, height = rowheight):
            st.plotly_chart(prerend3[i], use_container_width=True, config={"displayModeBar": False})