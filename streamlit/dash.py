import streamlit as st
import pymongo
import pandas as pd
import plotly.graph_objects as go

from data import *

st.set_page_config(
    page_title="Dashboard 3BIO",
    page_icon="📈",
    layout="wide",
)

st.title ("3 BIO: Analítica de datos")
st.markdown('## En el presente dashboard se podrá hacer pruebas a la base de datos del GrupLAC, así mismo para cuantificar el tiempo de ejecución para posibles consutas para el dashboard')

st.header('Seleccione un grupo de investigación')
@st.experimental_memo
def grupos_st(_COL):
    group = grupos(COL)
    return group
COL = connect()
grupos_id = grupos_st(COL)
grupos_id.drop(['_id'], axis=1, inplace = True)
st.dataframe(grupos_id)

option = st.selectbox('Seleccione el ID del grupo para consultar:', grupos_id['grupo'])

@st.experimental_memo
def investigadores_st(_COL, id):
    investigadores = investigadores_db(COL, id)
    return investigadores

investigador = investigadores_st(COL, str(option))

@st.experimental_memo
def articulos_st(_COL, id):
    articulos = articulos_db(COL, id)
    return articulos

@st.experimental_memo
def tg_st(_COL, id):
    tg = tg_db(COL, id)
    return tg

@st.experimental_memo
def soft_st(_COL, id):
    soft = soft_db(COL, id)
    return soft
# st.metric(label="Base de datos", value="1")

row1_1, row1_2 = st.columns((2, 3))

with row1_1:
    st.subheader('Investigadores')
    fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = investigador,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Investigadores"}))

    st.plotly_chart(fig, use_container_width=True)

with row1_2:
      articulos = articulos_st(COL, int(option))
      st.subheader('Artículos')
      st.metric(label="Total artículos", value=articulos)
      
      tg = tg_st(COL, int(option))
      st.subheader('Trabajos dirigidos')
      st.metric(label="Total trabajos dirigidos", value=tg)
      
      soft = soft_st(COL, int(option))
      st.subheader('Software')
      st.metric(label="Total software", value=soft)


@st.experimental_memo
def articulost_st(_COL, id):
    articulost = articulost_db(COL, id)
    return articulost

art = articulost_st(COL, int(option))
art['ano'] = art['ano'].astype(int)
art = art[art['ano'] >= 2016].value_counts().reset_index(name='Counts')
art = art.sort_values(['ano','Counts'], ascending=False)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=art['ano'], y = art['Counts'], fill='tozeroy',
                    mode='none'))
st.header('Producción de artículos desde 2016')
st.plotly_chart(fig2, use_container_width=True)
