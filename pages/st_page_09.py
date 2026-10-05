#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

from streamlit import session_state as ss
import streamlit as st

_ = st.slider("Overall Date Range", 
    min_value = ss.date_init[0].to_pydatetime(), 
    max_value = ss.date_init[1].to_pydatetime(),
    format = "YYYY-MM-DD", 
    key = "k_set_01"
    )

# st.text(ss.k_set_01)
# ss.ts_today = ss.k_set_01[1]
