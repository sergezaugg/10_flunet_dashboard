#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

import numpy as np
import pandas as pd
from streamlit import session_state as ss
import streamlit as st


c1, c2, c3 = st.columns([30, 10, 2])
with c1:

    with st.container(border=True):
        st.markdown(f""":primary[Estimate Historical Baseline Threshold (HBT):]  
        All computation below per countries and data sources  
        Note: HBT attempts to estimate an :primary[upper bound] on BL fluctuations (not an average).  
        :primary[(1)] Restrain analysis period to {ss.time_range_basli} weeks before reference date  
        :primary[(2)] Exclude groups with more than {int(100*((ss.na_thld)))}% NAs in analysis period.  
        :primary[(3)] Missing weeks are padded with zeros (Only adequate for countries that fail to report 
        out-of-season when count can be assume low, but not for all countries)  
        :primary[(4.1)] qua = {ss.quantile_val} quantile of these values.  
        :primary[(4.2)] mad = median absolute deviation of these values.  
        :primary[(4.3)] Compute BL threshold as qua +   {ss.mad_factor} *mad (⚠️PRELIMINARY METHOD⚠️)  
        :primary[(5)] The BL threshold is floored at {int(ss.tol_thld)} to avoid unrealistically low baselines.   
        :primary[Limitation:] Same quantile is applied to all countries and data sources, 
                regardless of differences in seasonal patterns and reporting practices. 
                While this works well for many countries, it may fail for some. 
        """) 

    with st.container(border=True):
        st.markdown(f""":primary[Trend:]  
        The Trend is a metric of change in cases count relative to the Historical Baseline Threshold; it derived as follows:  
        :primary[(1)] Traces (blue line) are first smoothed with moving regression of degree {ss.ma_degree} with bin size of {ss.ma_bin_size} weeks.
        Trailing moving regression is used here (=right-aligned).  
        :primary[(2)] The average change per week (slope) is then estimated from the latest {int(ss.nw_slo)} weeks via linear regression.  
        :primary[(3)] Finally, the slope is divided by the historical baseline threshold and expressed as a percentage.  
        :primary[Unit:] Percent change per week [% week⁻¹]  
        :primary[Limitation:] Normalization by the historical baseline improves comparability
        but does not account for differences in seasonal patterns and reporting practices across countries and data sources.
        """)

    with st.container(border=True):
        st.markdown(f""":primary[Burden:]  
        The Burden is a metric of average cases count relative to the Historical Baseline Threshold; it derived as follows:  
        :primary[(1)] The average case count is estimated from the latest {int(ss.time_range_stats)} weeks.  
        :primary[(2)] This average is divided by the historical baseline threshold and expressed as a ratio.  
        :primary[Unit:] ratio [dimensionless]  
        :primary[Interpretation:] This is the Relative case burden, values above 1.0 mean that case count is above HBT.  
        :primary[Limitation:] Normalization by the historical baseline improves comparability
        but does not account for differences in seasonal patterns and reporting practices across countries and data sources.
        """)     
    



