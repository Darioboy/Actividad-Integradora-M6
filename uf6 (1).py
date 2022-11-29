import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import datetime
from _plotly_utils.colors.qualitative import Vivid

df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")
df = df.drop(['HSOC Zones as of 2018-06-05', 'OWED Public Spaces','Central Market/Tenderloin Boundary Polygon - Updated','Parks Alliance CPSI (27+TL sites)', 'ESNCAG - Boundary File'], axis=1)



st.title("Reportes de Incidentes de la policia de San Francisco")
st.write("El dataset completo con todos los reportes de la policía  de San Francisco desde el año 2018 hasta el año 2020")
agree = st.checkbox('Desplegar Dataset Completo')
if agree:
    st.write('Excelente, aquí tienes el dataset')
    st.dataframe(df)

fig = px.histogram(df, x='Incident Day of Week', color = 'Incident Year', title="Incidentes por día de la semana" )
st.plotly_chart(fig, use_container_width=True)  
    
df18 = df[(df['Incident Year'] == 2018)]
df19 = df[(df['Incident Year'] == 2019)]
df20 = df[(df['Incident Year'] == 2020)]

tab1, tab2, tab3 = st.tabs(["2018", "2019", "2020"])
with tab1:
    mapita18=pd.DataFrame()
    mapita18["lat"]=df18['Latitude']
    mapita18["lon"]=df18['Longitude']
    st.header("Crímenes reportados 2018")
    mapita18.dropna(inplace= True)
    st.map(mapita18)
    
with tab2:
    mapita19=pd.DataFrame()
    mapita19["lat"]=df19['Latitude']
    mapita19["lon"]=df19['Longitude']
    st.header("Crímenes reportados 2019")
    mapita19.dropna(inplace= True)
    st.map(mapita19)
    
with tab3:
    mapita20=pd.DataFrame()
    mapita20["lat"]=df20['Latitude']
    mapita20["lon"]=df20['Longitude']
    st.header("Crímenes reportados 2020")
    mapita20.dropna(inplace= True)
    st.map(mapita20)






tab4, tab5, tab6 = st.tabs(["2018", "2019", "2020"])
with tab4:
    fig = px.histogram(df18, y='Incident Category', color = 'Report Type Description', title="Categoría de incidente"  )
    st.plotly_chart(fig, use_container_width=True)  
    
with tab5:
    fig = px.histogram(df19, y='Incident Category', color = 'Report Type Description', title="Categoría de incidente" )
    st.plotly_chart(fig, use_container_width=True)  
    
    
with tab6:
    fig = px.histogram(df20, y='Incident Category', color = 'Report Type Description' , title="Categoría de incidente" )
    st.plotly_chart(fig, use_container_width=True)  
    
category1 = df['Incident Category'].unique()
category = st.selectbox("Selecciona la categoría de crimen del que deseas ver la resolución:",category1)

categoria=df[(df['Incident Category'] == category)]
fig = px.histogram(categoria, x='Resolution', color = 'Incident Year', title="Resolución del crimen por año en base a la categoría seleccionada")
st.plotly_chart(fig, use_container_width=True)  


district = df['Police District'].unique()
district = st.selectbox("Selecciona el distrito de San Francisco del que deseas visualizar en el mapa la criminalidad:",district)
discrimes=df[(df['Police District'] == district)]

dc=pd.DataFrame()
dc["lat"]=discrimes['Latitude']
dc["lon"]=discrimes['Longitude']
st.header("Crímenes por distrito")
dc.dropna(inplace= True)
st.map(dc)



