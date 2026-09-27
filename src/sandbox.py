"""
Exploration of FluNet data
Author: Serge Zaugg
Date: 2026-09-14
"""

import pandas as pd
import plotly.express as px
from src.utils import download_flunet_data, preprocess_flunet_data, include_rows_for_total_flunet_data
from plotly.subplots import make_subplots

# download and pre-process (do once)
df_dat, df_meta, download_ts = download_flunet_data()

df_dat.columns
df_dat['SPEC_RECEIVED_NB'].isna().mean()
df_dat['SPEC_PROCESSED_NB'].isna().mean()
df_dat['INF_ALL'].isna().mean()

pd.crosstab(df_dat['SPEC_PROCESSED_NB'].isna(), 
            df_dat['INF_ALL'].isna())





df_data = preprocess_flunet_data(df = df_dat)
df_data = include_rows_for_total_flunet_data(df = df_data)
df_sumall = df_data[df_data["ORIGIN_SOURCE"] == "SUM_ALL"]

WHOREGION_levels = df_data["WHOREGION"].unique()
FLUSEASON_levels = df_data["FLUSEASON"].unique()

WHOREGION_levels.to_numpy().tolist()
WHOREGION_levels.to_numpy().tolist()








