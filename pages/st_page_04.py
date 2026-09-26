#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------


import numpy as np
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import streamlit as st
from src.utils import filter_a_country, filter_data

bin_size = 7

def rolling_consecutive(g):
    d = g["ISO_WEEKSTARTDATE"]
    # length of consecutive 7-day streak
    consecutive = d.diff().eq(pd.Timedelta(days=7))
    streak = consecutive.groupby((~consecutive).cumsum()).cumsum() + 1
    ma = g["INF_ALL"].rolling(bin_size, min_periods=bin_size, center=True).mean()
    return ma.where(streak >= bin_size)



df_data = ss.df_data.copy()

# use only SUM_ALL here 
df = df_data[df_data["ORIGIN_SOURCE"] == "SUM_ALL"]
df = df.sort_values(["COUNTRY", "ISO_WEEKSTARTDATE"]).copy()
df["INF_MA"] = df.groupby("COUNTRY", group_keys=False).apply(rolling_consecutive)


# build control items in sidebar
with st.sidebar:
    who_regions = st.multiselect("WHO region", options = ss.WHOREGION_levels, key="k_who_01")
    fse_regions = st.multiselect("Flu Season region", options = ss.FLUSEASON_levels, key="k_who_02")
    prop_na_tol = st.slider("Required proportion non-NAs", min_value=0.0, max_value=1.0,  step=0.05, format="%.2f", key="k_who_04") 
    mean_count_tol = st.slider("Required Average count", min_value=0, max_value=100, step=1, format="%d", key="k_who_05")  
    country_info = st.empty() 

# apply user's data filter to data 
df_plot, n_countries = filter_data(df = df, 
    prop_non_na_tol = prop_na_tol, mean_count_tol = mean_count_tol, 
    who_regions = who_regions, 
    fse_regions = fse_regions, 
    itz_regions = ss.ITZ_levels.to_numpy().tolist())

# plot if n countries not too large
if n_countries[0] > ss.MAX_COUNTRIES_IN_PLOTS:
    country_info.text(f"N Countries too large!  = {n_countries[0]}")
else:
    country_info.text(f"N Countries = {n_countries[0]}")

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
        height=3000,
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


