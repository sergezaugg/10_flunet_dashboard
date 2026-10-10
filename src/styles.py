#--------------------             
# Author : Serge Zaugg
# Description : overall page styles (affects all pages) 
#--------------------

import streamlit as st

def apply_global_styles():
    """Apply global CSS styles to the Streamlit app."""

    # Reduce spacing around st.divider() 
    st.markdown("""
        <style>
            div[data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] hr) {
                margin-top: -1.5rem !important;
                margin-bottom: -0.8rem !important;}
        </style>
        """, unsafe_allow_html=True)

    # reduce vertical space between navig and items(content
    st.markdown("""
        <style> 
            [data-testid="stMainBlockContainer"] {padding-top: 4rem; padding-left: 3rem;} 
        </style>
        """, unsafe_allow_html=True)

    # change color of navigation bar background and tabs          
    st.markdown("""
        <style>
        /* Header background */
        .stAppHeader {background-color: #0E1117;}

        /* Default tab background */
        .stAppHeader a {background-color: #2f2f2f !important;}

        /* Hover state */
        .stAppHeader a:hover {background-color: #3b4d63 !important;}

        /* click state */
        .stAppHeader a:active {background-color: #dddddd !important; }

        /* Active page */
        .stAppHeader a[aria-current="page"] {background-color: #fb2d2d !important;}

        </style>
    """, unsafe_allow_html=True)

    # All navigation tabs: same fixed width
    st.markdown("""
    <style>
        .stAppHeader a {
            width: 90px !important;
            min-width: 90px !important;
            max-width: 90px !important;
            box-sizing: border-box !important;
            justify-content: center !important;
            text-align: center !important;
            white-space: nowrap !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        .app-label {
            position: fixed;
            top:  17px;
            left: 55px;
            color: #9CA3AF;
            font-size: 15px;
            z-index: 999999;
            pointer-events: none;
        }
    </style>
    <div class="app-label">FluNet Explorer v0.5.X-β</div>
    """, unsafe_allow_html=True)


    