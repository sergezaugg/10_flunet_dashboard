#--------------------             
# Author : Serge Zaugg
# Description : per country plot to show onset of flu wave 
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
import numpy as np
import pandas as pd
from src.utils import filter_a_country, re_center_season, filter_by_date_range
from src.utils_plots import make_facet_bar_plot
import pandas as pd

df_data = ss.df_data.copy()
df_data = re_center_season(df_data)
all_countries = df_data['COUNTRY'].unique()
# Choose index of starting country
indx = int(np.where(all_countries == "Switzerland")[0][0])

# build control items in sidebar
with st.sidebar:
    selected_country = st.selectbox("Choose a country:", options=all_countries, placeholder="Type or select a country...", index=indx, key="k_wave_01")
    date_range = st.slider("Date range", min_value=ss.date_range_dt[0], max_value=ss.date_range_dt[1], format="YYYY", key="k_wave_02") # format="YYYY") 
    curr_year_first = st.toggle(label = "Current year first", key="k_wave_03")
    indep_y_scales  = st.toggle(label = "Same Y-scales", key="k_wave_04")
    plot_height = st.slider("Plot height", min_value=25, max_value=500, step=25, key="k_wave_05") 

# apply filters 
df_data = filter_by_date_range(df = df_data, date_range = date_range)
df_data = filter_a_country(df_data, selected_country)
n_years = pd.Series(df_data["SEASON_YEAR"].unique()).value_counts().shape

# plot 
fig = make_facet_bar_plot(df = df_data, n_years = n_years[0], inverse_year = curr_year_first, indep_y_scale = not indep_y_scales,
                          plot_height = plot_height )
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})



