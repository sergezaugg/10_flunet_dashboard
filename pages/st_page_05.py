#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

import numpy as np
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import streamlit as st
from src.utils import ma_by_country, polyreg_by_country, filter_a_country


# load data to local page 
df = ss.df_sumall.copy()

# keep only n most recent weeks 
s2 = df['ISO_WEEKSTARTDATE'].max() - pd.Timedelta(weeks=3)
df = df[df["ISO_WEEKSTARTDATE"] > s2]

df = df[['COUNTRY', 'ISO_WEEKSTARTDATE', 'INF_ALL']]
df = df.dropna(subset=['INF_ALL'])

latest_date = df['ISO_WEEKSTARTDATE'].max()

# 1st recent week 
week_0 = latest_date - pd.Timedelta(weeks=0)
df0 = df[df['ISO_WEEKSTARTDATE'] == week_0]
df0 = df0.sort_values('INF_ALL', ascending=False)
df0 = df0.iloc[0:10].reset_index(drop=True) # top 10 

# 2nd recent week 
week_1 = latest_date - pd.Timedelta(weeks=1)
df1 = df[df['ISO_WEEKSTARTDATE'] == week_1]
df1 = df1.sort_values('INF_ALL', ascending=False)
df1 = df1.iloc[0:10].reset_index(drop=True) # top 10 





c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    for i, row in df0.iterrows():
        date_str = row['ISO_WEEKSTARTDATE'].strftime('%b %d, %Y') # Format the date into a clean string (e.g., "Jul 13, 2026")
        st.metric(label=row['COUNTRY'], value=f"{int(row['INF_ALL'])} cases", delta=f"Week of {date_str}", 
            delta_color="inverse" , delta_arrow = "off", border  = True, width = "content")

with c2:
    for i, row in df1.iterrows():
        date_str = row['ISO_WEEKSTARTDATE'].strftime('%b %d, %Y') # Format the date into a clean string (e.g., "Jul 13, 2026")
        st.metric(label=row['COUNTRY'], value=f"{int(row['INF_ALL'])} cases", delta=f"Week of {date_str}", 
            delta_color="inverse" , delta_arrow = "off", border  = True, width = "content")

