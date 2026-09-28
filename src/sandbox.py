"""
Exploration of FluNet data
Author: Serge Zaugg
Date: 2026-09-14
"""

import pandas as pd
import plotly.express as px
from src.utils import download_flunet_data, preprocess_flunet_data, sum_over_origin_source
from plotly.subplots import make_subplots
from config import FLUNET_DATA_URL, FLUNET_META_URL


df_meta = pd.read_csv(FLUNET_META_URL)





# download and pre-process (do once)
df_dat, download_ts = download_flunet_data()

df_dat.columns
df_dat['SPEC_RECEIVED_NB'].isna().mean()
df_dat['SPEC_PROCESSED_NB'].isna().mean()
df_dat['INF_ALL'].isna().mean()

pd.crosstab(df_dat['SPEC_PROCESSED_NB'].isna(), 
            df_dat['INF_ALL'].isna())





df_data = preprocess_flunet_data(df = df_dat)
df_data = sum_over_origin_source(df = df_data)
df_sumall = df_data[df_data["ORIGIN_SOURCE"] == "SUM_ALL"]

WHOREGION_levels = df_data["WHOREGION"].unique()
FLUSEASON_levels = df_data["FLUSEASON"].unique()

WHOREGION_levels.to_numpy().tolist()
WHOREGION_levels.to_numpy().tolist()








