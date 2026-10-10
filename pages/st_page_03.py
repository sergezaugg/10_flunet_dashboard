#--------------------             
# Author : Serge Zaugg
# Description : plot typa A and B proportions 
#--------------------

import streamlit as st
from streamlit import session_state as ss
import numpy as np
from src.utils import filter_a_country
from config import cc
from src.utils_plots import make_a_b_area_plot

df_data = ss.df_data.copy()

# use only SUM_ALL here 
df_data = df_data[df_data["ORIGIN_SOURCE"] == "NONSENTINEL"]

all_countries = df_data['COUNTRY'].unique()
# Choose index of starting country
indx = int(np.where(all_countries == "CHE")[0][0])


# compute proportions of type A vs B
total = df_data["INF_A"].fillna(0) + df_data["INF_B"].fillna(0)
df_prop_ab = df_data.copy()
df_prop_ab["INF_A"] = df_prop_ab["INF_A"] / total
df_prop_ab["INF_B"] = df_prop_ab["INF_B"] / total
# wide to long for "INF_A" and "INF_B"
df_prop_long = df_prop_ab.melt(
    id_vars=df_prop_ab.columns.difference(["INF_A", "INF_B"]).tolist(),
    value_vars=["INF_A", "INF_B"],
    var_name="TYPE",
    value_name="PROP"
)

# build control items in sidebar
with st.sidebar:
    selected_country = st.selectbox("Choose a country:", options=all_countries, placeholder="Type or select a country...", index=indx, key="k_ab_01")
    # plot_height = st.slider("Plot height", min_value=300, max_value=2000, step=100, key="k_ab_02") 
    area_cutoff = st.slider("Area cutoff", min_value=0,   max_value=1000, step=10, key="k_ab_03") 

df_plot = filter_a_country(df_prop_long, selected_country)

fig =  make_a_b_area_plot(df_plot, area_cutoff)

c1,c2 = st.columns([30,5])
with c1:
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})



