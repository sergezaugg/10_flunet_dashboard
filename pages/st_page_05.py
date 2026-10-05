#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

from streamlit import session_state as ss
import plotly.express as px
import streamlit as st
from src.utils import polyreg_by_country_only, filter_a_data_source
from src.utils import keep_n_most_recent_weeks, select_top_n_highest_slope
from src.utils_plots import make_metric_items_slope, make_mini_trace_slope

# load data to local page 
df = ss.df_data.copy()

df00 = filter_a_data_source(df, "SENTINEL")
df00 = keep_n_most_recent_weeks(df00, keep_n_weeks = 15)
df00 = df00[['COUNTRY', 'ORIGIN_SOURCE', 'ISO_WEEKSTARTDATE', 'INF_ALL']]
df00 = polyreg_by_country_only(df00, bin_size = 4, deg = 1)

df01 = filter_a_data_source(df, "NONSENTINEL")
df01 = keep_n_most_recent_weeks(df01, keep_n_weeks = 15)
df01 = df01[['COUNTRY', 'ORIGIN_SOURCE', 'ISO_WEEKSTARTDATE', 'INF_ALL']]
df01 = polyreg_by_country_only(df01, bin_size = 4, deg = 1)

df02 = filter_a_data_source(df, "NOTDEFINED")
df02 = keep_n_most_recent_weeks(df02, keep_n_weeks = 15)
df02 = df02[['COUNTRY', 'ORIGIN_SOURCE', 'ISO_WEEKSTARTDATE', 'INF_ALL']]
df02 = polyreg_by_country_only(df02, bin_size = 4, deg = 1)

df_dat00 = ss.slope_dfs_by_source["SENTINEL"]
df_dat01 = ss.slope_dfs_by_source["NONSENTINEL"]
df_dat02 = ss.slope_dfs_by_source["NOTDEFINED"]

df_dat00 = select_top_n_highest_slope(df_dat00, n=10)
df_dat01 = select_top_n_highest_slope(df_dat01, n=10)
df_dat02 = select_top_n_highest_slope(df_dat02, n=10)

# plot metrics and mini traces 
c1, c2, c3, c4, c5, c6 = st.columns([50, 90, 50 , 90, 50, 90])
with c1:
    st.text("SENTINEL")
with c3:
    st.text("NONSENTINEL")
with c5:
    st.text("NOTDEFINED")

# plot metrics and mini traces 
c1, c2, c3, c4, c5, c6 = st.columns([50, 90, 50 , 90, 50, 90])

rowheight = 160
# nw_slo = 5
for i, row in df_dat00.iterrows():
    with c1:
        make_metric_items_slope(row, height_row = rowheight)
    with c2:
        make_mini_trace_slope(row, height_row = rowheight, df_for_trace = df00, n_slope = ss.nw_slo)

for i, row in df_dat01.iterrows():
    with c3:
        make_metric_items_slope(row, height_row = rowheight)
    with c4:
        make_mini_trace_slope(row, height_row = rowheight, df_for_trace = df01, n_slope = ss.nw_slo)  

for i, row in df_dat02.iterrows():
    with c5:
        make_metric_items_slope(row, height_row = rowheight)
    with c6:
        make_mini_trace_slope(row, height_row = rowheight, df_for_trace = df02, n_slope = ss.nw_slo)  
