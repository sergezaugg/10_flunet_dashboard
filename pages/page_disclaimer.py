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
        #### Disclaimer:  
        This dashboard provides visualizations and analyses based on influenza surveillance data from **WHO FluNet**.
        The dashboard is an independent project and is **not an official WHO product**,
        nor is it endorsed by the World Health Organization.
        This dashboard is intended for **exploration and informational purposes**.
        It is not intended to provide medical advice, diagnosis, or to replace official public-health information or guidance.
        """)

   


   
   

