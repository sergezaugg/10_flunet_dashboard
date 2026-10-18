#--------------------             
# Author : Serge Zaugg
# Description : trend from past few weeks 
#--------------------

import numpy as np
import pandas as pd
from streamlit import session_state as ss
import streamlit as st
from src.utils import filter_a_country, filter_a_data_source
from src.utils import det_regions, get_start_stop_of_region
from src.preprocessing import polyreg_by_country_source, get_baseline_threshold
from src.utils_plots import make_smoothed_curve_plot

# # Choose index of starting country
indx = int(np.where(ss.ALL_COUNTRIES == "CHE")[0][0])

# build control items in sidebar
with st.sidebar:
    selected_country = st.selectbox("Choose a country:", options=ss.ALL_COUNTRIES, placeholder="Select country", index=indx, key="k_tre_01")
    sel_data_source = st.radio(label = "Data Source", options = ["SENTINEL", "NONSENTINEL", "NOTDEFINED"], key="k_tre_04")
    quantile_val = st.slider("Quantile for baseline", min_value=0.0, max_value=1.0,  step=0.05, format="%.2f", key="k_tre_05")
    ma_bin_size = st.select_slider("Poly reg N weeks", options=np.arange(2,10), key="k_tre_02")
    ma_degree   = st.select_slider("Poly reg degree", options=np.arange(0,6), key="k_tre_03")
    st.error("⚠️Preliminary methodology⚠️")


# load data to local page 
df = ss.df_data.copy()

# keep only n most recent weeks 
week_limit = df['ISO_WEEKSTARTDATE'].max() - pd.Timedelta(weeks=ss.nw_for_demo)
df = df[df["ISO_WEEKSTARTDATE"] > week_limit]

# apply moving regression (for all countries)
df_sel1 = filter_a_country(df, selected_country)
df_sel2 = filter_a_data_source(df_sel1, sel_data_source)
df_plot = polyreg_by_country_source(df_sel2, bin_size = ma_bin_size, deg = ma_degree)


# plot if any reasonable data 
if len(df_plot) < 10:
    st.info(f"Not enough data for this country and data source")
    st.stop()

# get baseline of flu counts (for all countries)
bthld = get_baseline_threshold(df, q = quantile_val, tol_thld = ss.tol_thld)
# select values for chosen country and ORIGIN_SOURCE
thld = bthld.loc[bthld['COUNTRY']==selected_country]
thld = thld.loc[thld['ORIGIN_SOURCE']==sel_data_source]
thld = thld["INF_ALL_BASELINE"].item()

# define epidemic periods from smoothed count and threshold 
df_plot['set_reg'] = det_regions(df_plot["INF_MA"], thld)
sta, end = get_start_stop_of_region(df_plot['set_reg'], df_plot['ISO_WEEKSTARTDATE'])

#-----------------------
# plot 

c1,c2 = st.columns([30,1])
with c1:
    with st.container(border=True):
                
        fig = make_smoothed_curve_plot(df_plot, height = 330)

        # overlay threshold 
        fig.add_hline(y=thld, line_width=2, line_dash="dash", line_color="green")
        
        # overlay epidemic periods 
        for start, end in zip(sta, end):
            fig.add_vrect(x0=start, x1=end, fillcolor="pink", opacity=0.10, line_width=0, layer="below")

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

   
    c01,c02,c03 = st.columns([15,20,20])
    height_all = 320
    with c01:
        with st.container(border=True, height = height_all):
            st.markdown(f""":primary[Summary:] This is a Didactic page where you can
            play with some parameters used in the data-preparation module.
            Only the latest {int(ss.nw_for_demo)} weeks are used to derive the Historical Baseline and shown here.  
            :primary[Automatic Flu Season Detection:] Candidate Flu seasons are automatically detected (transparent rectangles) based on 
            smoothed trace and Threshold using a simple hysteresis method (like a thermostat).
            This is not yet used elsewhere in this app.
            
            """)
    with c02:
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
    with c03:
        with st.container(border=True, height = height_all):
            st.markdown(f""":primary[BL-Normalized Change:] Traces (blue line) are first smoothed with moving regression of degree {ss.ma_degree}
            with bin size of {ss.ma_bin_size} weeks (red line). Trailing moving regression is used here (=right-aligned).
            The average change per week (slope) is then estimated from the latest {int(ss.nw_slo)} weeks via linear regression.
            Finally, the slope is normalized by the historical baseline threshold and expressed as a percentage.  
            :primary[Limitation:] Normalization by the historical baseline improves comparability
            but does not account for differences differences in seasonal patterns and reporting practices across countries and data sources.
            """)



