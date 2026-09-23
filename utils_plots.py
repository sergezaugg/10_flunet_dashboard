#--------------------             
# Author : Serge Zaugg
# Description : functions that render display items
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

@st.cache_data()
def make_facet_bar_plot(df, n_years, inverse_year = False, indep_y_scale = False, plot_height = 150):

    # handle reverse plotting 
    years = sorted(df["SEASON_YEAR"].unique(), reverse=False)
    if inverse_year:    
        years = sorted(df["SEASON_YEAR"].unique(), reverse=True)

    row_spac = 0.005

    fig = px.bar(
        df,
        x="SEASON_WEEK",
        y="INF_ALL",
        facet_row="SEASON_YEAR",
        category_orders={"SEASON_YEAR": years},
        facet_row_spacing = row_spac,
        height= (n_years * (plot_height))
        )

    fig.add_vline(x=0, line_dash="dash", line_color="green", line_width=2)
    fig.update_layout(showlegend=True)
    fig.update_layout(margin=dict(l=60, r=150, t=40, b=40))
    fig.update_layout(legend=dict(x=1.20, y=1, xanchor="left", yanchor="top"))
    fig.update_xaxes(showline = True, linewidth=0.8, mirror=True)
    fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
    fig.for_each_annotation(lambda a: a.update(x=1.015,font=dict(size=18)))
    for annotation in fig.layout.annotations:
        annotation.text = annotation.text.replace("SEASON_YEAR=", "")
        annotation.textangle = 0

    # optional: independent y-scales
    if indep_y_scale == True:
        fig.update_yaxes(matches=None) 

    return(fig)



