#--------------------             
# Author : Serge Zaugg
# Description : assess baseline values
#--------------------

import streamlit as st
from streamlit import session_state as ss
from src.utils import filter_data_region, filter_several_countries, get_ts_today, filter_a_data_source
from src.utils_plots import make_facet_line_plot
import plotly.express as px
from src.preprocessing import keep_n_most_recent_weeks_2


# get bl thlds
df01 = ss.df_metri_merged[[ 'COUNTRY', 'ORIGIN_SOURCE', 'INF_ALL_BASELINE']]

# get traces 
# filter by region
with st.sidebar:
    who_regions = st.multiselect("Pre-select WHO Regions", options = ss.WHOREGION_levels, key="k_who_01")
    country_info_temp = st.empty() 

# apply user's data filter to data 
df_plot_temp, n_countries_temp = filter_data_region(df = ss.df_data, who_regions = who_regions, 
                                                    fse_regions = ss.FLUSEASON_levels.tolist(), 
                                                    itz_regions = ss.ITZ_levels)
country_info_temp.text(f"N Countries = {n_countries_temp[0]}")

# filter by country  
all_countries = df_plot_temp['COUNTRY'].unique()
with st.sidebar:
    sel_countries = st.multiselect("Select Countries", options=sorted(all_countries), placeholder="Select countries", key="k_who_06")
    country_info = st.empty() 
# apply user's data filter to data 
df02, n_countries = filter_several_countries(df_plot_temp, sel_countries)

with st.sidebar:
    sel_data_source = st.radio(label = "Data Source", options = ["SENTINEL", "NONSENTINEL", "NOTDEFINED"], key="k_tre_04")


df02 = filter_a_data_source(df02, sel_data_source)


# st.write(ss.time_range_basli)
# st.write(ss.ts_today)
# st.write(df02)

df02, _ = keep_n_most_recent_weeks_2(df02, ref_date = ss.ts_today , keep_n_weeks = ss.time_range_basli)


df = df02.merge(df01,on=["COUNTRY", "ORIGIN_SOURCE"],how="left")


if True:
    # df.head()
    df = df.head(20000)

    df_long = df.melt(
        id_vars=["COUNTRY", "ORIGIN_SOURCE", "ISO_WEEKSTARTDATE"],
        value_vars=["INF_ALL", "INF_ALL_BASELINE"],
        var_name="TYPE",
        value_name="VALUE",
    )


    fig = px.line(
        df_long,
        x="ISO_WEEKSTARTDATE",
        y="VALUE",
        color = "TYPE",
        facet_col="COUNTRY",
        facet_col_wrap=2,
        height=150*n_countries[0]-1,
        facet_row_spacing=0.030,
    )
    # fig.update_yaxes(type="log")
    fig.update_yaxes(matches=None)
    fig.update_yaxes(range=[0, None])
    fig.update_xaxes(showline = True, linewidth=1.8, mirror=True, showticklabels=True, ticks="inside",)
    fig.update_yaxes(showline = True, linewidth=1.8, mirror=True)

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

