import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import datetime
from _plotly_utils.colors.qualitative import Vivid
from PIL import Image
import plotly


st.set_page_config(layout="wide")
df = pd.read_csv("tempclean.csv")


st.title("Tablero ContaAyuda")
agree = st.checkbox('Desplegar Dataset Completo')
if agree:
    st.write('Excelente, aquí tienes el dataset')
    st.dataframe(df)



number = st.number_input('Da el número de cliente del que deseas visualizar información', key = int, step=1)
st.write('Cliente Número:', number)
df2 = df[(df['CUSTOMERID'] == number)]

bb = Image.open("bb.png")
st.sidebar.image(bb)

clientes =  df2['RECEIVEDBY'].unique()
cliente = st.sidebar.selectbox("Selecciona el cliente que recibió la factura:",clientes)

with st.container():

    col1, col2 = st.columns(2)
    
    #factura tiempo
    df2['DATE'] = pd.to_datetime(df2['DATE'], format="%Y-%m-%d %H:%M:%S")
    df2 = df2.sort_values(by='DATE')
    fig1 = px.line(df2, x='DATE', y='AMOUNTPAID', color ='PAYMETHODCODE' ,title='Income by years of work',color_discrete_sequence = ['#0031E2', '#ECF435'])
    
    #impuesto tiempo
    fig2 = px.line(df2, x='DATE', y='VATAMT', title='VAT by years of work',color_discrete_sequence = ['blue'])
    
    
    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)

    

    #factura comp
    df2['DATE']=df2['DATE'].astype(str)
    df2['YEAR'] = df2['DATE'].str[:4]
    df2['MONTH'] = df2['DATE'].str[5:7]
    df2['MONTH'] = df2['MONTH'].astype(str).astype(int)
    df2['YEAR'] = df2['YEAR'].astype(str).astype(int)

    years = df2['YEAR'].unique()
    year = st.sidebar.selectbox("Selecciona el año que deseas analizar:",years)


    meses = df2['MONTH'].unique()
    mes = st.sidebar.selectbox("Selecciona el mes:",meses)


    df2 = df2[(df2['YEAR'] == year)]
    df2 = df2[(df2['MONTH'] == mes)]
    print()
    print('Suma de impuestos')
    df3 = df2.groupby('RECEIVEDTAXID')[['VATAMOUNT']].sum()
    #st.dataframe(df3)
    
    print('Promedio del total después de impuestos')
    df4 = df2.groupby('RECEIVEDBY')[['TOTALAFTERTAX']].mean()
    #st.dataframe(df4)
    fig3 = px.pie(df3, values='VATAMOUNT', names=df3.index, title='Suma de impuestos pagados a cada cliente en determinado tiempo',color_discrete_sequence=['#0031E2', '#ECF435', '#1A2448', '#22325E', '#E8EEFF'])    

    tab1, tab2, tab3 = st.tabs(["Mes", "Año", "Trimestre"])
    with tab1:
        st.header("jujujua")
        st.plotly_chart(fig3, use_container_width=True)
   
    #egresos tiempo
    df2['DATE'] = pd.to_datetime(df2['DATE'], format="%Y-%m-%d %H:%M:%S")
    df2 = df2.sort_values(by='DATE')
    fig4 = px.line(df2, x='DATE', y='TOTALAFTERTAX', title='Egresos por cliente a lo largo del tiempo')
    
    #facturas pagadas 
    fig5 = px.histogram(df2, x='PAYMETHODCODE', color = 'PAYMETHODCODE',
                     color_discrete_sequence=['#0031E2', '#ECF435', '#1A2448', '#22325E', '#E8EEFF'])
    
        
    col1, col2, col3 = st.columns(3)
    col1.plotly_chart(fig4, use_container_width=True)
    col2.plotly_chart(fig5, use_container_width=True)
    col3.plotly_chart(fig1, use_container_width=True)


ca = Image.open("ca.png")
st.sidebar.image(ca, use_column_width=True)