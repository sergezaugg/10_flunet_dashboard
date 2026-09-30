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
s2 = df['ISO_WEEKSTARTDATE'].max() - pd.Timedelta(weeks=15)
df = df[df["ISO_WEEKSTARTDATE"] > s2]
df = df[['COUNTRY', 'ISO_WEEKSTARTDATE', 'INF_ALL']]
df = df.sort_values('ISO_WEEKSTARTDATE', ascending=False)


param_ma = 3
param_dif = 4
df = polyreg_by_country(df, bin_size = param_ma)


# take recent weeks only  
latest_date = df['ISO_WEEKSTARTDATE'].max()
week_0 = latest_date - pd.Timedelta(weeks=param_dif)
df0 = df[df['ISO_WEEKSTARTDATE'] >= week_0]
df0 = df0.sort_values('ISO_WEEKSTARTDATE', ascending=False)

# compute simple slope 
df0["SLOPE"] = (df0.groupby("COUNTRY")["INF_MA"].transform(lambda x: (x - x.shift(-param_dif)) ))


# df0[df0['COUNTRY'] == "China"]
# df0[df0['COUNTRY'] == "Bahrain"]



# keep only latest row per country 
week_1 = latest_date - pd.Timedelta(weeks=0)
df1 = df0[df0['ISO_WEEKSTARTDATE'] == week_1]


# select to with higherst slope 
df1 = df1.sort_values('SLOPE', ascending=False)
df1 = df1.dropna(subset=['SLOPE'])
df1 = df1.iloc[0:10].reset_index(drop=True) # top 10 




c1, c2, c3, c4, c5 = st.columns([60, 150, 50 , 80 , 50])

height_row = 150

for i, row in df1.iterrows():
    with c1:
        with st.container(border= True, height = height_row):
            date_str = row['ISO_WEEKSTARTDATE'].strftime('%b %d, %Y') # Format the date into a clean string (e.g., "Jul 13, 2026")
            st.metric(label=row['COUNTRY'], 
                value=f"{int(row['INF_ALL'])} cases",
                # delta=f"Δ {row['SLOPE']:+.0f}",
                delta=int(row['SLOPE']),
                delta_color="inverse", 
                delta_arrow = "auto", 
                delta_description = "Avg 3W change",
                border  = False, 
                width = 250, height = 180)
            
        
    with c2:
        with st.container(border= True, height = height_row):
            df_subset = df[df["COUNTRY"] == row['COUNTRY']]
            fig = px.line(df_subset, x = 'ISO_WEEKSTARTDATE', y = 'INF_ALL', height = int(0.8*height_row), markers = True)
            fig.add_annotation(x=0.01,y=0.98,xref="paper",yref="paper",text=row["COUNTRY"],showarrow=False,xanchor="left",yanchor="top")
            # fig.update_xaxes(tickvals=df_subset['ISO_WEEKSTARTDATE'])
            fig.update_layout(margin=dict(l=10, r=15, t=10, b=10), xaxis_title=None)
            fig.update_xaxes(showline = True, linewidth=0.8, mirror=True, )
            fig.update_yaxes(showline = True, linewidth=0.8, mirror=True)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})



