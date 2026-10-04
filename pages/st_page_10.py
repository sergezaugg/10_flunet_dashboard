#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

from streamlit import session_state as ss
import plotly.express as px
import pandas as pd
import streamlit as st

@st.cache_data
def prepre_for_page10(df):
    df = df.dropna(subset=["SLOPE"])
    df["ISO_WEEKSTARTDATE"] = (df["ISO_WEEKSTARTDATE"].dt.strftime("%Y-%m-%d"))
    df = df.sort_values("SLOPE", ascending = False)
    return(df)

@st.cache_data
def make_bar_plot(df):
    fig = px.bar(
        df,
        x="SLOPE",
        y="COUNTRY",
        color="ISO_WEEKSTARTDATE",
        orientation="h",
        height=200 + len(df)*40,
        category_orders={"COUNTRY": df["COUNTRY"].tolist()},
    )
    fig.update_layout(showlegend=True)
    fig.update_layout(legend_title_text="Latest data from")
    fig.update_layout(margin=dict(l=60, r=60, t=80, b=40))
    fig.update_layout(legend=dict(orientation="h",x=0.5,y=1.02,xanchor="center",yanchor="bottom"))
    fig.update_xaxes(showline = True, linewidth=0.8, mirror=True)
    fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
    return fig

df_dat00 = prepre_for_page10(ss.slope_dfs_by_source["SENTINEL"])
df_dat01 = prepre_for_page10(ss.slope_dfs_by_source["NONSENTINEL"])
df_dat02 = prepre_for_page10(ss.slope_dfs_by_source["NOTDEFINED"])

# plot metrics and mini traces 
c1, c2, c3 = st.columns([50, 50 , 50])
with c1:
    st.text("SENTINEL")
with c2:
    st.text("NONSENTINEL")
with c3:
    st.text("NOTDEFINED")


c1, c2, c3 = st.columns([50,50,50])

with c1:
    fig = make_bar_plot(df_dat00)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c2:
    fig = make_bar_plot(df_dat01)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c3:
    fig = make_bar_plot(df_dat02)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})







