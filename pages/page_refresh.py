#--------------------             
# Author : Serge Zaugg
# Description : misc stuff 
#--------------------

from streamlit import session_state as ss
import streamlit as st
from src.utils import download_flunet_data, preprocess_flunet_data, get_ts_today
import time
import streamlit as st

# st.write("code:", st.secrets['refreshcode'])

c1, c2 = st.columns([20, 50])
with c1:
    dev_mode = st.text_input("enter code", value="") == st.secrets['refreshcode']
    if dev_mode:
        with st.container(border=True, height = 300):
            st.markdown("""
            Here you can trigger the re-download of data from WHO.  
            The data at country level are updated weekly 
            """)

            st.warning("Refresh is needed at most once per day!")

            @st.cache_resource
            def get_refresh_state():
                return {"last_refresh": 0.0}

            refresh_state = get_refresh_state()
            COOLDOWN = 300  # 5 minutes

            if st.button("🔄 Refresh WHO data"):
                elapsed = time.time() - refresh_state["last_refresh"]

                if elapsed < COOLDOWN:
                    st.warning(f"Please wait {int(COOLDOWN - elapsed)} seconds before refreshing again.")
                else:
                    refresh_state["last_refresh"] = time.time()
                    get_ts_today.clear()
                    download_flunet_data.clear()
                    preprocess_flunet_data.clear()
                    st.rerun()    



