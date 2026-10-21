#--------------------             
# Author : Serge Zaugg
# Description : trend (slope) all bu ine source 
#--------------------

from streamlit import session_state as ss
import plotly.express as px
import pandas as pd
import streamlit as st
from src.utils import filter_a_data_source
from src.utils import select_top_n_highest_slope
from src.utils_plots import make_metric_items_slope, make_mini_trace_slope
from src.utils_geo import prepre_for_pages_10_13, rm_if_stat_na_per_source
from src.utils_plots import make_bar_plot_pages_10_13, make_geo_map, make_per_source_strip_plot


with st.sidebar:
    st.markdown(f""":primary[Summary:] Her you can rank countries with highest flu trend first.""")
    st.divider()
    all_recent_dates = pd.Series(ss.df_metri_merged["ISO_WEEKSTARTDATE"].unique()).sort_values()
    sel_date = st.select_slider("Filter by recency", options=all_recent_dates, format_func=lambda x: x.strftime("%y-%m-%d"), key = "tbnhfgdbefrth")
    sel_data_source = st.radio(label = "Data Source", options = ["SENTINEL", "NONSENTINEL", "NOTDEFINED"], index=0, key="xcndhfgetr")
    sel_top_n = st.select_slider("Top N", options=[10,20,30], key = "fgbbhjmn")
    sel_thld = st.slider("Trend > t", min_value = -200.0, max_value = +200.0, value = 0.0, step = 10.0, key = "dfftzurqqffsxcv")


# apply user's choice 
df_metri_ma = ss.df_metri_merged[ss.df_metri_merged["ISO_WEEKSTARTDATE"] >= sel_date]
df_metri = filter_a_data_source(df_metri_ma, sel_data_source) 
df_trace = filter_a_data_source(ss.df_trace_ma, sel_data_source) 

# quick fix - supress stats if N was too small
df_metri.loc[df_metri["N_VALID"] < 3, "PERC_CHANGE"] = pd.NA
# keep only if + percent change positive
df_metri =  df_metri[df_metri["PERC_CHANGE"] > sel_thld]
# select top X
df_metri = select_top_n_highest_slope(df_metri, n=sel_top_n, sorting_var = 'PERC_CHANGE')

# with st.sidebar:
#     st.write("N countries", df_metri.shape[0])

#------------------
# make metric boxes 
rowheight = 150
prerend1 = [make_mini_trace_slope(row, rowheight, df_trace, ss.trace_x_range_ma, ss.stats_x_range_ma) for _, row in df_metri.iterrows()]

# smart way to fill in by rows (using st columns )
c1, c2, c3, c4, c5,  = st.columns([50, 90, 50, 90, 250])
col_pairs = [(c1, c2), (c3, c4)]
for i, row in df_metri.iterrows():
    c_metric, c_plot = col_pairs[i % 2]
    with c_metric:make_metric_items_slope(row, height_row=rowheight, show_percent=True)
    with c_plot:
        with st.container(border=True, height=rowheight):
            st.plotly_chart(prerend1[i], use_container_width=True, config={"displayModeBar": False})


#------------------
# make geo map 
# mollweide , orthographic , natural earth
fig_geo = make_geo_map(df_metri, "PERC_CHANGE", "bluered", height = 300, range_color = [-55,55], 
    legend_title = "Trend (Percent Change)", 
    # proj = "orthographic", 
    proj = None , 
    col_bar_horiz = False) 

df_scat = ss.df_metri_merged[ss.df_metri_merged["ORIGIN_SOURCE"] != "MAXCOMBINE"]
fig_strip = make_per_source_strip_plot(df = df_scat, yvar = "PERC_CHANGE", height = 300, log_y=False, y_title = "Trend (Percent Change)")
fig_strip.add_hline(y=sel_thld, line_width=2, line_dash="dot", line_color="grey" )

with c5:
    with st.container(border=True, height = 380):
        st.text("Mini-map (only countries from selection are highlighted)")
        st.plotly_chart(fig_geo, use_container_width=True)

    with st.container(border=True, height = 380):
        st.text("Overview of countries where metrics could be computed")
        st.plotly_chart(fig_strip, use_container_width=False)
