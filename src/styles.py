


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




    