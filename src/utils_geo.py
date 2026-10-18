#--------------------             
# Author : Serge Zaugg
# Description : functions specific fo geo map pages 
#--------------------

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from datetime import datetime



@st.cache_data
def prepre_for_pages_10_13(df, xvar):
    # df = df.dropna(subset=[xvar])
    df["ISO_WEEKSTARTDATE_str"] = ("" + df["ISO_WEEKSTARTDATE"].dt.strftime("%Y-%m-%d"))
    df = df.sort_values(xvar, ascending = False)
    return(df)

@st.cache_data
def prepre_for_pages_b(df, xvar):
    df = df.dropna(subset=[xvar])
    # df["ISO_WEEKSTARTDATE_str"] = ("" + df["ISO_WEEKSTARTDATE"].dt.strftime("%Y-%m-%d"))
    # df = df.sort_values(xvar, ascending = False)
    return(df)



@st.cache_data
def rm_if_stat_na_per_source(df_dat00, df_dat01, df_dat02, df_max, xvar):
    """ Helper function to prepare data for geo pages """
    df_fresh = pd.DataFrame({
        "SOURCE" : ["Fresh"],
        "SENTINEL":    [df_dat00["COUNTRY"].nunique()],
        "NONSENTINEL": [df_dat01["COUNTRY"].nunique()],
        "NOTDEFINED":  [df_dat02["COUNTRY"].nunique()],
        "MAXCOMBINE":  [pd.NA],
    })

    df_dat00 = prepre_for_pages_b(df_dat00, xvar = xvar)
    df_dat01 = prepre_for_pages_b(df_dat01, xvar = xvar)
    df_dat02 = prepre_for_pages_b(df_dat02, xvar = xvar)
    df_max   = prepre_for_pages_b(df_max,   xvar = xvar)

    df_with_slope = pd.DataFrame({
        "SOURCE" : ["Analysable"],
        "SENTINEL":    [df_dat00["COUNTRY"].nunique()],
        "NONSENTINEL": [df_dat01["COUNTRY"].nunique()],
        "NOTDEFINED":  [df_dat02["COUNTRY"].nunique()],
        "MAXCOMBINE":  [df_max["COUNTRY"].nunique()],
    })
    
    # construct a small info data frame
    dat_info = pd.concat([df_fresh,df_with_slope], axis=0, ignore_index=True).T.reset_index()
    dat_info.columns = ["a", "b", "c"]
    dat_info.columns = dat_info.loc[dat_info["a"] == "SOURCE"].iloc[0]
    dat_info = dat_info.drop(dat_info.index[dat_info["SOURCE"] == "SOURCE"][0]).reset_index(drop=True)

    return df_dat00, df_dat01, df_dat02, df_max, dat_info

