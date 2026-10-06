#--------------------             
# Author : Serge Zaugg
# Description : config file for global-dashboard parameters 
#--------------------

from streamlit import session_state as ss


FLUNET_DATA_URL = "https://xmart-api-public.who.int/FLUMART/VIW_FNT?$format=csv"

FLUNET_META_URL = "https://xmart-api-public.who.int/FLUMART/VIW_FLU_METADATA?$format=csv&$filter=contains(DatasetName,%20%27FluNet%27)"


# define custom colors 
cc = {
    "traces": {
        "basic": "#ffffff",
        "hot": "#fb2d2d",
    },
    "types": {
        "a": "#05fa42",
        "b": "#ce2dfb",
        "o": "#535253",
    },
    "sources": {  
        "sentin": "#8c0463",
        "nonsen": "#3e2dfb",
        "notdef": "#8A7C7C",
        "sumall": "#D1E306",
    },
}
