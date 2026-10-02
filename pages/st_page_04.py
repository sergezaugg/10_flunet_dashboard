#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

import numpy as np
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import streamlit as st
from src.utils import polyreg_by_country_source, filter_a_country, get_baseline_count

# Choose index of starting country
indx = int(np.where(ss.ALL_COUNTRIES == "Switzerland")[0][0])

# build control items in sidebar
with st.sidebar:
    selected_country = st.selectbox("Choose a country:", options=ss.ALL_COUNTRIES, placeholder="Type or select a country...", index=indx, key="k_tre_01")
    sel_data_source = st.radio(label = "Data Source", options = ["SENTINEL", "NONSENTINEL", "NOTDEFINED"], index=0, key="bbbbbbb")
    st.divider()
    quantile_val = st.slider("Quantile for baseline", min_value=0.0, max_value=1.0,  step=0.05, format="%.2f", key="aaaaaaaa")
    ma_bin_size = st.select_slider("Poly reg N weeks", options=np.arange(2,10), value=3, key="k_tre_02")
    ma_degree   = st.select_slider("Poly reg degree", options=np.arange(0,6), value=1, key="k_tre_03")

# load data to local page 
df = ss.df_data.copy()

# keep only n most recent weeks 
week_limit = df['ISO_WEEKSTARTDATE'].max() - pd.Timedelta(weeks=300)
df = df[df["ISO_WEEKSTARTDATE"] > week_limit]


# get baseline of flu counts (for all countries)
bthld = get_baseline_count(df, q = quantile_val)
# select values for chosen country and ORIGIN_SOURCE
thld = bthld.loc[bthld['COUNTRY']==selected_country]
thld = thld.loc[thld['ORIGIN_SOURCE']==sel_data_source]
thld = thld["INF_ALL_BASELINE"].item()


# apply moving regression (for all countries)
df_ma = polyreg_by_country_source(df, bin_size = ma_bin_size, deg = ma_degree)
df_ma = df_ma[df_ma["ORIGIN_SOURCE"] == sel_data_source]
df_plot = filter_a_country(df_ma, selected_country)






@st.cache_data
def make_smoothed_curve_plot(df_plot):
    """
    TBD
    """
    # reshape to long for easy plotting of two traces 
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
        color_discrete_map={"INF_ALL": "#1f77b4", "INF_MA": "#d62728", "OTHER": "#2ca02c"},
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
    return(fig)

fig = make_smoothed_curve_plot(df_plot)

fig.add_hline(y=thld, line_width=2, line_dash="dash", line_color="green")

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


