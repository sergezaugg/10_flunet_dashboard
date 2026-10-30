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
def make_facet_line_plot(df, n_countr, outcome, label_dict):
    """ 
    aaa 
    """

    # handle labels of multiple y variable
    y_label = label_dict[outcome]

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
        color_discrete_sequence=[cc["sources"]["nonsen"], cc["sources"]["notdef"], cc["sources"]["sentin"], cc["sources"]["sumall"]],
        labels={
            "ISO_WEEKSTARTDATE": "Date",
            outcome: y_label,
        },
    )
    fig.update_traces(marker=dict(size=5))   
    fig.update_layout(showlegend=True)
    fig.update_layout(margin=dict(l=60, r=150, t=50, b=40))
    fig.update_layout(legend=dict(title=None, bordercolor="white", borderwidth=1,))
    fig.update_layout(legend=dict(orientation="h", x=0, xanchor="left", y=1.015+1.03*facet_row_spacing, yanchor="top",))
    fig.update_xaxes(showline = True, linewidth=1.8, mirror=True, showticklabels=True, ticks="inside",)
    fig.update_xaxes(title_font=dict(size=14))
    fig.update_yaxes(matches=None,)  
    fig.update_yaxes(showline = True, linewidth=1.8, mirror=True)
    fig.update_yaxes(title_font=dict(size=16))
    fig.update_yaxes(range=[0.0, None]) 
    if outcome == "POSITIVITY":
        fig.update_yaxes(range=[0.0, 100.0]) 
    fig.for_each_annotation(lambda a: a.update(x=1.015,font=dict(size=18)))
    for annotation in fig.layout.annotations:
        annotation.text = annotation.text.replace("COUNTRY=", "")
        annotation.textangle = 0
    return(fig)    

@st.cache_data
def make_smoothed_curve_plot(df_plot, height):
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
        height=height,
        markers=True,
        color_discrete_map={"INF_ALL": "#1f77b4", "INF_MA": "#d62728", "OTHER": "#2ca02c"},
    )
    fig.update_traces(marker=dict(size=5))
    fig.update_yaxes(title_text="Flu detections [count]")
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
        selected_met = f"{int(row['PERC_CHANGE']):+d} %"
        selected_desc = "Per Week" 
    else:
        selected_met = f"{int(row['SLOPE']):+d} / W"   
        selected_desc = "*New cases/week" 

    with st.container(border= True, height = height_row):
        # st.metric(label=row['COUNTRY'],                  
        #     # value=f"{int(row['SLOPE']):+d} / W",
        #     value=selected_met,
        #     delta_description = selected_desc,
        #     border  = False, 
        #     width = 210, height = int(0.55*height_row))
        # st.markdown(
        #     f'<span style="font-size: 12px;">Upd. {row["ISO_WEEKSTARTDATE"].strftime("%Y-%m-%d")}</span>',
        #     unsafe_allow_html=True,)
        st.markdown(
            f"**{row['COUNTRY']}**  \n"
            f"{int(row['PERC_CHANGE']):+d} % \n"
            f"{row['ISO_WEEKSTARTDATE'].strftime('%Y-%m-%d')} "
            f"{row['ORIGIN_SOURCE']} ",
            # f"(n={row['N_VALID']}) weeks",
            unsafe_allow_html=False,
        )

@st.cache_data
def make_mini_trace_slope(row, height_row, df_for_trace, xrange, stats_x_range):
    df_subset = df_for_trace[df_for_trace["COUNTRY"] == row['COUNTRY']]
    fig = px.line(
        df_subset, 
        x = 'ISO_WEEKSTARTDATE', 
        y = 'INF_MA', 
        height = int(0.8*height_row), 
        # markers = True,
        color_discrete_sequence=[cc["traces"]["basic"]],
        )
    # # plot latest vals (used to compute slope) in another color 
    dfb = df_subset[df_subset['ISO_WEEKSTARTDATE'] > stats_x_range[0]]
    fig.update_xaxes(showticklabels=False)
    fig.add_scatter(x=dfb["ISO_WEEKSTARTDATE"],y=dfb["INF_MA"],
        # mode="lines+markers",
        mode="lines",
        line=dict(color = cc["traces"]["hot"]), 
        # marker=dict(color=  cc["traces"]["hot"]), 
        showlegend=False)
    fig.add_hline(y=row['INF_ALL_BASELINE'], line_width=1, line_dash="dot", line_color="green")
    # fig.add_vline(x=stats_x_range[0], line_width=1, line_dash="dot", line_color="red")
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), xaxis_title=None, yaxis_title=None)
    fig.update_xaxes(showline = True, linewidth=0.8, mirror=True, range=xrange, showgrid=False)
    fig.update_yaxes(showline = True, linewidth=0.8, mirror=True, rangemode="tozero", showgrid=False) 
    return fig



@st.cache_data
def make_metric_items_baseline(row, height_row, time_range_stats):
    with st.container(border= True, height = height_row):
        # st.caption(row['COUNTRY'])
        # st.text(f"{np.round(row['REL_BURDEN'], 1)}")     
        # st.caption(row["ISO_WEEKSTARTDATE"].strftime("%Y-%m-%d") + 
        #            " " + row["ORIGIN_SOURCE"] +
        #            " " + f"(n={row['N_VALID']}) weeks")
        st.markdown(
            f"**{row['COUNTRY']}**  \n"
            f"{np.round(row['REL_BURDEN'], 1)}  \n"
            f"{row['ISO_WEEKSTARTDATE'].strftime('%Y-%m-%d')} "
            f"{row['ORIGIN_SOURCE']} "
            f"(n={row['N_VALID']}) weeks",
            unsafe_allow_html=False,
        )

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
        use_container_width=True,
        height = height,
        column_config={
            "COUNTRY": st.column_config.TextColumn("Country", width="auto", alignment="center",),
            "days_since": st.column_config.NumberColumn("Age (days)", width="auto", alignment="center",),
            "Latest date": st.column_config.DateColumn("Date", width="auto", alignment="center",),
        },
       
    )


@st.cache_data
def make_bar_plot_pages_10_13(df, xvar, xlabel, height, colormap, range_color):

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
        color=xvar,
        range_color=range_color, 
        color_continuous_scale=colormap,
    )

    fig.update_coloraxes(showscale=False)
    # fig.update_xaxes(range=[-0.1, None])
    fig.update_traces(width=0.7,) #  marker_color=cc["traces"]["basic"])
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
def make_geo_map(df, var, colormap, height, range_color, legend_title, proj = "mollweide", col_bar_horiz = False): 
    # mollweide , orthographic , natural earth
    fig = px.choropleth(
        df,
        locations="COUNTRY",
        color=var,
        labels={var: legend_title},
        locationmode="ISO-3",
        projection=proj,
        color_continuous_scale=colormap, 
        range_color=range_color, 
        height=height,
    )

    fig.update_geos(
        showframe=False, showcoastlines=True, showcountries=True,
        showocean=True, oceancolor="#1e5a8a", bgcolor="black",
        domain=dict(x=[0, 1], y=[0.0, 1]),
        projection_scale=0.99,   
    )

    bar_dict = dict(title=dict(text=legend_title, side="right"), len=0.6, thickness=12,)
    if col_bar_horiz :
        bar_dict = dict(title=dict(text=legend_title, side="top"),
                    orientation="h", x=0.5, xanchor="center", y=0.95, yanchor="bottom", len=0.8, thickness=12,)

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="black",
        plot_bgcolor="black",
        coloraxis_colorbar=bar_dict,
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
    # adjut labels of the legend 
    fig_area.for_each_trace(lambda t: t.update(name={"INF_A": "Type A Influenza", "INF_B": "Type B Influenza"}[t.name]))
    # make fill color more intense (no transparency)
    fig_area.for_each_trace(lambda trace: trace.update(fillcolor=trace.line.color.replace('rgb', 'rgba').replace(')', ', 0.3)')))

    # wrap as two subplots 
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.16, 
                        subplot_titles=("Flu detections [count]", "Proportion of A/B Types"))
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


@st.cache_data
def make_per_source_strip_plot(df, yvar, height, log_y, y_title):
    """  """
    fig = px.strip(df, x="ORIGIN_SOURCE", y=yvar, 
        log_y=log_y, height = height, labels = {yvar : y_title})
    fig.update_layout(
        margin=dict(l=10, r=120, t=10, b=1),
        paper_bgcolor="black",
        plot_bgcolor="black",
        yaxis=dict(side="right"),
        )
    fig.update_xaxes(showline = True, linewidth=0.8, mirror=True)
    fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
    return fig


