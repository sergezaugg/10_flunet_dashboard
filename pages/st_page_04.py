#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

import plotly.express as px
from streamlit import session_state as ss
import streamlit as st
from src.utils import filter_data, ma_by_country

# build control items in sidebar
with st.sidebar:
    who_regions = st.multiselect("WHO region", options = ss.WHOREGION_levels, key="k_ma_01")
    prop_na_tol = st.slider("Required proportion non-NAs", min_value=0.0, max_value=1.0,  step=0.05, format="%.2f", key="k_ma_04") 
    mean_count_tol = st.slider("Required Average count", min_value=0, max_value=100, step=1, format="%d", key="k_ma_05")  
    ma_bin_size = st.select_slider("Moving Avg N weeks", options=[1,2,3,4,5,6,7,8,9,30], value=3, key="k_ma_06")
    country_info = st.empty() 

# load data to local page 
df = ss.df_sumall.copy()

# apply moving average 
df_ma = ma_by_country(df, bin_size = ma_bin_size)

# apply user's data filter to data 
df_plot, n_countries = filter_data(df = df_ma, 
    prop_non_na_tol = prop_na_tol, mean_count_tol = mean_count_tol, 
    who_regions = who_regions, 
    fse_regions = ss.FLUSEASON_levels.to_numpy().tolist(), 
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


