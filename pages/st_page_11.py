#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

import numpy as np
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import streamlit as st
from src.utils import get_baseline_count, filter_a_data_source
from src.utils import select_top_n_highest_val_by_origin, keep_n_most_recent_weeks, keep_n_most_recent_weeks_2
from src.utils_plots import make_smoothed_curve_plot

quantile_val = 0.65
# define time ranges in weeks 
time_range_basli = 52*5
time_range_trace = 24
time_range_stats = 6

with st.sidebar:
    st.markdown(f""" BL from :primary[{quantile_val} quantile] taken over :primary[{int(time_range_basli)} weeks.]
    Traces show latest :primary[{int(time_range_trace)} weeks.]
    Stats from latest :primary[{int(time_range_stats)} weeks.]    
    """)
    

# load data to local page 
df = ss.df_data.copy()

# keep last 5 years to compute baseline 
df, _ = keep_n_most_recent_weeks_2(df, ref_date = ss.ts_today, keep_n_weeks = time_range_basli)
# get flu baseline counts (for all countries)
bl_thld = get_baseline_count(df, q = quantile_val)

# reduce to fewer recent weeks for trace plottins
df_tra, trace_x_range = keep_n_most_recent_weeks_2(df, ref_date = ss.ts_today, keep_n_weeks = time_range_trace)

# reduce even fewer recent weeks for recent stats (below)
df00, stats_x_range = keep_n_most_recent_weeks_2(df_tra, ref_date = ss.ts_today, keep_n_weeks = time_range_stats)

# merge-in baseline threshold 
df00 = df00.merge(bl_thld, on=["COUNTRY", "ORIGIN_SOURCE"], how="left")

df_bl = (df00
    # remove when all-na for "INF_ALL" 
    .loc[df00.groupby(["COUNTRY", "ORIGIN_SOURCE"])["INF_ALL"].transform("count").gt(0)]
    # keep only where baseline reasonably high (i.e. far enough from 0)
    .loc[lambda x: x["INF_ALL_BASELINE"] >= 5]
    # create boolean for 'above bl'
    .assign(ABOVE_BASELINE=lambda x: x["INF_ALL"] >= x["INF_ALL_BASELINE"])
    .groupby(["COUNTRY", "ORIGIN_SOURCE"], as_index=False) # extract summaries by group
    .agg(N_ABOVE_BASELINE=("ABOVE_BASELINE", "sum"),
        INF_ALL_BASELINE=("INF_ALL_BASELINE", "first"),
        ISO_WEEKSTARTDATE=("ISO_WEEKSTARTDATE", "max"),)
    .sort_values("N_ABOVE_BASELINE", ascending=False) # sort   
)

# select top 10 
df_bl = select_top_n_highest_val_by_origin(df_bl, n = 10, var ="N_ABOVE_BASELINE")

# organize by data source 
df_metri = [filter_a_data_source(df_bl, a) for a in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]]
df_trace = [filter_a_data_source(df_tra, a)  for a in ["SENTINEL", "NONSENTINEL", "NOTDEFINED"]]


@st.cache_data
def make_metric_items_baseline(row, height_row):
    with st.container(border= True, height = height_row):
        st.metric(label=row['COUNTRY'], 
            value=f"{int(row['N_ABOVE_BASELINE'])} weeks",
            border  = False, 
            delta_description = f"{int(row['N_ABOVE_BASELINE'])}/{time_range_stats} above BL",
            width = 200, height = int(0.60*height_row))
        st.markdown(
            f'<span style="font-size: 12px;">Updated {row["ISO_WEEKSTARTDATE"].strftime("%Y-%m-%d")}</span>',
            unsafe_allow_html=True,)

@st.cache_data
def make_mini_trace_baseline(row, height_row, df_for_trace):
     with st.container(border= True, height = height_row):
        df_subset = df_for_trace[df_for_trace["COUNTRY"] == row['COUNTRY']]
        fig = px.line(df_subset, x = 'ISO_WEEKSTARTDATE', y = 'INF_ALL', height = int(0.8*height_row), markers = True)
        fig.update_yaxes(range=[0, None])
        fig.update_xaxes(range=trace_x_range)
        fig.update_layout(margin=dict(l=10, r=15, t=10, b=10), xaxis_title=None, yaxis_title=None)
        fig.update_xaxes(showline = True, linewidth=0.8, mirror=True, )
        fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
        fig.add_hline(y=row['INF_ALL_BASELINE'], line_width=1, line_dash="dot", line_color="green")
        fig.add_hrect(y0=0.0, y1=row['INF_ALL_BASELINE'], fillcolor="pink", opacity=0.10, line_width=0, layer="below")
        fig.add_vline(x=stats_x_range[0], line_width=1, line_dash="dot", line_color="red")
        fig.add_vrect(x0=trace_x_range[0], x1=stats_x_range[0], fillcolor="pink", opacity=0.10, line_width=0, layer="below")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})



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

for i, row in df_metri[0].iterrows():
    with c1:
        make_metric_items_baseline(row, height_row = rowheight)
    with c2:
        make_mini_trace_baseline(row, height_row = rowheight, df_for_trace = df_trace[0])

for i, row in df_metri[1].iterrows():
    with c3:
        make_metric_items_baseline(row, height_row = rowheight)
    with c4:
        make_mini_trace_baseline(row, height_row = rowheight, df_for_trace = df_trace[1])

for i, row in df_metri[2].iterrows():
    with c5:
        make_metric_items_baseline(row, height_row = rowheight)
    with c6:
        make_mini_trace_baseline(row, height_row = rowheight, df_for_trace = df_trace[2])        