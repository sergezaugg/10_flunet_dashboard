#--------------------             
# Author : Serge Zaugg
# Description : stuff for the devs
#--------------------

import streamlit as st
from streamlit import session_state as ss

c1, c2 = st.columns([50,1])
with c1:
    st.text("Ah yeah .. you couldn't help clicking on the skull 💀 You were lucky, "
    "no danger here, this page is just for the devs to explore the session state of the app." )

st.title(" \n  ")
st.title(" \n  ")
st.json(dict(st.session_state))
