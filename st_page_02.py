#--------------------             
# Author : Serge Zaugg
# Description : per country plot to show onset of flu wave 
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
import pandas as pd
from utils import filter_data, filter_a_country, re_center_season
from utils_plots import make_facet_line_plot
import pandas as pd

df_data = ss.df_data.copy()
df_data = re_center_season(df_data)

all_countries = df_data['COUNTRY'].unique()

# build control items in sidebar
with st.sidebar:
    selected_country = selected_country = st.selectbox("Choose a country:", options=all_countries,
        index=None, placeholder="Type or select a country...")

df_plot = filter_a_country(df_data, selected_country)

# reverse plotting 
years = sorted(df_plot["SEASON_YEAR"].unique(), reverse=True)


fig = px.bar(
    df_plot,
    x="SEASON_WEEK",
    y="INF_ALL",
    facet_row="SEASON_YEAR",
    category_orders={"SEASON_YEAR": years},
    facet_row_spacing=0.004,
    height = 5000
    )

fig.add_vline(
    x=0,
    line_dash="dash",
    line_color="green",
    line_width=1
)

# fig.update_yaxes(matches=None)     # optional: independent y-scales
fig.update_layout(showlegend=True)
fig.update_layout(margin=dict(l=60, r=150, t=40, b=40))
fig.update_layout(legend=dict(x=1.20, y=1, xanchor="left", yanchor="top"))
fig.update_xaxes(showline = True, linewidth=0.8, mirror=True)
fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
fig.for_each_annotation(lambda a: a.update(x=1.015,font=dict(size=18)))
for annotation in fig.layout.annotations:
    annotation.text = annotation.text.replace("SEASON_YEAR=", "")
    annotation.textangle = 0

# fig.show()

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


