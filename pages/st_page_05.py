#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

import numpy as np
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import streamlit as st
from src.utils import polyreg_by_country_only, select_top_n_highest_slope
from src.utils_plots import make_metric_items, make_mini_trace

# load data to local page 
df = ss.df_data.copy()

with st.sidebar:
    sel_data_source = st.radio(label = "Data Source", options = ["SENTINEL", "NONSENTINEL", "NOTDEFINED"], index=0)
st.text(sel_data_source)

# get top 3 weekks and delay to today 
top3_weeks =  df["ISO_WEEKSTARTDATE"].drop_duplicates().sort_values(ascending=False).head(3)
delays_days = ((ss.ts_today - top3_weeks).dt.days).tolist()
latest_week = df['ISO_WEEKSTARTDATE'].max()

df = df[df["ORIGIN_SOURCE"] == sel_data_source]
# df = df[df["ORIGIN_SOURCE"] == "NOTDEFINED"]


# keep only n most recent weeks 
s2 = df['ISO_WEEKSTARTDATE'].max() - pd.Timedelta(weeks=15)
df = df[df["ISO_WEEKSTARTDATE"] > s2]
df = df[['COUNTRY', 'ISO_WEEKSTARTDATE', 'INF_ALL']]

df = polyreg_by_country_only(df, bin_size = 3, deg = 1)

# take 5 most recent weeks per country  
week_0 = latest_week - pd.Timedelta(weeks=5)
df0 = df[df['ISO_WEEKSTARTDATE'] >= week_0]
# keep 3 most recent per country
df0 = df0.sort_values("ISO_WEEKSTARTDATE", ascending=False).groupby("COUNTRY").head(3) 
df0 = df0.sort_values(["COUNTRY", "ISO_WEEKSTARTDATE"], ascending=[True, False])

# compute simple slope from smoothed curve
param_dif = 2 # 3 will take 3 steps, i.e. change week-3 to week-0 
df0["SLOPE"] = (df0.groupby("COUNTRY")["INF_MA"].transform(lambda x: (x - x.shift(-param_dif)) ))

# keep only latest row per country
df1 = df0.sort_values("ISO_WEEKSTARTDATE", ascending=False).groupby("COUNTRY").head(1) 
df1 = df1.sort_values(["COUNTRY"], ascending=[True])

date_00 = latest_week - pd.Timedelta(weeks=0)
date_01 = latest_week - pd.Timedelta(weeks=1)
date_02 = latest_week - pd.Timedelta(weeks=2)

df_dat00 = df1[df1['ISO_WEEKSTARTDATE']==date_00] 
df_dat01 = df1[df1['ISO_WEEKSTARTDATE']==date_01] 
df_dat02 = df1[df1['ISO_WEEKSTARTDATE']==date_02] 

# df_dat00.shape
# df_dat01.shape
# df_dat02.shape

df_dat00 = select_top_n_highest_slope(df_dat00, n=10)
df_dat01 = select_top_n_highest_slope(df_dat01, n=10)
df_dat02 = select_top_n_highest_slope(df_dat02, n=10)

# colors_recency = ["#00ff55", "yellow", "orange", "red"]


# plot delay / recency information
c1, c2, x1, c3, c4, x2, c5, c6, x3 = st.columns([50, 80, 8, 50 , 80, 8, 50, 80, 8])
with st.container():
    with c1:
        st.markdown(f'<span style="color:{ss.colors_recency[0]}"><b>{delays_days[0]} days old</b></span>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<span style="color:{ss.colors_recency[1]}"><b>{delays_days[1]} days old</b></span>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<span style="color:{ss.colors_recency[2]}"><b>{delays_days[2]} days old</b></span>', unsafe_allow_html=True)
    
# plot metrics and mini traces 
c1, c2, x1, c3, c4, x2, c5, c6, x3 = st.columns([50, 80, 8, 50 , 80, 8, 50, 80, 8])

for i, row in df_dat00.iterrows():
    with c1:
        make_metric_items(row, height_row = 150)
    with c2:
        make_mini_trace(row, height_row = 150, df_for_trace = df)

for i, row in df_dat01.iterrows():
    with c3:
        make_metric_items(row, height_row = 150)
    with c4:
        make_mini_trace(row, height_row = 150, df_for_trace = df)

for i, row in df_dat02.iterrows():
    with c5:
        make_metric_items(row, height_row = 150)
    with c6:
        make_mini_trace(row, height_row = 150, df_for_trace = df)
