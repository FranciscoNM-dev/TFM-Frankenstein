# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 12:33:01 2024

@author: Cuchu
"""


from scipy import stats
import numpy as np
from scipy.spatial import distance

                           
def funcion_prueba_percentiles(lista_parametros, lista_jugadores, lista_pesos, dataf):
    result=dataf.copy()
    deseados=[]
    for x in range(len(lista_parametros)):
        deseados.append(stats.percentileofscore(dataf[lista_parametros[x]],float(dataf[dataf["Player (Squad)"]==lista_jugadores[x]][lista_parametros[x]].iloc[0]),kind="rank"))
    indices=[]
    for index, row in dataf.iterrows():
        percentiles=[]
        for x in lista_parametros:
            percentiles.append(stats.percentileofscore(dataf[x],float(row[x]),kind="rank"))
        #Distancia euclidea
        indices.append(max(0,round(100-np.linalg.norm((np.asarray(percentiles)-np.asarray(deseados))*np.sqrt(np.asarray(lista_pesos))),2)))
    result['Similarity %'] = indices   
    return result[["Player (Squad)", "Nation", 'Pos. Det.', 'Foot', "Comp.", "Age",
                  "Mins", 'Value']+lista_parametros+['Similarity %']].sort_values("Similarity %",ascending=False)


def funcion_prueba_similitud_coseno(lista_parametros, lista_jugadores, lista_pesos, dataf):
    result=dataf.copy()
    deseados=[]
    for x in range(len(lista_parametros)):
        deseados.append(float(dataf[dataf["Player (Squad)"]==lista_jugadores[x]][lista_parametros[x]]))
    indices=[]
    for index, row in dataf.iterrows():
        valores=list(row[lista_parametros])
        if valores==[0]*len(lista_parametros):
            indices.append(0.0)
        else:
            #Similitud coseno Y NORMALIZACIÓN entre 0 y 100
            indices.append(round((1 - distance.cosine(valores, deseados, lista_pesos)+1)*50,2))        
    result['Similarity %'] = indices   
    return result[["Player (Squad)", "Nation", 'Pos. Det.', 'Foot', "Comp.", "Age",
                  "Mins", 'Value']+lista_parametros+['Similarity %']].sort_values("Similarity %",ascending=False)





def value_transform(value):
    if value[-1]=="€":
        if "mill" in value:
            result=int(value.split(",")[0])*1000000
        else:
            result= int(value.split()[0])*1000
    elif value[0]=="€":
        if value[-1]=="m":
            result=int(value.split(".")[0][1:])*1000000
        else:
            result=int(value.split("k")[0][1:])*1000
    else:
        result=0
    
    return result

