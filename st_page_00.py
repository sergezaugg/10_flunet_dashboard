#--------------------             
# Author : Serge Zaugg
# Description : classic time traces 
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
import pandas as pd
n_countries = ss.df_data_plot["COUNTRY"].nunique()

# handle NAs before plot
df_plot = ss.df_data_plot.copy()

df_plot.loc[df_plot["INF_ALL"].isna(), "ISO_WEEKSTARTDATE"] = pd.NaT

fig = px.line(
    df_plot,
    x="ISO_WEEKSTARTDATE",
    y="INF_ALL",
    color="ORIGIN_SOURCE",
    facet_row="COUNTRY",
    facet_row_spacing=0.004,
    height= (n_countries * 200)
)

fig.update_yaxes(matches=None)     # optional: independent y-scales
fig.update_layout(showlegend=True)
fig.update_layout(margin=dict(l=60, r=150, t=40, b=40))
fig.update_layout(legend=dict(x=1.20, y=1, xanchor="left", yanchor="top"))
fig.update_xaxes(showline = True, linewidth=0.8, mirror=True)
fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)

for annotation in fig.layout.annotations:
    annotation.text = annotation.text.replace("COUNTRY=", "")
    annotation.textangle = 45

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)




