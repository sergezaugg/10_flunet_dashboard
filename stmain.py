#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# run locally : streamlit run stmain.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
# from utils import update_ss
import numpy as np

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# initial value of session state
if 'upar' not in ss:
    ss["upar"] = {
        "aaaaaaaa" : '3333',
        "vvvvvvvv" : '55555',
        }

# make navigation
p0 = st.Page("st_page_00.py", title="tbd")
p1 = st.Page("st_page_01.py", title="tbd")
pg = st.navigation([p1, p0])
pg.run()

with st.sidebar:
    st.markdown(":violet[**Interactive Exploration of FluNet data**]") 

    with st.container(border=True):
        st.text("blabla ")
       



    with st.container(border=True): 
        st.markdown("""
        ## AAAAAAAAAAAAAAA:             
        **aaaaaaaaa  
        **aaaaaaaaaaa 
        
        """)        
    # logos an links
    c1, c2 = st.columns([55,200])
    # c1.image(image='pics/z_logo_violet.png', width=65)
    c2.markdown('''
    :primary[v0.0.0]  
    :primary[Created by]
    :primary[[Serge Zaugg](https://www.linkedin.com/in/dkifh34rtn345eb5fhrthdbgf45)]  
    :primary[[Pollito-ML](https://github.com/sergezaugg)]
    ''')
    # st.logo(image='pics/z_logo_violet.png', size="large", link="https://github.com/sergezaugg")

       