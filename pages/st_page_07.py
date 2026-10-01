#--------------------             
# Author : Serge Zaugg
# Description : get metric for "above baseline"
#--------------------

import numpy as np
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import streamlit as st
from src.utils import filter_data
from src.utils_plots import make_facet_line_plot

# load data to local page 
df = ss.df_data.copy()
# df = df[df["ORIGIN_SOURCE"] == "NONSENTINEL"]


# keep only n most recent weeks 
week_limit = df['ISO_WEEKSTARTDATE'].max() - pd.Timedelta(weeks=150)
df = df[df["ISO_WEEKSTARTDATE"] > week_limit]
df = df[['COUNTRY', 'ORIGIN_SOURCE', 'ISO_WEEKSTARTDATE', 'INF_ALL']]

df = df[df["ORIGIN_SOURCE"] == "SENTINEL"]


baseline_thresholds = (df.groupby(["COUNTRY", "ORIGIN_SOURCE"])["INF_ALL"].quantile(0.40).reset_index(name="INF_ALL_BASELINE"))

st.dataframe(baseline_thresholds, height = 800)







