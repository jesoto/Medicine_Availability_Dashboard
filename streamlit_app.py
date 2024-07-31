##################################
# Import libraries 
import streamlit as st 
import pandas as pd 
import folium 
import altair as alt
import plotly.express as px 
import numpy as np

#################################

st.set_page_config(
    page_title='Disponibilidad de medicamentos en establecimientos de salud Peru',
    page_icon="💊",
    layout='wide',
    initial_sidebar_state='expanded'
)

#################################
# Loading data to create the sidebar and filters
filtros = pd.read_excel('data/sidebar.xlsx')

################################
# Sidebar
with st.sidebar:
    st.title('🏥💊 Disponibilidad de Medicamentos - Peru')
    
    year_list = [2019, 2020, 2021, 2022, 2023, 2024]
    
    selected_year = st.selectbox('Selecciona un año', year_list, index=len(year_list)-1)
    
    depart_list = ['AMAZONAS', 'CAJAMARCA', 'AREQUIPA', 'AYACUCHO', 'APURIMAC',
       'ANCASH', 'HUANUCO', 'ICA', 'HUANCAVELICA', 'CUSCO', 'CALLAO',
       'UCAYALI', 'TUMBES', 'SANMARTIN', 'TACNA', 'PUNO', 'PIURA',
       'PASCO', 'LORETO', 'MOQUEGUA', 'MADREDEDIOS', 'LIMA', 'LALIBERTAD',
       'JUNIN', 'LAMBAYEQUE']
    
    selected_depart = st.selectbox('Selecciona el departamento', depart_list)