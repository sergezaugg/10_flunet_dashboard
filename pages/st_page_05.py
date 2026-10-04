#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

from streamlit import session_state as ss
import plotly.express as px
import streamlit as st
from src.utils import polyreg_by_country_only, filter_a_data_source
from src.utils import get_3_dfs_by_recency_for_top_n_slope, keep_n_most_recent_weeks
from src.utils_plots import make_metric_items, make_mini_trace

with st.sidebar:
    sel_data_source = st.radio(label = "Data Source", options = ["SENTINEL", "NONSENTINEL", "NOTDEFINED"], index=0)
st.text(sel_data_source)

# load data to local page 
df = ss.df_data.copy()
# df = df[df["ORIGIN_SOURCE"] == "NOTDEFINED"]
df = filter_a_data_source(df, sel_data_source)
df = keep_n_most_recent_weeks(df, keep_n_weeks = 15)
df = polyreg_by_country_only(df, bin_size = 4, deg = 1)
nw_slo = 5
# df_dat00, df_dat01, df_dat02, df_slopes_all = get_3_dfs_by_recency_for_top_n_slope(df, ss.latest_week, slope_thld = 0.1, n_weeks_for_slope = nw_slo)

df_dat00, df_dat01, df_dat02, df_slopes_all = ss.slope_dfs_by_source[sel_data_source]

# plot delay / recency information
c1, c2, x1, c3, c4, x2, c5, c6, x3 = st.columns([50, 80, 8, 50, 80, 8, 50, 80, 8])
with st.container():
    with c1:
        st.markdown(f'<span style="color:{ss.colors_recency[0]}"><b>{ss.delays_days[0]} days old</b></span>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<span style="color:{ss.colors_recency[1]}"><b>{ss.delays_days[1]} days old</b></span>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<span style="color:{ss.colors_recency[2]}"><b>{ss.delays_days[2]} days old</b></span>', unsafe_allow_html=True)
    
# plot metrics and mini traces 
c1, c2, x1, c3, c4, x2, c5, c6, x3 = st.columns([50, 80, 8, 50 , 80, 8, 50, 80, 8])

for i, row in df_dat00.iterrows():
    with c1:
        make_metric_items(row, height_row = 150)
    with c2:
        make_mini_trace(row, height_row = 150, df_for_trace = df, n_slope = nw_slo)

for i, row in df_dat01.iterrows():
    with c3:
        make_metric_items(row, height_row = 150)
    with c4:
        make_mini_trace(row, height_row = 150, df_for_trace = df, n_slope = nw_slo)

for i, row in df_dat02.iterrows():
    with c5:
        make_metric_items(row, height_row = 150)
    with c6:
        make_mini_trace(row, height_row = 150, df_for_trace = df, n_slope = nw_slo)


