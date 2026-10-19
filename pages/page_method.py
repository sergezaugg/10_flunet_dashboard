#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

import numpy as np
import pandas as pd
from streamlit import session_state as ss
import streamlit as st

with st.sidebar:
    st.error("⚠️Preliminary methodology⚠️")

with st.container(border=True):
    st.markdown(f""":primary[Estimate Historical Baseline Threshold:]  
    All computation below per countries and data sources  
    :primary[(1)] Restrain analysis period to {ss.time_range_basli} weeks before reference date  
    :primary[(2)] Exclude groups with more than {int(100*((ss.na_thld)))}% NAs in analysis period.  
    :primary[(3)] Missing weeks are padded with zeros (Only adequate for countries that fail to report 
    out-of-season when count can be assume low, but not for all countries)  
    :primary[(4)] Compute BL threshold as the {ss.quantile_val} quantile of these values.   
    :primary[(5)] The threshold is floored at {int(ss.tol_thld)} to avoid unrealistically low baselines in countries with sparse detections.  
    :primary[Limitation:] Same quantile is applied to all countries and data sources, 
            regardless of differences in seasonal patterns and reporting practices. 
            While this works well for many countries, it may fail for some. 
    """) 

with st.container(border=True):
    st.markdown(f""":primary[Burden = BL-Normalized avrage:] 
    <TBD>
    """)     

with st.container(border=True):
    st.markdown(f""":primary[Trend = BL-Normalized Change:]  
    :primary[(1)] Traces (blue line) are first smoothed with moving regression of degree {ss.ma_degree} with bin size of {ss.ma_bin_size} weeks.
    Trailing moving regression is used here (=right-aligned).  
    :primary[(2)] The average change per week (slope) is then estimated from the latest {int(ss.nw_slo)} weeks via linear regression.  
    :primary[(3)] Finally, the slope is normalized by the historical baseline threshold and expressed as a percentage.    
    :primary[Limitation:] Normalization by the historical baseline improves comparability
    but does not account for differences differences in seasonal patterns and reporting practices across countries and data sources.
    """)


   



