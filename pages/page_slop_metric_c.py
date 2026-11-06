#--------------------             
# Author : Serge Zaugg
# Description : trend (slope) 
#--------------------

from streamlit import session_state as ss
import plotly.express as px
import pandas as pd
import streamlit as st
from src.utils_pages import filter_a_data_source
from src.utils_pages import select_top_n_highest_slope
from src.utils_plots import make_metric_items_slope, make_mini_trace_slope
from src.utils_plots import make_geo_map, make_per_source_strip_plot

with st.sidebar:
    st.markdown(f""":primary[Summary:] Rank countries with highest flu trend first.""")
    st.divider()
    all_recent_dates = pd.Series(ss.df_metri_merged["ISO_WEEKSTARTDATE"].unique()).sort_values()
    sel_data_source = st.radio(label = "Data Source", options = ["COMBINED", "SENTINEL", "NONSENTINEL", "NOTDEFINED"], index=0, key="xcndhfgetr")
    sel_top_n = st.select_slider("Top N to Display", options=[10,20,30], value = 20, key = "fgbbhjmn")
    sel_thld = st.slider("Min Trend value to Display", min_value = -200.0, max_value = +200.0, value = 0.0, step = 10.0, key = "dfftzurqqffsxcv")
    sel_date = st.select_slider("Filter by recency", options=all_recent_dates, format_func=lambda x: x.strftime("%y-%m-%d"), key = "tbnhfgdbefrth")

# apply user's choice 
df_metri_ma = ss.df_metri_merged[ss.df_metri_merged["ISO_WEEKSTARTDATE"] >= sel_date]

# spec for COMBINED
if sel_data_source == "COMBINED":
    df_metri = df_metri_ma[df_metri_ma["perc_change_is_max"] == True]
    # get correct traces via the merge-mask trick
    df_mask = df_metri[['COUNTRY','ORIGIN_SOURCE']]
    df_trace = df_mask.merge(ss.df_trace_ma, on=['COUNTRY','ORIGIN_SOURCE'], how="left")
else :
    df_metri = filter_a_data_source(df_metri_ma, sel_data_source) 
    df_trace = filter_a_data_source(ss.df_trace_ma, sel_data_source) 

# quick fix - supress stats if N was too small
df_metri.loc[df_metri["N_VALID"] < 3, "PERC_CHANGE"] = pd.NA
# keep only if + percent change positive
df_metri =  df_metri[df_metri["PERC_CHANGE"] > sel_thld]
# select top X
df_metri = select_top_n_highest_slope(df_metri, n=sel_top_n, sorting_var = 'PERC_CHANGE')


#------------------
# display 

rowheight = 150

prerend1 = [make_mini_trace_slope(row, rowheight, df_trace, ss.trace_x_range_ma, ss.stats_x_range_ma) for _, row in df_metri.iterrows()]

# prepare the two main columns
m0, m1 = st.columns([280, 250])

# smart way to fill in by rows (using st columns )
with m0:
    with st.container(border = False, height = 700):
        c1, c2, c3, c4  = st.columns([50, 90, 50, 90])
        col_pairs = [(c1, c2), (c3, c4)]
        for i, row in df_metri.iterrows():
            c_metric, c_plot = col_pairs[i % 2]
            with c_metric:make_metric_items_slope(row, height_row=rowheight)
            with c_plot:
                with st.container(border=True, height=rowheight):
                    st.plotly_chart(prerend1[i], use_container_width=True, config={"staticPlot": True})

# make geo map 
# mollweide , orthographic , natural earth
fig_geo = make_geo_map(df_metri, "PERC_CHANGE", "bluered", height = 300, range_color = [-55,55], 
    legend_title = "Trend (Percent Change)", 
    # proj = "orthographic", 
    proj = None , 
    col_bar_horiz = False) 

df_scat = ss.df_metri_merged
fig_strip = make_per_source_strip_plot(df = df_scat, yvar = "PERC_CHANGE", height = 230, log_y=False, y_title = "Trend (Percent Change)")
fig_strip.add_hline(y=sel_thld, line_width=2, line_dash="dot", line_color="grey" )

with m1:
    with st.container(border=True, height = 370):
        st.caption("Mini-map (only top N countries from selection are highlighted)")
        st.plotly_chart(fig_geo, use_container_width=True)

    with st.container(border=True, height = 300):
        st.caption("Overview of Trend (Percent Change) across countries")
        st.plotly_chart(fig_strip, use_container_width=False)
