##################################
# Import libraries 
import streamlit as st 
import pandas as pd 
import folium 
import altair as alt
import plotly.express as px 
import numpy as np
from folium import Popup
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
    
    
#################################

# Plots

# Map 



# lineplot




# top desabastecido



# Donut chart
def assign_color(idm_value):
    if idm_value >= 90:
        return ['#27AE60', '#12783D']  # Verde
    elif idm_value >= 70:
        return ['#F39C12', '#875A12']  # Amarillo
    elif idm_value >= 50:
        return ['#E67E22', '#B35418']  # Naranja
    else:
        return ['#E74C3C', '#781F16']  # Rojo

def make_donut(idm_value, departamento):
    chart_color = assign_color(idm_value)
    
    source = pd.DataFrame({
        "Topic": ['', departamento],
        "% value": [100 - idm_value, idm_value]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', departamento],
        "% value": [100, 0]
    })
    
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[departamento, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
    
    text = plot.mark_text(align='center', color=chart_color[0], font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(
        text=alt.value(f'{idm_value} %')
    )
    
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[departamento, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
    
    return plot_bg + plot + text

# Calculation IDM by year and department

def calculate_idm_by_depart_year(input_df, input_year, input_depart):
    selected_IDM_depart_year = input_df[(input_df['departamento'] == input_depart) & (input_df['año'] == input_year)]['IDM'].round(0).values
    if len(selected_IDM_depart_year) > 0:
        return selected_IDM_depart_year[0]
    else:
        return None
###################################

# Loading all the data

#IDM col 0
idm_anual_data = pd.read_excel('data/IDM_anual.xlsx')
idm_anual_hosp = pd.read_excel('data/IDM_anual_hospitales.xlsx')
idm_anual_cen = pd.read_excel('data/IDM_anual_centros.xlsx')
idm_anual_pue = pd.read_excel('data/IDM_anual_puestos.xlsx')






####################################
# Dashboard Main Panel
col = st.columns((1.5,4.5,2), gap='medium')

with col[0]:
    st.markdown('#### IDM Anual Departamental')
    
    IDM_anual = calculate_idm_by_depart_year(idm_anual_data,selected_year, selected_depart)
    IDM_anual_hosp = calculate_idm_by_depart_year(idm_anual_hosp, selected_year, selected_depart)
    IDM_anual_cen = calculate_idm_by_depart_year(idm_anual_cen, selected_year, selected_depart)
    IDM_anual_pue = calculate_idm_by_depart_year(idm_anual_pue, selected_year, selected_depart)

    
    
    
    idm_donut_total_chart = make_donut(IDM_anual,selected_depart)
    idm_donut_hosp_chart = make_donut(IDM_anual_hosp,selected_depart)
    idm_donut_cen_chart = make_donut(IDM_anual_cen,selected_depart)
    idm_donut_pue_chart = make_donut(IDM_anual_pue,selected_depart)
    
    
    st.write('IDM Anual Total')
    st.altair_chart(idm_donut_total_chart, use_container_width=True)
    
    st.write('IDM Anual Total - Hospitales')
    st.altair_chart(idm_donut_hosp_chart, use_container_width=True)
    
    st.write('IDM Anual Total - Centros')
    st.altair_chart(idm_donut_cen_chart, use_container_width=True)
    
    st.write('IDM Anual Total - Puestos')
    st.altair_chart(idm_donut_pue_chart, use_container_width=True)