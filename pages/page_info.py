#--------------------             
# Author : Serge Zaugg
# Description : info 
#--------------------

from streamlit import session_state as ss
import streamlit as st

c1, c2, c3 = st.columns([30, 30, 2])
with c1:

    with st.container(border=True, height = 250):
        st.markdown("""
        #### About the dashboard:  
        This app provides a concise overview of the latest global influenza detection data.
        It also offers tools for exploring and analyzing influenza activity in greater detail at the country level.
        """)

    with st.container(border=True, height = 200):
        st.markdown("""
        #### Tabs legend:
        🔥 Recent stats on selected countries  
        🌍 Overview maps and charts     
        🔎 Deep dives  
        🔬 Tabular information  
        """)

    with st.container(border=True, height = 200):
        st.markdown('''
        #### Planned:
        -  compare countries for type A/B proportion
        -  include metrics boxes and geo map for positivity
       
        ''')


with c2:
    with st.container(border=True, height = 250):
        st.markdown("""
        #### Disclaimer:  
        This dashboard provides visualizations and analyses based on influenza surveillance data from **WHO FluNet**.
        The dashboard is an independent project and is **not an official WHO product**,
        nor is it endorsed by the World Health Organization.
        This dashboard is intended for **exploration and informational purposes**.
        It is not intended to provide medical advice, diagnosis, or to replace official public-health information or guidance.
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
   




# country codes 
