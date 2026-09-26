#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

import numpy as np
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import streamlit as st
from src.utils import ma_by_country, polyreg_by_country, filter_a_country


# load data to local page 
df = ss.df_sumall.copy()

all_countries = df['COUNTRY'].unique()
# Choose index of starting country
indx = int(np.where(all_countries == "Switzerland")[0][0])

# build control items in sidebar
with st.sidebar:
    selected_country = st.selectbox("Choose a country:", options=all_countries, placeholder="Type or select a country...", index=indx, key="k_wave_01")
    ma_bin_size = st.select_slider("Moving Avg N weeks", options=[1,3,5,7,9], value=3, key="k_ma_06")

# keep only n most recent weeks 
st.text(df.shape)
s2 = df['ISO_WEEKSTARTDATE'].max() - pd.Timedelta(weeks=53)
df = df[df["ISO_WEEKSTARTDATE"] > s2]
st.text(df.shape)

# apply moving average 
# df_ma = ma_by_country(df, bin_size = ma_bin_size)
df_ma = polyreg_by_country(df, bin_size = ma_bin_size)

df_plot = filter_a_country(df_ma, selected_country)

df_long = df_plot.melt(
    id_vars=[c for c in df.columns if c not in ["INF_ALL", "INF_MA"]],
    value_vars=["INF_ALL", "INF_MA"],
    var_name="TYPE",
    value_name="INF_VALUE"
)

fig = px.line(
    df_long,
    x="ISO_WEEKSTARTDATE",
    y="INF_VALUE",
    color="TYPE",
    facet_row="COUNTRY",
    height=300,
    markers=True,
    color_discrete_map={"INF_ALL": "#1f77b4",   "INF_MA": "#d62728",   "OTHER": "#2ca02c"},
)

fig.update_traces(marker=dict(size=5))
fig.update_yaxes(title_text="Weekly Infl. Detect.")
fig.update_yaxes(matches=None)     # optional: independent y-scales
fig.update_layout(showlegend=True)
fig.update_layout(margin=dict(l=60, r=150, t=40, b=40))
fig.update_layout(legend=dict(x=1.20, y=1, xanchor="left", yanchor="top"))
fig.update_xaxes(showline = True, linewidth=0.8, mirror=True)
fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
fig.for_each_annotation(lambda a: a.update(x=1.015,font=dict(size=18)))
for annotation in fig.layout.annotations:
    annotation.text = annotation.text.replace("COUNTRY=", "")
    annotation.textangle = 90

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


