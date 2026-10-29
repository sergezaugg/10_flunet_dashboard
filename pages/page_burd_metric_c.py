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
from src.utils_plots import make_geo_map, make_per_source_strip_plot


with st.sidebar:
    st.markdown(f""":primary[Summary:] Her you can rank countries with highest flu burden first.""")
    st.divider()
    all_recent_dates = pd.Series(ss.df_metri_merged["ISO_WEEKSTARTDATE"].unique()).sort_values()
    sel_date = st.select_slider("Filter by recency", options=all_recent_dates, format_func=lambda x: x.strftime("%y-%m-%d"), key = "k_burd_recency")
    sel_data_source = st.radio(label = "Data Source", options = ["COMBINED", "SENTINEL", "NONSENTINEL", "NOTDEFINED"], index=0, key="k_abcvbfg_02")
    sel_top_n = st.select_slider("Top N", options=[10,20,30], value = 10, key = "k_burd_top_n")
    sel_thld = st.slider("Burden > t", min_value = 0.0, max_value = 10.0, value = 1.0, step = 0.1, key = "dfrqqsxcv")
    st.divider()

# apply user's choice 
df_metri_bl = ss.df_metri_merged[ss.df_metri_merged["ISO_WEEKSTARTDATE"] >= sel_date]


# spec for COMBINED
if sel_data_source == "COMBINED":
    df_metri = df_metri_bl[df_metri_bl["rel_burden_is_max"] == True]
    # get correct traces via the merge-mask trick
    df_mask = df_metri[['COUNTRY','ORIGIN_SOURCE']]
    df_trace = df_mask.merge(ss.df_trace_bl, on=['COUNTRY','ORIGIN_SOURCE'], how="left")
else :
    df_metri = filter_a_data_source(df_metri_bl, sel_data_source) 
    df_trace = filter_a_data_source(ss.df_trace_bl, sel_data_source)  

# st.write(df_metri)
# st.write(df_trace)

# quick fix - supress stats if N was too small
df_metri.loc[df_metri["N_VALID"] < 3, "REL_BURDEN"] = pd.NA
# keep only if > 1.0
df_metri =  df_metri[df_metri["REL_BURDEN"] > sel_thld]
# not needed here 
df_metri = select_top_n_highest_slope(df_metri, n=sel_top_n, sorting_var = 'REL_BURDEN') 

# with st.sidebar:
#     st.write("N countries", df_metri.shape[0])

rowheight = 160

# smart way to fill in by rows (using st columns )
c1, c2, c3, c4, c5 = st.columns([50, 90, 50 , 90, 250])
col_pairs = [(c1, c2), (c3, c4)]
for i, row in df_metri.iterrows():
    c_metric, c_plot = col_pairs[i % 2]
    with c_metric:
        make_metric_items_baseline(row, rowheight, ss.time_range_stats)
    with c_plot:
        make_mini_trace_baseline(row, rowheight, df_trace, ss.trace_x_range_bl, ss.stats_x_range_bl) 


#------------------
# make geo map 
# mollweide , orthographic , natural earth
fig_geo = make_geo_map(df_metri, "REL_BURDEN", "viridis", height = 300, range_color = [0.0, 2.0], 
    legend_title = "Relative Burden", 
    # proj = "orthographic", 
    proj = None , 
    col_bar_horiz = False) 

df_scat = ss.df_metri_merged
fig_strip = make_per_source_strip_plot(df = df_scat, yvar = "REL_BURDEN", height = 300, log_y=True, y_title = "Relative Burden")
fig_strip.add_hline(y=sel_thld, line_width=2, line_dash="dot", line_color="grey" )

with c5:
    with st.container(border=True, height = 380):
        st.text("Mini-map (only countries from selection are highlighted)")
        st.plotly_chart(fig_geo, use_container_width=True)

    with st.container(border=True, height = 380):
        st.text("Overview of countries where metrics could be computed")
        st.plotly_chart(fig_strip, use_container_width=False)





