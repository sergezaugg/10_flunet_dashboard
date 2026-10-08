#--------------------             
# Author : Serge Zaugg
# Description : config file for global-dashboard parameters 
#--------------------

from streamlit import session_state as ss


FLUNET_DATA_URL = "https://xmart-api-public.who.int/FLUMART/VIW_FNT?$format=csv"
# FLUNET_DATA_URL = "https://xmart-api-public.who.int/blablabal=csv"

FLUNET_META_URL = "https://xmart-api-public.who.int/FLUMART/VIW_FLU_METADATA?$format=csv&$filter=contains(DatasetName,%20%27FluNet%27)"


# define custom colors 
cc = {
    "traces": {
        "basic": "#d2f4f9",
        "hot": "#fb2d2d",
    },
    "types": {
        "a": "#05fa42",
        "b": "#ce2dfb",
        "o": "#535253",
    },
    "sources": {  
        "sentin": "#8c0463",
        "nonsen": "#2d1ddb",
        "notdef": "#0E8F48",
        "sumall": "#E0D503",
    },
     "recency": {  
            "a": "#00ff55",
            "b": "#e7f709",
            "c": "#fb6d08",
            "d": "#ff0808",
        },
}
