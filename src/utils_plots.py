#--------------------             
# Author : Serge Zaugg
# Description : functions that render display items
#--------------------

import streamlit as st
import plotly.express as px
import pandas as pd

@st.cache_data()
def make_facet_line_plot(df, n_countr, outcome):
    " aaa "

    # handle NAs before plot
    df.loc[df["INF_ALL"].isna(), "ISO_WEEKSTARTDATE"] = pd.NaT

    fig = px.line(
        df,
        x = "ISO_WEEKSTARTDATE",
        y = outcome,
        color = "ORIGIN_SOURCE",
        facet_row="COUNTRY",
        facet_row_spacing=0.004,
        height= (n_countr * 200),
        markers=True,
    )
    fig.update_traces(marker=dict(size=5))
    # fig.update_yaxes(title_text="Weekly Infl. Detect.")
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
    
    fig.update_yaxes(title_text="Weekly Infl. Detect.")
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


@st.cache_data
def make_smoothed_curve_plot(df_plot):
    """
    TBD
    """
    # reshape to long for easy plotting of two traces 
    df_long = df_plot.melt(
        id_vars=[c for c in df_plot.columns if c not in ["INF_ALL", "INF_MA"]],
        value_vars=["INF_ALL", "INF_MA"],
        var_name="TYPE",
        value_name="INF_VALUE"
    )
    # plot 
    fig = px.line(
        df_long,
        x="ISO_WEEKSTARTDATE",
        y="INF_VALUE",
        color="TYPE",
        height=500,
        markers=True,
        color_discrete_map={"INF_ALL": "#1f77b4", "INF_MA": "#d62728", "OTHER": "#2ca02c"},
    )
    fig.update_traces(marker=dict(size=5))
    fig.update_yaxes(title_text="Weekly Infl. Detect.")
    fig.update_layout(showlegend=True)
    fig.update_layout(margin=dict(l=60, r=150, t=40, b=40))
    fig.update_layout(legend=dict(x=1.20, y=1, xanchor="left", yanchor="top"))
    fig.update_xaxes(showline = True, linewidth=0.8, mirror=True)
    fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
    return(fig)


@st.cache_data
def make_metric_items(row, height_row):
    with st.container(border= True, height = height_row):
        st.metric(label=row['COUNTRY'], 
            value=f"{int(row['INF_ALL'])} cases",
            delta=int(row['SLOPE']),
            delta_color="inverse", 
            delta_arrow = "auto", 
            delta_description = "Per Week",
            border  = False, 
            width = 200, height = int(0.60*height_row))
        st.markdown(
            f'<span style="font-size: 12px;">Updated {row["ISO_WEEKSTARTDATE"].strftime("%Y-%m-%d")}</span>',
            unsafe_allow_html=True,
        )


@st.cache_data
def make_mini_trace(row, height_row, df_for_trace, n_slope):
     with st.container(border= True, height = height_row):
        df_subset = df_for_trace[df_for_trace["COUNTRY"] == row['COUNTRY']]
        fig = px.line(df_subset, x = 'ISO_WEEKSTARTDATE', y = 'INF_MA', height = int(0.8*height_row), markers = True)
        # fig = px.line(df_subset, x = 'ISO_WEEKSTARTDATE', y = 'INF_ALL', height = int(0.8*height_row), markers = True)
        # plot latest vals in another color 
        dfb = df_subset.tail(n_slope)
        fig.add_scatter(x=dfb["ISO_WEEKSTARTDATE"],y=dfb["INF_MA"],mode="lines+markers",line=dict(color="orange"),
            marker=dict(color="orange"), showlegend=False)
        # fig.add_annotation(x=0.01,y=0.98,xref="paper",yref="paper",text=row["COUNTRY"], showarrow=False, xanchor="left", yanchor="top")
        # fig.update_xaxes(tickvals=df_subset['ISO_WEEKSTARTDATE'])
        fig.update_layout(margin=dict(l=10, r=15, t=10, b=10), xaxis_title=None, yaxis_title=None)
        fig.update_xaxes(showline = True, linewidth=0.8, mirror=True, )
        fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
