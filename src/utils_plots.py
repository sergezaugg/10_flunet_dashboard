#--------------------             
# Author : Serge Zaugg
# Description : functions that render display items
#--------------------

import numpy as np
import streamlit as st
import plotly.express as px
import pandas as pd
from config import cc
from plotly.subplots import make_subplots

@st.cache_data()
def make_facet_line_plot(df, n_countr, outcome):
    """ 
    aaa 
    """
    # pre-compute vertical spacings dependent on n_countr
    facet_height = 150
    spacing_px = 60
    height_b = (n_countr * facet_height + (n_countr - 1) * spacing_px + 200)
    facet_row_spacing = spacing_px / height_b

    fig = px.line(
        df,
        x = "ISO_WEEKSTARTDATE",
        y = outcome,
        color = "ORIGIN_SOURCE",
        facet_row = "COUNTRY",
        facet_row_spacing = facet_row_spacing,
        height= height_b,
        markers=True,
        color_discrete_sequence=[cc["sources"]["nonsen"], cc["sources"]["notdef"], cc["sources"]["sentin"], cc["sources"]["sumall"]]
    )
    fig.update_traces(marker=dict(size=5))
    # fig.update_yaxes(title_text="WEEKLY  DETECT.")
    fig.update_yaxes(matches=None,)   
    fig.update_layout(showlegend=True)
    fig.update_layout(margin=dict(l=60, r=150, t=50, b=40))
    fig.update_xaxes(showline = True, linewidth=1.8, mirror=True, showticklabels=True, ticks="inside",)
    fig.update_yaxes(showline = True, linewidth=1.8, mirror=True)
    fig.for_each_annotation(lambda a: a.update(x=1.015,font=dict(size=18)))
    fig.update_layout(legend=dict(title=None, bordercolor="white", borderwidth=1,))
    fig.update_layout(legend=dict(orientation="h", x=0, xanchor="left", y=1.015+1.03*facet_row_spacing, yanchor="top",))
    for annotation in fig.layout.annotations:
        annotation.text = annotation.text.replace("COUNTRY=", "")
        annotation.textangle = 0
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
    fig.update_layout(margin=dict(l=40, r=20, t=20, b=40))
    fig.update_layout(legend=dict(orientation="h", x=0, xanchor="left", y=1.2, yanchor="top",))
    fig.update_xaxes(showline = True, linewidth=0.8, mirror=True)
    fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
    fig.update_layout(legend_title_text="")
    return(fig)


@st.cache_data
def make_metric_items_slope(row, height_row, show_percent = False):
    
    if show_percent:
        selected_met = f"{int(row['PERC_CHANGE']):+d} % / W"
        selected_desc = "*Percent change" 
    else:
        selected_met = f"{int(row['SLOPE']):+d} / W"   
        selected_desc = "*New cases/week" 

    with st.container(border= True, height = height_row):
        st.metric(label=row['COUNTRY'],                  
            # value=f"{int(row['SLOPE']):+d} / W",
            value=selected_met,
            delta_description = selected_desc,
            border  = False, 
            width = 200, height = int(0.55*height_row))
        st.markdown(
            f'<span style="font-size: 12px;">Updated {row["ISO_WEEKSTARTDATE"].strftime("%Y-%m-%d")}</span>',
            unsafe_allow_html=True,)

#--------------------------------------------------

@st.cache_data
def make_mini_trace_slope(row, height_row, df_for_trace, xrange, stats_x_range):
    df_subset = df_for_trace[df_for_trace["COUNTRY"] == row['COUNTRY']]
    fig = px.line(
        df_subset, 
        x = 'ISO_WEEKSTARTDATE', 
        y = 'INF_MA', 
        height = int(0.8*height_row), 
        markers = True,
        color_discrete_sequence=[cc["traces"]["basic"]],
        )
    # # plot latest vals (used to compute slope) in another color 
    dfb = df_subset[df_subset['ISO_WEEKSTARTDATE'] > stats_x_range[0]]
    fig.add_scatter(x=dfb["ISO_WEEKSTARTDATE"],y=dfb["INF_MA"],mode="lines+markers",
        line=dict(color=    cc["traces"]["hot"]), marker=dict(color=  cc["traces"]["hot"]), showlegend=False)
    fig.add_hline(y=row['INF_ALL_BASELINE'], line_width=1, line_dash="dot", line_color="green")
    fig.add_vline(x=stats_x_range[0], line_width=1, line_dash="dot", line_color="red")
    fig.update_layout(margin=dict(l=10, r=15, t=10, b=10), xaxis_title=None, yaxis_title=None)
    fig.update_xaxes(showline = True, linewidth=0.8, mirror=True, range=xrange)
    fig.update_yaxes(showline = True, linewidth=0.8, mirror=True, rangemode="tozero",) # range=[0, None])
    return fig



@st.cache_data
def make_metric_items_baseline(row, height_row, time_range_stats):
    with st.container(border= True, height = height_row):
        st.metric(label=row['COUNTRY'], 
            value=f"{int(row['N_ABOVE_BASELINE'])} weeks",
            border  = False, 
            # delta_description = f"{int(row['N_ABOVE_BASELINE'])}/{time_range_stats} above BL",
            delta_description = f"BL: {int(row['INF_ALL_BASELINE'])}",
            width = 200, height = int(0.60*height_row))
        st.markdown(
            f'<span style="font-size: 12px;">Updated {row["ISO_WEEKSTARTDATE"].strftime("%Y-%m-%d")}</span>',
            unsafe_allow_html=True,)

@st.cache_data
def make_mini_trace_baseline(row, height_row, df_for_trace, trace_x_range, stats_x_range):
     with st.container(border= True, height = height_row):
        df_subset = df_for_trace[df_for_trace["COUNTRY"] == row['COUNTRY']]
        fig = px.line(
            df_subset, 
            x = 'ISO_WEEKSTARTDATE', 
            y = 'INF_ALL', 
            height = int(0.8*height_row), 
            markers = True,
            color_discrete_sequence=[cc["traces"]["basic"]],
        )
        fig.update_layout(margin=dict(l=10, r=15, t=10, b=10), xaxis_title=None, yaxis_title=None)
        fig.update_xaxes(showline = True, linewidth=0.8, mirror=True, range=trace_x_range)
        fig.update_yaxes(showline = True, linewidth=0.8, mirror=True, rangemode="tozero",)
        fig.add_hline(y=row['INF_ALL_BASELINE'], line_width=1, line_dash="dot", line_color="green")
        fig.add_hrect(y0=0.0, y1=row['INF_ALL_BASELINE'], fillcolor="pink", opacity=0.10, line_width=0, layer="below")
        fig.add_vline(x=stats_x_range[0], line_width=1, line_dash="dot", line_color="red")
        fig.add_vrect(x0=trace_x_range[0], x1=stats_x_range[0], fillcolor="pink", opacity=0.10, line_width=0, layer="below")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
















@st.cache_data
def display_df_page_08(df, nw_cutoff, height):

    
    def set_color_in_df(x):
        """ helper function for formatting df """
        if x < nw_cutoff:
            return "color: green"
        elif x >= nw_cutoff:
            return "color: red"
        return ""

    st.dataframe(
        df.style.map(set_color_in_df, subset=["days_since"]),
        hide_index=True,
        use_container_width=False,
        height = height,
        column_config={
            "COUNTRY": st.column_config.TextColumn("Country", width="auto", alignment="center",),
            "days_since": st.column_config.NumberColumn("Age (days)", width="auto", alignment="center",),
            "Latest date": st.column_config.DateColumn("Date", width="auto", alignment="center",),
        },
       
    )


@st.cache_data
def make_bar_plot_pages_10_13(df, xvar, xlabel, height):

    fig = px.bar(
        df,
        x="COUNTRY",
        y=xvar, 
        custom_data="CNTRY",
        # text="ISO_WEEKSTARTDATE_str",
        orientation="v",
        height=height,
        width=130 + len(df)*30,
        category_orders={"COUNTRY": df["COUNTRY"].tolist()},
        labels={xvar: xlabel},
    )

    fig.update_traces(width=0.7, marker_color=cc["traces"]["basic"])
    fig.update_traces(hovertemplate=(
        "%{customdata[0]}<br>"
        f"{xlabel}: %{{x}}"  ))

    # fig.update_xaxes(range=[0, x_max])
    fig.update_xaxes(side="top")
    fig.update_xaxes(tickangle=90)
    fig.update_xaxes(title=None)
    fig.update_layout(showlegend=False)
    fig.update_layout(margin=dict(l=60, r=60, t=20, b=20))
    fig.update_xaxes(showline = True, linewidth=0.8, mirror=True)
    fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
    # fig.update_traces(marker_color=cc["traces"]["hot"])
    return fig




@st.cache_data
def make_geo_map(df, var, colormap, height, range_color, legend_title):
    fig = px.choropleth(
        df,
        locations="COUNTRY",
        color=var,
        labels={var: legend_title},
        locationmode="ISO-3",
        projection="natural earth",
        color_continuous_scale=colormap, # "RdYlGn_r",
        range_color=range_color, 
        height=height
    )

    fig.update_geos(
        showframe=True, showcoastlines=True, showcountries=True,
        showocean=True, oceancolor="#1e5a8a", bgcolor="black",
        domain=dict(x=[0, 1], y=[0.0, 1]),
        projection_scale=0.9,   
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="black",
        plot_bgcolor="black",
    )

    return fig



@st.cache_data
def make_a_b_area_plot(df_plot, area_cutoff, col_a, col_b):
        
    # apply thld
    df_plot.loc[df_plot["INF_ALL"] < area_cutoff, "PROP"] = np.nan
    df_line_plot = df_plot[df_plot["TYPE"] == "INF_A"]

    fig_line = px.line(
        df_line_plot,
        x="ISO_WEEKSTARTDATE",
        y="INF_ALL",
        facet_row="COUNTRY",
        template="plotly_dark", 
        color_discrete_sequence=[cc["traces"]["basic"]],
    )

    fig_area = px.area(
        df_plot,
        x="ISO_WEEKSTARTDATE",
        y="PROP",
        facet_row="COUNTRY",
        color="TYPE",
        # color_discrete_map={"INF_A": cc["types"]["a"],   "INF_B": cc["types"]["b"],   "OTHER": cc["types"]["o"]},
        color_discrete_map={"INF_A": col_a,   "INF_B": col_b,   "OTHER": cc["types"]["o"]},
        template="plotly_dark", 
        markers = False,
        line_shape = 'hvh', # 'hvh',#'spline', One of 'linear', 'spline', 'hv', 'vh', 'hvh', or 'vhv'
    )
    fig_area.update_traces(line=dict(width=0))

    # make fill color more intense (no transparency)
    fig_area.for_each_trace(lambda trace: trace.update(fillcolor=trace.line.color.replace('rgb', 'rgba').replace(')', ', 0.3)')))

    # wrap as two subplots 
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.16, 
                        subplot_titles=("Weekly Influenza Detections", "Proportion of A/B Types"))
    for trace in fig_line.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in fig_area.data:
        fig.add_trace(trace, row=2, col=1)

    # move subplot title a bit higher 
    for annotation in fig.layout.annotations:
        annotation.y += 0.025
    fig.update_layout(margin=dict(l=40, r=20, t=20, b=40))
    fig.update_layout(height=600)
    fig.update_xaxes(matches="x")
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(showline = True, linewidth=0.8, mirror=True)
    fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
    fig.update_yaxes(range=[0.0, 1.02], row=2, col=1)
    fig.update_layout(legend=dict(orientation="h", x=0, xanchor="left", y=1.2, yanchor="top",))

    return fig





