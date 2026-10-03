#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

import numpy as np
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import streamlit as st
from src.utils import polyreg_by_country_source, filter_a_country, get_baseline_count, filter_a_data_source
from src.utils import det_regions, get_start_stop_of_region
from src.utils_plots import make_smoothed_curve_plot

# # Choose index of starting country
indx = int(np.where(ss.ALL_COUNTRIES == "Switzerland")[0][0])

# build control items in sidebar
with st.sidebar:
    selected_country = st.selectbox("Choose a country:", options=ss.ALL_COUNTRIES, placeholder="Select country", 
                                    index=indx, key="k_tre_01")
    sel_data_source = st.radio(label = "Data Source", options = ["SENTINEL", "NONSENTINEL", "NOTDEFINED"], key="k_tre_04")
    st.divider()
    quantile_val = st.slider("Quantile for baseline", min_value=0.0, max_value=1.0,  step=0.05, format="%.2f", key="k_tre_05")
    ma_bin_size = st.select_slider("Poly reg N weeks", options=np.arange(2,10), key="k_tre_02")
    ma_degree   = st.select_slider("Poly reg degree", options=np.arange(0,6), key="k_tre_03")

# load data to local page 
df = ss.df_data.copy()

# keep only n most recent weeks 
week_limit = df['ISO_WEEKSTARTDATE'].max() - pd.Timedelta(weeks=300)
df = df[df["ISO_WEEKSTARTDATE"] > week_limit]

# sel_data_source = "SENTINEL"
# sel_data_source = "NOTDEFINED"

# apply moving regression (for all countries)
df_ma = polyreg_by_country_source(df, bin_size = ma_bin_size, deg = ma_degree)
df_plot = filter_a_data_source(df_ma, sel_data_source)
df_plot = filter_a_country(df_plot, selected_country)

# plot if any reasonable data 
if len(df_plot) < 10:
    st.info(f"Not enough data for this country and data source")
    st.stop()

# get baseline of flu counts (for all countries)
bthld = get_baseline_count(df, q = quantile_val)
# select values for chosen country and ORIGIN_SOURCE
thld = bthld.loc[bthld['COUNTRY']==selected_country]
thld = thld.loc[thld['ORIGIN_SOURCE']==sel_data_source]
thld = thld["INF_ALL_BASELINE"].item()

# define epidemic periods from smoothed count and threshold 
df_plot['set_reg'] = det_regions(df_plot["INF_MA"], thld)
sta, end = get_start_stop_of_region(df_plot['set_reg'], df_plot['ISO_WEEKSTARTDATE'])

#-----------------------
# plot 
fig = make_smoothed_curve_plot(df_plot)
# overlay threshold 
fig.add_hline(y=thld, line_width=2, line_dash="dash", line_color="green")
# overlay epidemic periods 
for start, end in zip(sta, end):
    fig.add_vrect(x0=start, x1=end, fillcolor="pink", opacity=0.10, line_width=0, layer="below")
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


