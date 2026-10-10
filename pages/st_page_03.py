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

# Choose index of starting country
indx = int(np.where(ss.ALL_COUNTRIES == "CHE")[0][0])

# build control items in sidebar
with st.sidebar:
    selected_country = st.selectbox("Choose a Country:", options=ss.ALL_COUNTRIES, placeholder="Type or select a country...", 
                                    index=indx, key="k_ab_01")
    sel_data_source = st.radio(label = "Data Source", options = ["SENTINEL", "NONSENTINEL", "NOTDEFINED"], index=0, key="k_ab_02")
    area_cutoff = st.slider("Detection Cutoff for Area", min_value=0, max_value=1000, step=10, key="k_ab_03") 
    c1,c2,_ = st.columns(3)
    col_a = c1.color_picker("A color", value="#1f21d0",)
    col_b = c2.color_picker("B color", value="#27c32c",)


df_data = df_data[df_data["ORIGIN_SOURCE"] == sel_data_source]
# df_data = df_data[df_data["ORIGIN_SOURCE"] == "NONSENTINEL"]




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



df_plot = filter_a_country(df_prop_long, selected_country)

fig =  make_a_b_area_plot(df_plot, area_cutoff, col_a, col_b)

c1,c2 = st.columns([30,5])
with c1:
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})



