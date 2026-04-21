# -*- coding: utf-8 -*-
"""
Created on Mon May 27 17:40:29 2024

@author: Cuchu
"""


#Imports
import requests
#from bs4 import BeautifulSoup
import pandas as pd
#import time
#from collections import Counter


#Urls de las páginas con todas las stats de las 5 grandes ligas, esta temporada
listaUrls= ["https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats",
            "https://fbref.com/en/comps/Big5/keepers/players/Big-5-European-Leagues-Stats",
            "https://fbref.com/en/comps/Big5/keepersadv/players/Big-5-European-Leagues-Stats",
            "https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats",
            "https://fbref.com/en/comps/Big5/passing/players/Big-5-European-Leagues-Stats",
            "https://fbref.com/en/comps/Big5/passing_types/players/Big-5-European-Leagues-Stats",
            "https://fbref.com/en/comps/Big5/gca/players/Big-5-European-Leagues-Stats",
            "https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats",
            "https://fbref.com/en/comps/Big5/possession/players/Big-5-European-Leagues-Stats",
            "https://fbref.com/en/comps/Big5/misc/players/Big-5-European-Leagues-Stats"]
print("Tengo las urls, voy a sacar las tablas")


#Sacamos una lista con todos los DataFrames
listaDfs=[pd.read_html(
    requests.get(x).text.replace('<!--','').replace('-->',''))[1] for x in listaUrls]

print("Tengo la lista de dfs. Voy limpiando")
##reqs.headers["Retry-After"] ESPERAR ESOS SEGUNDOS si falla la query

#Prelimpieza

#Columnas comunes en todos los Dataframes de listaDfs
comunes=['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born',
         '90s', 'Matches']


for x in range(len(listaDfs)):
    print("Haciendo flatten a los nombres de las columnas")
    listaDfs[x].columns=listaDfs[x].columns.map('|'.join).str.strip('|')
    print("Dejando bonitos los nombres de las columnas")
    listaDfs[x].columns=[y.split("|")[1] for y in listaDfs[x].columns]
    print("Añadiendo Nombre + Squad a cada df como Primary key para join")
    listaDfs[x]["Player (Squad)"]= listaDfs[x]["Player"] + " (" + listaDfs[x]["Squad"] + ")" 
    mid = listaDfs[x]["Player (Squad)"]
    listaDfs[x].drop(labels=["Player (Squad)"], axis=1,inplace = True)
    listaDfs[x].insert(0, "Player (Squad)", mid)
    print("Quitando las filas 'intermedias'")
    listaDfs[x]= listaDfs[x][listaDfs[x]['Rk']!="Rk"]
    print("Quitando columnas comunes en todos los df")
    if x==0:
        listaDfs[x]=listaDfs[x].drop(["Rk","Matches"],axis=1)
    else:
        listaDfs[x]=listaDfs[x].drop(comunes,axis=1)
    print("Haciendo último rename para saber a qué tabla pertenece cada columna")
    listaDfs[x].columns=[listaUrls[x].split("/")[6]+y  if y != "Player (Squad)" else "Player (Squad)" for y in listaDfs[x].columns]

print("Juntamos todos los dfs")
todo=listaDfs[0]
for x in range(1,len(listaDfs)):
    todo=pd.merge(todo, listaDfs[x], on='Player (Squad)', how='outer')

#Filtramos para tener los jugadores con más de 5 "90s"
todo=todo[todo["stats90s"].astype(float)>5]

#Guardamos en csv
todo.to_csv("fbref.csv", index=False)
















