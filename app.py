#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# run locally : streamlit run stmain.py
#--------------------

import pandas as pd
import streamlit as st
from streamlit import session_state as ss
from src.utils_preproc import download_flunet_data, preprocess_flunet_data, get_latest_date_per_group
from src.utils_preproc import compute_recent_slope, compute_recent_level, combine_bl_and_slope_summaries
from resources.styles import apply_global_styles

#------------------------------
# prepare app 
st.set_page_config(layout = "wide", initial_sidebar_state = "expanded", page_title="Global Influenza Explorer", page_icon='pics/z_logo_red.png')
apply_global_styles() # apply custom CSS styles 
st.logo(image='pics/z_logo_red.png', size="large", link="https://github.com/sergezaugg")
pd.set_option('display.max_rows', 500)

#------------------------------
# prepare data once on session startup 
# Functions cached across sessions for the lifetime of the running app.
# Cache of download_flunet_data() cleared on 'refresh', triggering re-run of data prep
if "df_data" not in ss:

    #------------------------------
    # initialize session state (constant values)
    ss.max_countries_in_plots = 20
    ss.nw_global = 6 # weeks from ref to be used for stats 
    ss.top_n = 5 # how much to show in 'top' pages
    ss.nw_for_demo = 52*4
    # (1) advanced pre-processing (slope / percent change)
    ss.nw_ma = 20 # 15
    ss.ma_bin_size = 3 # 4
    ss.ma_degree = 1
    ss.nw_slo = ss.nw_global 
    # (2) advanced pre-processing (burden / above Baseline)
    ss.time_range_basli = 52*4
    ss.quantile_val = 0.50 # 0.65 # originally 0.65
    ss.mad_factor = 0.5
    ss.tol_thld = 10 # 10
    ss.na_thld = 0.40 # tolerance for prop NAs 
    ss.time_range_trace = 24
    ss.time_range_stats = ss.nw_global

    #------------------------------
    # download and pre-process (do once)
    df_dat, ss.ts_download, ss.sha256_download, ss.dl_status = download_flunet_data(3425)
    ss.ts_today = ss.ts_download
    ss.df_data = preprocess_flunet_data(df = df_dat)

    # initialize data dependent objects in ss
    ss.df_latest_data = get_latest_date_per_group(ss.df_data, ts_today = ss.ts_today)

    # remove all data that is too old already here 
    mask = ss.df_latest_data[['COUNTRY', 'ORIGIN_SOURCE', 'days_since']]
    mask = mask[mask['days_since'] <= (ss.nw_global)*7] # 
    ss.df_data = ss.df_data.merge(mask, on=["COUNTRY", "ORIGIN_SOURCE"], how="right")

    #------------------------------
    # advanced pre-processing

    # (1) advanced pre-processing (Slope)
    obj = compute_recent_slope(ss.df_data, ss.nw_ma, ss.ma_bin_size, ss.ma_degree, ss.nw_slo, ss.ts_today)
    ss.df_trace_ma, ss.trace_x_range_ma, dfma_temp, ss.stats_x_range_ma = obj # unwrap

    # (2) advanced pre-processing (Flu Burden above Baseline)
    obj = compute_recent_level(ss.df_data, ss.time_range_basli, ss.quantile_val, ss.tol_thld, ss.na_thld, ss.time_range_trace, ss.time_range_stats, ss.ts_today)
    ss.df_trace_bl, ss.trace_x_range_bl, dfbl_temp, ss.stats_x_range_bl = obj # unwrap

    # (3) combine bl and slope summaries
    ss.df_metri_merged = combine_bl_and_slope_summaries(dfma_temp, dfbl_temp)

    # (4) derive new indicator columns for 'COMBINED' = 'MAXCOMBINE'
    ss.df_metri_merged["rel_burden_is_max"] = (ss.df_metri_merged["REL_BURDEN"].eq(
        ss.df_metri_merged.groupby("COUNTRY")["REL_BURDEN"].transform("max")))

    ss.df_metri_merged["perc_change_is_max"] = (ss.df_metri_merged["PERC_CHANGE"].eq(
        ss.df_metri_merged.groupby("COUNTRY")["PERC_CHANGE"].transform("max")))

    #------------------------------
    # put data-dependent values into ss
    if "ts_latest_data" not in ss:
        ss.ts_latest_data   = ss.df_data['ISO_WEEKSTARTDATE'].max()
    if "date_range_dt" not in ss:
        ss.date_range_dt    = [ss.df_data["ISO_WEEKSTARTDATE"].min().date(), ss.df_data["ISO_WEEKSTARTDATE"].max().date()]
    if "top3_weeks" not in ss:
        ss.top3_weeks       =  ss.df_data["ISO_WEEKSTARTDATE"].drop_duplicates().sort_values(ascending=False).head(3)
    if "delays_days" not in ss:
        ss.delays_days      = ((ss.ts_today - ss.top3_weeks).dt.days).tolist()
    if "WHOREGION_levels" not in ss:
        ss.WHOREGION_levels = ss.df_data["WHOREGION"].unique()
    if "FLUSEASON_levels" not in ss:
        ss.FLUSEASON_levels = ss.df_data["FLUSEASON"].unique()
    if "ITZ_levels" not in ss:
        ss.ITZ_levels       = ss.df_data["ITZ"].unique().tolist()
    if "ALL_COUNTRIES" not in ss:
        ss.ALL_COUNTRIES    = ss.df_data['COUNTRY'].unique()

    #------------------------------
    # set widget defaults here if really needed here!
    ss.setdefault("k_who_06", ['CHE', 'ESP', 'FRA'])

# Protect widget keys from being deleted (for multi-page consistency across clicks)
# official docu Option 4: Interrupt the widget clean-up process
for key in list(st.session_state.keys()):
    st.session_state[key] = st.session_state[key]

# debug
# st.write(ss.df_metri_merged)
# st.write(ss.df_trace_bl)

#------------------------------
# build app's visible  frontend
with st.sidebar:
    st.markdown(f"""## :primary[**Global Influenza Explorer (BETA)**] """)
    st.markdown("""
    <div style="line-height: 1.3; margin-bottom: 0.9em;">
        <div>Data Hash: <code style="color:orange">{}</code></div>
        <div>Downloaded: <code style="color:orange">{}</code></div>
        <div>Reference date: <code style="color:orange">{}</code></div>
    </div>
    """.format(
        ss.sha256_download[:12], 
        ss.ts_download.strftime("%Y-%m-%d %H:%M"), 
        ss.ts_today.strftime("%Y-%m-%d")),
    unsafe_allow_html=True)
    st.caption(ss.dl_status)
    st.divider()
 
# make navigation
p01a = st.Page("pages/page_age1.py", title="Map")
p01b = st.Page("pages/page_age2.py", title="Tabular")
p02 = st.Page("pages/page_slop_metric_c.py", title="Trend", default=True)
p03 = st.Page("pages/page_burd_metric_c.py", title="Burden")
p04 = st.Page("pages/page_slop_geo.py", title="Trend")
p05 = st.Page("pages/page_burd_geo.py", title="Burden")
p06 = st.Page("pages/page_traces.py", title="History")
p07 = st.Page("pages/page_ab_type.py", title="Type A vs B")
p08a = st.Page("pages/page_play.py", title="Interactive illustration")
p08b = st.Page("pages/page_method.py", title="Methods")
p10 = st.Page("pages/page_info.py", title="Info")
p11 = st.Page("pages/page_disclaimer.py", title="Disclaimer")
p12 = st.Page("pages/page_refresh.py", title="Maintenance")
p13 = st.Page("pages/page_bl_thld.py", title="Historic-BL-Threshold")

pages = {
    "Data Age":     [p01a, p01b],
    "Metrics Rank": [p02, p03],
    "Metrics Map":  [p04, p05],
    "Explore":      [p06, p07],
    "Methods":      [p08b, p13, p08a],
    "About":        [p10],
    "More":         [p12],
    "Disclaimer":   [p11],
}

pg = st.navigation(pages, position="top")

pg.run()

