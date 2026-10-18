#--------------------             
# Author : Serge Zaugg
# Description : misc stuff 
#--------------------

from streamlit import session_state as ss
import streamlit as st
from src.utils import preprocess_flunet_data

c1, c2 = st.columns([15, 50])
with c1:
    # password protected maintenance dev-mode
    dev_mode = st.text_input("🛠️ Maintenance access: enter code 🍴", value="", type="password") == st.secrets['refreshcode']
    if dev_mode:
        with st.container(border=True, height = 400):    
            if st.button("🔄 Refresh data"):
                del ss["df_data"]
                preprocess_flunet_data.clear()
                st.rerun()
