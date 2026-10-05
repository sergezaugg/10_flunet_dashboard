#--------------------             
# Author : Serge Zaugg
# Description : info 
#--------------------

from streamlit import session_state as ss
import streamlit as st

c1, xx, c2, c3 = st.columns([40, 5, 50, 20])
with c1:

    st.markdown("""
    #### About the dashboard:  
    This app provides a concise overview of the latest global influenza detection data.
    It also offers tools for exploring and analyzing influenza activity in greater detail at the country level.
    """)

    st.markdown("""
    #### Tabs legend:
    🔥 Recent stats on selected countries  
    📈 Overview charts on all countries    
    🔎 Deep dives (single country)  
    ℹ️ Tabular information  
    ⚙️ Settings  
    """)

    st.text("\n\n")
  
    st.markdown('''
    Author: 
    Serge Zaugg ( 
    [LinkedIn](https://www.linkedin.com/in/dkifh34rtn345eb5fhrthdbgf45/), 
    [GitHub](https://github.com/sergezaugg))
    ''')

with c2:
    st.markdown("""
    #### Disclaimer:  
    This dashboard provides visualizations and analyses based on influenza surveillance data from **WHO FluNet**.
    The dashboard is an independent project and is **not an official WHO product**,
    nor is it endorsed by the World Health Organization.
    This dashboard is intended for **exploration and informational purposes**.
    It is not intended to provide medical advice, diagnosis, or to replace official public-health information or guidance.
    """)

    st.markdown("""
    #### Data source:  
    Data is dowmloaded from the WHO API  
    `https://xmart-api-public.who.int/FLUMART/VIW_FNT?$format=csv`
    """)


   

# country codes 
