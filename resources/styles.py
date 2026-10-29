#--------------------             
# Author : Serge Zaugg
# Description : overall page styles (affects all pages) 
#--------------------

import streamlit as st

def apply_global_styles():
    """Apply global CSS styles to the Streamlit app."""

    # enforce  min and max accepted screen width via CSS
    st.markdown("""
        <style>
            .block-container {
                max-width: 1500px;
                min-width: 1400px;
                padding-left: 2rem;
                padding-right: 2rem;
                margin-left: auto;
                margin-right: auto;
                box-sizing: border-box;
            }
        </style>
    """, unsafe_allow_html=True)


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
            [data-testid="stMainBlockContainer"] {padding-top: 0rem; padding-left: 1.8rem;} 
        </style>
        """, unsafe_allow_html=True)

    # change color of multilevel-navigation bar background and tabs  
    st.markdown("""
    <style>
    /* Overall header background */
    .stAppHeader {
        background-color: #111111 !important;
    }

    /* Navigation group labels (e.g. Flu Trend, Deep dive) */
    .stAppHeader button {
        background-color: #4f4f4f !important;
        color: white !important;
        border-radius: 5px !important;
    }

    /* Hover over group labels */
    .stAppHeader button:hover {
        background-color: #3b4d63 !important;
    }

    /* Navigation page links inside dropdown groups */
    .stAppHeader a {
        background-color: #4f4f4f !important;
        color: white !important;
    }

    /* Hover over page links */
    .stAppHeader a:hover {
        background-color: #3b4d63 !important;
    }

    /* Active/current page link */
    .stAppHeader a[aria-current="page"] {
        background-color: #fb2d2d !important;
        color: white !important;
    }

    /* Optional: dropdown menu background */
    .stAppHeader [role="menu"] {
        background-color: #222222 !important;
    }
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


    # copyright notice and version at bottom-left
    st.markdown("""
    <style>
        .app-label {
            position: fixed;
            bottom: 15px;
            left: 20px;
            color: #9CA3AF;
            font-size: 15px;
            line-height: 1.4;
            z-index: 999999;
            pointer-events: none;
        }
    </style>
    <div class="app-label">
        v0.10.5-β<br>© 2026 Serge Zaugg
    </div>
    """, unsafe_allow_html=True)


    # reduce height of nav bar 
    st.markdown("""
    <style>
        [data-testid="stHeader"] {
            height: 4rem;
            min-height: 4rem;
            }
    </style>
    """, unsafe_allow_html=True)



