#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

import numpy as np
import pandas as pd
from streamlit import session_state as ss
import streamlit as st
# from src.utils import filter_a_country, filter_a_data_source
# from src.utils import det_regions, get_start_stop_of_region
# from src.preprocessing import polyreg_by_country_source, get_baseline_threshold
# from src.utils_plots import make_smoothed_curve_plot


    

with st.container(border=True):
    st.markdown(f""":primary[Estimate Historical Baseline Threshold:]  
    :primary[(1)] Restrain analysis period to {ss.time_range_basli} weeks before reference date  
    :primary[(2)] Exclude groups with more than {int(100*((ss.na_thld)))}% NAs in analysis period.  
    :primary[(3)] Add missing weeks in ISO_WEEKSTARTDATE and replace NA with 0  
    :primary[(4)] Compute BL threshold as the {ss.quantile_val} quantile of these values.    
    """)  



c01,c02,c03 = st.columns([15,20,20])
height_all = 500
    
with c01:
    with st.container(border=True, height = height_all):
        st.markdown(f""":primary[Historical Baseline Threshold:] 
        Missing weeks are padded with zeros (Only adequate for countries
        that fail to report out-of-season when count can be assume low, but not for all countries)
        Then, a historical baseline threshold (green line) is computed per-county and data source from {ss.quantile_val} 
        quantile taken over {int(ss.time_range_basli)} weeks.
        Lastly, the threshold is floored at {int(ss.tol_thld)} to avoid unrealistically low baselines in 
        countries with sparse detections.  
        :primary[Limitation:] Same quantile is applied to all countries and data sources, 
        regardless of differences in seasonal patterns and reporting practices. 
        While this works well for many countries, it may fail for some.
        """)  
with c02:
    with st.container(border=True, height = height_all):
        st.markdown(f""":primary[BL-Normalized Change:] Traces (blue line) are first smoothed with moving regression of degree {ss.ma_degree}
        with bin size of {ss.ma_bin_size} weeks (red line). Trailing moving regression is used here (=right-aligned).
        The average change per week (slope) is then estimated from the latest {int(ss.nw_slo)} weeks via linear regression.
        Finally, the slope is normalized by the historical baseline threshold and expressed as a percentage.  
        :primary[Limitation:] Normalization by the historical baseline improves comparability
        but does not account for differences differences in seasonal patterns and reporting practices across countries and data sources.
        """)



