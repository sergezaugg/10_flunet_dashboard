#--------------------             
# Author : Serge Zaugg
# Description : functions that render a display item
#--------------------

import streamlit as st
import plotly.express as px
import pandas as pd

@st.cache_data()
def make_facet_line_plot(df, n_countr):
    " aaa "
    fig = px.line(
        df,
        x="ISO_WEEKSTARTDATE",
        y="INF_ALL",
        color="ORIGIN_SOURCE",
        facet_row="COUNTRY",
        facet_row_spacing=0.004,
        height= (n_countr * 200)
    )
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





