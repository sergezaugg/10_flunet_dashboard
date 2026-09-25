#--------------------             
# Author : Serge Zaugg
# Description : plot typa A and B proportions 
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
import numpy as np
import pandas as pd
from src.utils import filter_data, filter_a_country, filter_by_date_range
from src.utils_plots import make_facet_bar_plot
import pandas as pd
from plotly.subplots import make_subplots

df_data = ss.df_data.copy()

# use only SUM_ALL here 
df_data = df_data[df_data["ORIGIN_SOURCE"] == "SUM_ALL"]


all_countries = df_data['COUNTRY'].unique()
# Choose index of starting country
indx = int(np.where(all_countries == "Switzerland")[0][0])


# compute proportions of type A vs B
total = df_data["INF_A"].fillna(0) + df_data["INF_B"].fillna(0)
df_prop_ab = df_data.copy()
df_prop_ab["INF_A"] = df_prop_ab["INF_A"] / total
df_prop_ab["INF_B"] = df_prop_ab["INF_B"] / total
# wide to long for "INF_A" and "INF_B"
df_prop_long = df_prop_ab.melt(
    id_vars=df_prop_ab.columns.difference(["INF_A", "INF_B"]).tolist(),
    value_vars=["INF_A", "INF_B"],
    var_name="TYPE",
    value_name="PROP"
)


# build control items in sidebar
with st.sidebar:
    selected_country = st.selectbox("Choose a country:", options=all_countries, placeholder="Type or select a country...", index=indx, key="k_ab_01")
    plot_height = st.slider("Plot height", min_value=300, max_value=2000, step=100, key="k_ab_02") 
    area_cutoff = st.slider("Area cutoff", min_value=0,   max_value=1000, step=10, key="k_ab_03") 




df_plot = filter_a_country(df_prop_long, selected_country)



# make function from here 
# apply thld
df_plot.loc[df_plot["INF_ALL"] < area_cutoff, "PROP"] = np.nan
df_line_plot = df_plot[df_plot["TYPE"] == "INF_A"]

fig_line = px.line(
    df_line_plot,
    x="ISO_WEEKSTARTDATE",
    y="INF_ALL",
    facet_row="COUNTRY",
    template="plotly_dark", 
    color_discrete_sequence=["rgb(255,240,240)"]
)

fig_area = px.area(
    df_plot,
    x="ISO_WEEKSTARTDATE",
    y="PROP",
    facet_row="COUNTRY",
    color="TYPE",
    color_discrete_map={"INF_A": "#1f77b4",   "INF_B": "#d62728",   "OTHER": "#2ca02c"},
    template="plotly_dark", 
    markers = False,
    line_shape = 'hvh', # 'hvh',#'spline', One of 'linear', 'spline', 'hv', 'vh', 'hvh', or 'vhv'
)
fig_area.update_traces(line=dict(width=0))
# make fill color more intense (no transparency)
fig_area.for_each_trace(lambda trace: trace.update(fillcolor=trace.line.color.replace('rgb', 'rgba').replace(')', ', 0.3)')))

# wrap as two subplots 
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.16, 
                    subplot_titles=("Proportion of A/B Types", "Weekly Influenza Detections"))
for trace in fig_line.data:
    fig.add_trace(trace, row=2, col=1)
for trace in fig_area.data:
    fig.add_trace(trace, row=1, col=1)
# move subplot title a bit higher 
for annotation in fig.layout.annotations:
    annotation.y += 0.025

fig.update_layout(height=plot_height)
fig.update_xaxes(matches="x")
fig.update_layout(hovermode="x unified")
fig.update_xaxes(showline = True, linewidth=0.8, mirror=True)
fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
fig.update_yaxes(range=[0.0, 1.02], row=1, col=1)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})



