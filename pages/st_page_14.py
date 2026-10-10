#--------------------             
# Author : Serge Zaugg
# Description : assess baseline values
#--------------------

import streamlit as st
from streamlit import session_state as ss
from src.utils import filter_data_region, filter_several_countries
from src.utils_plots import make_facet_line_plot
import plotly.express as px


# ss.df_data.head()
# ss.df_data.columns
# ss.dfbl_temp.head()

df01 = ss.dfbl_temp[[ 'COUNTRY', 'ORIGIN_SOURCE', 'INF_ALL_BASELINE']]
df02 = ss.df_data[['FLUSEASON', 'COUNTRY', 'ORIGIN_SOURCE', 'ISO_WEEKSTARTDATE', 'INF_ALL']]

df01 = df01[df01['ORIGIN_SOURCE'] == 'SENTINEL']

df02['FLUSEASON'].unique()

df02 = df02[df02['ORIGIN_SOURCE'] == 'SENTINEL']
df02 = df02[df02['FLUSEASON'] == 'NH'] # ['YR', 'NH', 'SH']

# df01.head()
# df02.head()

df = df02.merge(
    df01,
    on=["COUNTRY", "ORIGIN_SOURCE"],
    how="left"
)

df.shape

# df.head()
df = df.head(20000)

df_long = df.melt(
    id_vars=["COUNTRY", "ORIGIN_SOURCE", "ISO_WEEKSTARTDATE"],
    value_vars=["INF_ALL", "INF_ALL_BASELINE"],
    var_name="TYPE",
    value_name="VALUE",
)

# df_long.head()

# px.scatter(df['INF_ALL_BASELINE']).show()

fig = px.line(
    df_long,
    x="ISO_WEEKSTARTDATE",
    y="VALUE",
    color = "TYPE",
    facet_col="COUNTRY",
    facet_col_wrap=4,
    height=2000,
    facet_row_spacing=0.030,
)

# fig.update_yaxes(type="log")

fig.update_yaxes(matches=None)
fig.update_yaxes(range=[0, None])
fig.update_xaxes(showline = True, linewidth=1.8, mirror=True, showticklabels=True, ticks="inside",)
fig.update_yaxes(showline = True, linewidth=1.8, mirror=True)

# fig.show()
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

