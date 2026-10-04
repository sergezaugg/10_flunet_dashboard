#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

from streamlit import session_state as ss
import plotly.express as px
import pandas as pd
import streamlit as st
# from src.utils import polyreg_by_country_only, filter_a_data_source
# from src.utils import get_3_dfs_by_recency_for_top_n_slope, keep_n_most_recent_weeks

with st.sidebar:
    sel_data_source = st.radio(label = "Data Source", options = ["SENTINEL", "NONSENTINEL", "NOTDEFINED"], index=0)
st.text(sel_data_source)

df_slopes_all = ss.slope_dfs_by_source[sel_data_source][3]

df_slopes_all = df_slopes_all.dropna(subset=["SLOPE"])
df_slopes_all["ISO_WEEKSTARTDATE"] = (df_slopes_all["ISO_WEEKSTARTDATE"].dt.strftime("%Y-%m-%d"))
df_plot = df_slopes_all.sort_values("SLOPE", ascending = False)

c1, c2 = st.columns([50,50])

with c1:
    fig = px.bar(
        df_plot,
        x="SLOPE",
        y="COUNTRY",
        color="ISO_WEEKSTARTDATE",
        orientation="h",
        height=100 + len(df_plot)*40,
        category_orders={"COUNTRY": df_plot["COUNTRY"].tolist()},
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})







