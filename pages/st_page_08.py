#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

from streamlit import session_state as ss
import streamlit as st
from src.utils import get_latest_date_per_group

# load data to local page 
df_latest_data = ss.df_latest_data.copy()


df_latest_data = df_latest_data[["COUNTRY" , "ALL_latest"]]

df_latest_data["days_since"] = (ss.ts_today - df_latest_data["ALL_latest"]).dt.days

delays = df_latest_data["days_since"].unique()
delays.sort()
ctf = delays[0:3].max()

# an let's hope sorting will remain through next steps ;-)
df_latest_data = df_latest_data.sort_values("days_since")
df_latest_data["days_since_cat"] = (df_latest_data["days_since"].astype(str))
df_latest_data.loc[df_latest_data["days_since"] > ctf, "days_since_cat"] = "older"



cols = st.columns(6)

colors = ["#00ff55", "yellow", "orange", "red"]

for i, (col, cat) in enumerate(zip(cols, df_latest_data["days_since_cat"].unique())):

    with col:
        df_sel = df_latest_data.loc[df_latest_data["days_since_cat"] == cat,["COUNTRY"]]
    
        st.markdown(f'<span style="color:{colors[i]}"><b>{cat} days old</b></span>', unsafe_allow_html=True)
        st.markdown(f"**{len(df_sel)} countries**")
        st.dataframe(
            df_sel,
            hide_index=True,
            use_container_width=True,
            height = 2000
        )









