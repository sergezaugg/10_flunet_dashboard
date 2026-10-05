#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

import numpy as np
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import streamlit as st
from src.utils import polyreg_by_country_source, filter_a_country, get_baseline_count, filter_a_data_source
from src.utils import det_regions, get_start_stop_of_region, keep_n_most_recent_weeks
from src.utils_plots import make_smoothed_curve_plot

quantile_val = 0.66
ma_bin_size = 5
ma_degree   = 1

# load data to local page 
df = ss.df_data.copy()

# keep last 5 years to compute baseline 
week_limit = df['ISO_WEEKSTARTDATE'].max() - pd.Timedelta(weeks=52*5)
df = df[df["ISO_WEEKSTARTDATE"] > week_limit]

# get baseline of flu counts (for all countries)
bthld = get_baseline_count(df, q = quantile_val)


# reduce to fewer recent weeks for dashboard 
df00 = keep_n_most_recent_weeks(df, keep_n_weeks = 15)


# merge-in baseline 
dfb = df00.merge(bthld, on=["COUNTRY", "ORIGIN_SOURCE"], how="left")
# remove "COUNTRY", "ORIGIN_SOURCE" that are all-na for "INF_ALL"
dfb = dfb[dfb.groupby(["COUNTRY", "ORIGIN_SOURCE"])["INF_ALL"].transform("count").gt(0)]
# keep only "COUNTRY" by "ORIGIN_SOURCE" where baseline reasonably high (i.e. far enough from 0)
dfb = dfb[dfb['INF_ALL_BASELINE'] >= 5]

# count number above thld 
abv_bl_counts = (
        dfb.assign(ABOVE_BASELINE=dfb["INF_ALL"] >= dfb["INF_ALL_BASELINE"])
        .groupby(["COUNTRY", "ORIGIN_SOURCE"], as_index=False)
        .agg(N_ABOVE_BASELINE=("ABOVE_BASELINE", "sum"), 
             INF_ALL_BASELINE=("INF_ALL_BASELINE", "first"),
             ISO_WEEKSTARTDATE=("ISO_WEEKSTARTDATE", "max"),
             )
    )
 
abv_bl_counts = abv_bl_counts[abv_bl_counts['N_ABOVE_BASELINE'] > 1]
abv_bl_counts = abv_bl_counts.sort_values("N_ABOVE_BASELINE", ascending = False)
# abv_bl_counts.head()



df_dat01 = abv_bl_counts[abv_bl_counts['ORIGIN_SOURCE'] == "SENTINEL"]
df_dat02 = abv_bl_counts[abv_bl_counts['ORIGIN_SOURCE'] == "NONSENTINEL"]
df_dat03 = abv_bl_counts[abv_bl_counts['ORIGIN_SOURCE'] == "NOTDEFINED"]

df01 = filter_a_data_source(df00, "SENTINEL")
df02 = filter_a_data_source(df00, "NONSENTINEL")
df03 = filter_a_data_source(df00, "NOTDEFINED")




@st.cache_data
def make_metric_items_baseline(row, height_row):
    with st.container(border= True, height = height_row):
        st.metric(label=row['COUNTRY'], 
            value=f"{int(row['N_ABOVE_BASELINE'])} Weeks",
            border  = False, 
            width = 200, height = int(0.60*height_row))
        st.markdown(
            f'<span style="font-size: 12px;">Updated {row["ISO_WEEKSTARTDATE"].strftime("%Y-%m-%d")}</span>',
            unsafe_allow_html=True,)

@st.cache_data
def make_mini_trace_baseline(row, height_row, df_for_trace):
     with st.container(border= True, height = height_row):
        df_subset = df_for_trace[df_for_trace["COUNTRY"] == row['COUNTRY']]
        fig = px.line(df_subset, x = 'ISO_WEEKSTARTDATE', y = 'INF_ALL', height = int(0.8*height_row), markers = True)
        fig.update_layout(margin=dict(l=10, r=15, t=10, b=10), xaxis_title=None, yaxis_title=None)
        fig.update_xaxes(showline = True, linewidth=0.8, mirror=True, )
        fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
        fig.add_hline(y=row['INF_ALL_BASELINE'], line_width=1, line_dash="dash", line_color="green")
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

for i, row in df_dat01.iterrows():
    with c1:
        make_metric_items_baseline(row, height_row = rowheight)
    with c2:
        make_mini_trace_baseline(row, height_row = rowheight, df_for_trace = df01)

for i, row in df_dat02.iterrows():
    with c3:
        make_metric_items_baseline(row, height_row = rowheight)
    with c4:
        make_mini_trace_baseline(row, height_row = rowheight, df_for_trace = df02)

for i, row in df_dat03.iterrows():
    with c5:
        make_metric_items_baseline(row, height_row = rowheight)
    with c6:
        make_mini_trace_baseline(row, height_row = rowheight, df_for_trace = df03)        