#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
import pandas as pd
from utils import filter_data
from utils_plots import make_facet_line_plot
import pandas as pd


df_data = ss.df_data.copy()

# per country plot to show onset of flu wave 

# Re-define "year" as period from July -> June
df_data["SEASON_YEAR"] = (df_data["ISO_WEEKSTARTDATE"].dt.year - (df_data["ISO_WEEKSTARTDATE"].dt.month < 7))

# Reference date = 1 January within that season
jan1 = pd.to_datetime((df_data["SEASON_YEAR"] + 1).astype(str) + "-01-01")

# Set Jan 1 = week 0, previous weeks = -1, -2, ...
df_data["SEASON_WEEK"] = ((df_data["ISO_WEEKSTARTDATE"] - jan1).dt.days // 7) + 0


# plot 
countries = ["Switzerland"]
df = df_data[df_data["COUNTRY"].isin(countries)]
df = df[df["ORIGIN_SOURCE"] == "SUM_ALL"]

fig = px.bar(
    df,
    x="SEASON_WEEK",
    y="INF_ALL",
    facet_row="SEASON_YEAR",
    facet_row_spacing=0.004,
    height = 7000
    )

fig.add_vline(
    x=0,
    line_dash="dash",
    line_color="green",
    line_width=1
)

# fig.update_yaxes(matches=None)     # optional: independent y-scales

# fig.show()

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


