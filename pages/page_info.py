#--------------------             
# Author : Serge Zaugg
# Description : text-only page with general info 
#--------------------

from streamlit import session_state as ss
import streamlit as st
from src.utils import download_flunet_data, preprocess_flunet_data

c1, c2, c3 = st.columns([30, 30, 2])
with c1:

    with st.container(border=True, height = 300):
        st.markdown("""
        #### About the dashboard:  
        FluNet Explorer provides an interactive overview of global influenza virus detections using data from the WHO FluNet surveillance system.
        Explore trends across countries and WHO regions and track changes over time.
        Interactive visualizations highlight recent activity and deviations from historical baselines.
        Explore geographic patterns to identify countries with increasing or unusually high detection levels.
        Data are retrieved from the WHO API and updated as new surveillance reports become available.
        Reported detections reflect surveillance and testing practices, which vary across countries and over time.
        This dashboard is an exploratory data analysis tool, not a substitute for official public health assessments.
        """)

    with st.container(border=True, height = 200):
        st.markdown("""
        #### Data source:  
        Data is downloaded from the WHO API  
        `https://xmart-api-public.who.int/FLUMART/VIW_FNT?$format=csv`
        """)

    with st.container(border=True, height = 200):
        st.markdown('''
        #### Author:
        Serge Zaugg ( 
        [LinkedIn](https://www.linkedin.com/in/dkifh34rtn345eb5fhrthdbgf45/), 
        [GitHub](https://github.com/sergezaugg))
        ''')
   

