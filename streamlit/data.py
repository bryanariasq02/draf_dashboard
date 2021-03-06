import pymongo
import pandas as pd
import streamlit as st


def connect():
    URI =  st.secrets["db_username"]
    CLIENT = pymongo.MongoClient(URI)
    DB = CLIENT['3Bios']
    COL = DB['GrupLAC']
    COL2 = DB['SiB']
    # CLIENT.close()
    return COL, COL2

def grupos(COL):
    
    query = {"categoria_gruplac" : "grupos_general"}
    grupos = COL.find(query)
    
    columnas = grupos[0].keys()
    df       = pd.DataFrame(columns = columnas)
    for grupo in grupos:
        df = df.append(grupo, ignore_index=True)
    return df

def investigadores_db(col, id):
    query = {"categoria_gruplac" : "investigadores", "grupo":id}
    investigadores = col.count_documents(query)
    # .explain()['stages']
    return investigadores

def articulos_db(col, id):
    query = {"categoria_gruplac" : "articulos", "grupo":id}
    articulos = col.count_documents(query)
    return articulos

def tg_db(col, id):
    query = {"categoria_gruplac" : "trabajos_dirigidos", "grupo":id}
    tg = col.count_documents(query)
    return tg

def soft_db(col, id):
    query = {"categoria_gruplac" : "softwares", "grupo":id}
    soft = col.count_documents(query)
    return soft


def articulost_db(col, id):
    query = {"categoria_gruplac" : "articulos", "grupo":id}
    project={'ano': 1, '_id': 0}
    articulos = col.find(query, projection=project)
    
    columnas = articulos[0].keys()
    df       = pd.DataFrame(columns = columnas)
    for articulo in articulos:
        df = df.append(articulo, ignore_index=True)
    return df

def SiB_db(col, anio):
    sep = "-"
    year = str(anio)+sep
    filter={'created': {'$regex': year}}
    project={'created': 1, "_id":0}
    sib = col.count_documents(filter=filter,projection=project)
    return sib
    
def total_sib(col):
    sib = col.count_documents({})
    return sib

def type_db(col):
    filter = {}
    project = {'type':1, "_id":0}
    result = col.find(filter=filter, projection=project)
    
    columnas = result[0].keys()
    df       = pd.DataFrame(columns = columnas)
    for res in result:
        df = df.append(res, ignore_index=True)
    return df
    
# col = connect()
# grupos = grupos(col)
# metrics = investigadores_db(col, str(5))