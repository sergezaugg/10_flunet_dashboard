#--------------------             
# Author : Serge Zaugg
# Description : stuff for the devs
#--------------------

import streamlit as st
from streamlit import session_state as ss

st.json(dict(st.session_state))
