import streamlit as st
import os
import pandas as pd
import geopandas as gpd
import plotly.express as px
from PIL import Image
import time


#------------------------ Objetives and description ------------------------#

st.set_page_config(page_title="Objetives", page_icon="🎯",
                   layout="wide", initial_sidebar_state="expanded",
                   menu_items=None)

descripcion_proyecto = ("""
<div style="text-align: justify; line-height: 1.5; padding-bottom: 12px;">
  <span style="font-size: 17px;">
    <br>
    El conjunto de datos con el que estaremos trabajando consiste en las visitas a los clientes</strong>.
    <br>
    <br>
</span>
</div>
<br>
<br>
""")

desire_dir = "CUSTOMERSEARCH/DATA/DATOS.csv"

os.chdir(desire_dir)
current_dir = os.getcwd()
path = os.path.join(current_dir, "DATA/DATOS.csv")

@st.cache_data(show_spinner=True)
def read_file(path):
   df = pd.read_csv(path)
   return df

Datos = read_file(path)

def mapa_de_clientes():
        geo_clientes = gpd.GeoDataFrame(Datos,
                                geometry = gpd.points_from_xy(Datos.Longitud, Datos.Latitud),
                                crs=3857)
        geo_clientes.rename(columns={"Longitud": "lon",
                                "Latitud": "lat"}, inplace=True)

        colores = {'ABSA S.A': 'lightblue'}

        fig = px.scatter_mapbox(geo_clientes, lat='lat', lon='lon',
                                hover_name='Cliente', zoom=11,
                                mapbox_style='carto-positron',
                                color='Cliente', color_discrete_map=colores,
                                width=500, height=500,
                                center={'lat': -34.60205, 'lon': -58.43135})
        fig.update_layout(font_color='black',
                        hoverlabel_bordercolor='black',
                        hoverlabel_bgcolor = 'white',
                        legend_bgcolor="#FDFFCD",
                        legend_borderwidth=1)

        return fig

st.header("🗒️Breve description")
st.write(descripcion_proyecto, unsafe_allow_html=True)


st.header("🎯Objetivos")
c1, c2 = st.columns(2)
with c1:
    ABSA_Image = Image.open("Grundfos Customer Images/Bomba_Flygt_Absa.png")
    st.image(ABSA_Image, width=110, use_column_width=False)
with c2:
        st.plotly_chart(mapa_de_clientes(), use_container_width=True)
