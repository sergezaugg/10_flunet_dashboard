#--------------------             
# Author : Serge Zaugg
# Description : functions - streamlit chunks
#--------------------

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
# from config import FLUNET_DATA_URL, FLUNET_META_URL
# import requests
# from io import BytesIO
# from datetime import datetime
# import hashlib

@st.cache_data() # filter_data
def filter_data_region(df, who_regions = ['EUR'], fse_regions = ['aa'], itz_regions = ['bb']):
    """
    aaaa 
    """
    df = df.copy()
    # select based on WHOREGION
    df = df[df["WHOREGION"].isin(who_regions)]
    # select based on FLUSEASON
    df = df[df["FLUSEASON"].isin(fse_regions)]
    # select based on ITZ
    df = df[df["ITZ"].isin(itz_regions)]
    # check
    n_countries = pd.Series(df["COUNTRY"].unique()).value_counts().shape
    return(df, n_countries) 

@st.cache_data()
def filter_several_countries(df, countries):
    df = df[df["COUNTRY"].isin(countries)]
    n_countries = pd.Series(df["COUNTRY"].unique()).value_counts().shape
    return df, n_countries

@st.cache_data()
def filter_a_country(df, c):
    df = df[df["COUNTRY"] == c]
    return(df)

@st.cache_data()
def filter_a_data_source(df, c):
    df = df[df["ORIGIN_SOURCE"] == c]
    return(df)

@st.cache_data
def select_top_n_highest_slope(df, n, sorting_var): 
    """ select top-n with highest slope in df """
    df = df.dropna(subset=[sorting_var])
    df = df.sort_values(sorting_var, ascending=False)
    df = df.iloc[0:n].reset_index(drop=True) 
    return df





@st.cache_data
def prepre_for_pages_10_13(df, xvar):
    df["ISO_WEEKSTARTDATE_str"] = ("" + df["ISO_WEEKSTARTDATE"].dt.strftime("%Y-%m-%d"))
    df = df.sort_values(xvar, ascending = False)
    return(df)

# @st.cache_data
def prepre_for_pages_b(df, xvar):
    df = df.dropna(subset=[xvar])
    return(df)

@st.cache_data
def rm_if_stat_na_per_source(df_dat00, df_dat01, df_dat02, df_dat03, xvar):
    """ Helper function to prepare data for geo pages """
    df_fresh = pd.DataFrame({
        "SOURCE" : ["Fresh"],
        "SENTINEL":    [df_dat00["COUNTRY"].nunique()],
        "NONSENTINEL": [df_dat01["COUNTRY"].nunique()],
        "NOTDEFINED":  [df_dat02["COUNTRY"].nunique()],
    })

    df_dat00 = prepre_for_pages_b(df_dat00, xvar = xvar)
    df_dat01 = prepre_for_pages_b(df_dat01, xvar = xvar)
    df_dat02 = prepre_for_pages_b(df_dat02, xvar = xvar)
    df_dat03 = prepre_for_pages_b(df_dat03, xvar = xvar)


    df_with_slope = pd.DataFrame({
        "SOURCE" : ["Analysable"],
        "SENTINEL":    [df_dat00["COUNTRY"].nunique()],
        "NONSENTINEL": [df_dat01["COUNTRY"].nunique()],
        "NOTDEFINED":  [df_dat02["COUNTRY"].nunique()],
    })
    
    # construct a small info data frame
    dat_info = pd.concat([df_fresh,df_with_slope], axis=0, ignore_index=True).T.reset_index()
    dat_info.columns = ["a", "b", "c"]
    dat_info.columns = dat_info.loc[dat_info["a"] == "SOURCE"].iloc[0]
    dat_info = dat_info.drop(dat_info.index[dat_info["SOURCE"] == "SOURCE"][0]).reset_index(drop=True)

    return df_dat00, df_dat01, df_dat02, df_dat03, dat_info










@st.cache_data
def det_regions(x, t):
    """
    Detect threshold regions in a Series using hysteresis.
    Parameters
    x : (pd.Series) Continuous input values.
    t : (float) Threshold value.
    Returns
    (pd.Series) Boolean Series with the same index as x.
    """
    lower = t*0.95
    upper = t*1.05
    state = False
    regions = []
    for value in x:
        if not state and value > upper:
            state = True
        elif state and value < lower:
            state = False
        regions.append(state)
    regions = pd.Series(regions, index=x.index)
    return regions

@st.cache_data
def get_start_stop_of_region(regions, time):
    """
    Identify onset and offset of contiguous True regions.
    ingests output of det_regions()
    Parameters
    regions : (pd.Series) Boolean Series indicating the regions.
    time : (pd.Series) Time values corresponding to regions.
    Returns
    (tuple of pd.Series) Two Series containing the start and end times of each region.
    """
    starts = regions & ~regions.shift(fill_value=False)
    ends = regions & ~regions.shift(-1, fill_value=False)
    sta = time[starts]
    end = time[ends]
    return(sta,end)


