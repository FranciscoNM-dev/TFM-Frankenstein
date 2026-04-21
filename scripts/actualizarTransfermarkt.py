# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 00:52:27 2024

@author: Cuchu
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from collections import Counter #Usado para limpieza de los datos

#URL fbref
url = 'https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats'

#Encabezado para simular un navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

#Solicitud HTTP
response = requests.get(url, headers=headers)


if response.status_code == 200: #Éxito
    #Sacamos el html
    html_content = response.text

    #Parseamos html
    soup = BeautifulSoup(html_content, 'html.parser')

    data = []
    
    #Sacamos las filas de la tabla de jugadores
    player_rows = soup.find_all('tr')
    
    #Cogemos solo los jugadores con más de 5 "90s"
    for row in player_rows:
        player_cell = row.find('td', class_='left', attrs={'data-stat': 'player'})
        if player_cell:
            player_name = player_cell.find('a').text.strip()  #Nombre del jugador
            player_url = "https://fbref.com" + player_cell.find('a')['href']  #Link de fbref del jugador
            minutes_90s_cell = row.find('td', class_='right')  #Valor de 90s
            if minutes_90s_cell:
                try:
                    minutes_90s = float(minutes_90s_cell.text.strip()) 
                    if minutes_90s > 5:
                        team_cell = row.find_all('td')[3]  #Celda del equipo
                        team_name = team_cell.find('a').text.strip()  #Nombre del equipo
                        data.append([player_name, minutes_90s, team_name, player_url])
                except ValueError:
                    print(f"Error al convertir '90s' a punto flotante para {player_name}")
    
    #Creamos un dataframe con los datos que tenemos
    df = pd.DataFrame(data, columns=['Player', '90s', 'Team', 'fbref URL'])
    df["Player (Squad)"]=df["Player"]+" ("+df["Team"]+")"
    
    
#----------------- AHORA A TRANSFERMARKT----------------------------
#Creamos las queries a partir de la estructura de query de Transfermarkt y el nombre del jugador
queries=["https://www.transfermarkt.es/schnellsuche/ergebnis/schnellsuche?query="+x.replace(" ","+") for x in df["Player"]]

precios=[]
exact_position=[]
good_foot=[]
fotoEquipo=[] #No usado. Quizá para futuras mejoras
fotoEquipo_HD=[] #No usado. Quizá para futuras mejoras
fotoJugador=[] #No usado. Quizá para futuras mejoras
transferMarkturl=[]
queriesQueNo=[] #Para las búsquedas que dan resultado vacío
supuestos=[] #Para las queries en las que he supuesto el valor
inputeadas=[] #Para las queries para las que he pedido el input
#A los que no he encontrado un precio cercano les he puesto -

#Para cada query hacemos la solicitud html
for i in range(len(queries)):
    print (df["Player"][i])
    print(queries[i])
    responseQuery = requests.get(queries[i], headers=headers)
    if responseQuery.status_code == 200:

        try:
            html_contentQuery = responseQuery.text #Contenido html
            soupQuery = BeautifulSoup(html_contentQuery, 'html.parser') #Parse
            players_table = soupQuery.find('table', class_='items') #Tabla de jugadores
            player_rows = players_table.find_all('tr', class_=['odd', 'even']) #Filas de la tabla
            if len(player_rows)==1: #Si solo hay un resultado, asumiré que él es el jugador que buscamos
                precios.append(player_rows[0].find('td', class_="rechts hauptlink").text.strip()) #Precio
                playerTransferMarktUrl="https://www.transfermarkt.co.uk"+player_rows[0].find_all('a')[1].get('href') #Url de Transfermarkt
                transferMarkturl.append(playerTransferMarktUrl)
                responseQueryPlayer = requests.get(playerTransferMarktUrl, headers=headers) #Nos metemos al perfil Transfermarkt del jugador
                html_contentQueryPlayer = responseQueryPlayer.text #Contenido html
                soupQueryPlayer = BeautifulSoup(html_contentQueryPlayer, 'html.parser') #Parse
                tablitaPerfil=[z.text.strip() for z in soupQueryPlayer.find_all('span', class_='info-table__content info-table__content--regular')]
                if "Position:" in tablitaPerfil: #Posición exacta según Transfermarkt
                    exact_position.append(soupQueryPlayer.find_all('span', class_='info-table__content info-table__content--bold')[tablitaPerfil.index("Position:")].text.strip()) 
                else:
                    print("No tiene posición exacta Transfermarkt")
                    exact_position.append("Revisa luego")
                if "Foot:" in tablitaPerfil: #Pie bueno según Transfermarkt
                    good_foot.append(soupQueryPlayer.find_all('span', class_='info-table__content info-table__content--bold')[tablitaPerfil.index("Foot:")].text.strip())
                else:
                    print("No tiene pie bueno Transfermarkt")
                    good_foot.append("Revisa luego")
                
                #NO USADOS, QUIZÁ PARA FUTURAS MEJORAS
                #photoset=soupQueryPlayer.find("a", class_="data-header__box__club-link").find("img").get("srcset").replace('\n', '')
                #fotoEquipo.append(photoset.split(",")[0].split()[0])
                #fotoEquipo_HD.append(photoset.split(",")[1].split()[0])
                #fotoJugador.append(soupQueryPlayer.find("div", class_="modal-trigger").find("img").get("src"))
            else: #Si no solo hay un resultado en la tabla de Transfermarkt, o no hay ningún resultado
                print(df["Player"][i], df["Team"][i])
                if player_rows[0].find('img', class_='bilderrahmen-fixed')['title']==df["Player"][i]: #Si coincide el nombre buscado con el primer resultado de la tabla
                    #En ese caso también suponemos que hemos dado con el jugador bueno (Se manejan errores luego)
                    precios.append(player_rows[0].find('td', class_="rechts hauptlink").text.strip())
                    playerTransferMarktUrl="https://www.transfermarkt.co.uk"+player_rows[0].find_all('a')[1].get('href')
                    transferMarkturl.append(playerTransferMarktUrl)
                    responseQueryPlayer = requests.get(playerTransferMarktUrl, headers=headers)
                    html_contentQueryPlayer = responseQueryPlayer.text
                    soupQueryPlayer = BeautifulSoup(html_contentQueryPlayer, 'html.parser')
                    tablitaPerfil=[z.text.strip() for z in soupQueryPlayer.find_all('span', class_='info-table__content info-table__content--regular')]
                    if "Position:" in tablitaPerfil:
                        exact_position.append(soupQueryPlayer.find_all('span', class_='info-table__content info-table__content--bold')[tablitaPerfil.index("Position:")].text.strip())
                    else:
                        print("No tiene posición exacta Transfermarkt")
                        exact_position.append("Revisa luego")
                    if "Foot:" in tablitaPerfil:
                        good_foot.append(soupQueryPlayer.find_all('span', class_='info-table__content info-table__content--bold')[tablitaPerfil.index("Foot:")].text.strip())
                    else:
                        print("No tiene pie bueno Transfermarkt")
                        good_foot.append("Revisa luego")
                    #photoset=soupQueryPlayer.find("a", class_="data-header__box__club-link").find("img").get("srcset").replace('\n', '')
                    #fotoEquipo.append(photoset.split(",")[0].split()[0])
                    #fotoEquipo_HD.append(photoset.split(",")[1].split()[0])
                    #fotoJugador.append(soupQueryPlayer.find("div", class_="modal-trigger").find("img").get("src"))
                    supuestos.append(queries[i])
                    print("He supuesto que vale " + player_rows[0].find('td', class_="rechts hauptlink").text.strip())
                else: #Si no coincide el nombre exactamente crearemos una tabla para elegir nosotros el jugador correcto
                    inputeadas.append(queries[i])
                    dataChavales=[]
                    for row in player_rows:
                        #Nombre del jugador
                        player_name = row.find('img', class_='bilderrahmen-fixed')['title']
    
                        #Equipo del jugador
                        team_name = row.find('img', class_='tiny_wappen')['title']
    
                        #Valor de mercado del jugador
                        market_value = row.find('td', class_="rechts hauptlink").text.strip()
    
                        dataChavales.append([player_name, team_name, market_value])
    
                    #DataFrame con los datos
                    chavales = pd.DataFrame(dataChavales, columns=['Player', 'Team', 'Market Value'])
                    print(chavales)
    
                    filaCorrecto=input("Qué fila es la del jugador que estás buscando? ") #Yo elijo qué jugador en la tabla es
                    if int(filaCorrecto) in range(0,10): #Si elijo un número del 1 al 10 
                        precios.append(chavales.loc[int(filaCorrecto)]["Market Value"])
                        playerTransferMarktUrl="https://www.transfermarkt.co.uk"+player_rows[int(filaCorrecto)].find_all('a')[1].get('href')
                        transferMarkturl.append(playerTransferMarktUrl)
                        responseQueryPlayer = requests.get(playerTransferMarktUrl, headers=headers)
                        html_contentQueryPlayer = responseQueryPlayer.text
                        soupQueryPlayer = BeautifulSoup(html_contentQueryPlayer, 'html.parser')
                        tablitaPerfil=[z.text.strip() for z in soupQueryPlayer.find_all('span', class_='info-table__content info-table__content--regular')]
                        if "Position:" in tablitaPerfil:
                            exact_position.append(soupQueryPlayer.find_all('span', class_='info-table__content info-table__content--bold')[tablitaPerfil.index("Position:")].text.strip())
                        else:
                            print("No tiene posición exacta Transfermarkt")
                            exact_position.append("Revisa luego")
                        if "Foot:" in tablitaPerfil:
                            good_foot.append(soupQueryPlayer.find_all('span', class_='info-table__content info-table__content--bold')[tablitaPerfil.index("Foot:")].text.strip())
                        else:
                            print("No tiene pie bueno Transfermarkt")
                            good_foot.append("Revisa luego")
                        #photoset=soupQueryPlayer.find("a", class_="data-header__box__club-link").find("img").get("srcset").replace('\n', '')
                        #fotoEquipo.append(photoset.split(",")[0].split()[0])
                        #fotoEquipo_HD.append(photoset.split(",")[1].split()[0])
                        #fotoJugador.append(soupQueryPlayer.find("div", class_="modal-trigger").find("img").get("src"))
                    else: #Si no elijo un número del 1 al 10, o sea, si el jugador no estaba en el DataFrame que he creado
                        print("No has encontrado nada en "+queries[i]+"?")
                        print("Entiendo que no está en la tabla, pongo para que revises luego")
                        precios.append("Revisa luego")
                        exact_position.append("Revisa luego")
                        good_foot.append("Revisa luego")
                        transferMarkturl.append("Revisa luego")
                        #fotoEquipo.append("Revisa luego")
                        #fotoEquipo_HD.append("Revisa luego")
                        #fotoJugador.append("Revisa luego")
        except Exception as e: #Si algo del anterior proceso no ha salido bien
            print(e)
            #print(queries[i])
            print("Jugador no encontrado, se añade a la lista y el precio se deja como No disponible")
            precios.append("No disponible")
            exact_position.append("Revisa luego")
            good_foot.append("Revisa luego")
            transferMarkturl.append("Revisa luego")
            #fotoEquipo.append("Revisa luego")
            #fotoEquipo_HD.append("Revisa luego")
            #fotoJugador.append("Revisa luego")
            queriesQueNo.append(queries[i])
    print(len(precios), len(exact_position), len(good_foot), i+1)
    if i%20==0: # Supervisión del proceso para hacerlo más ameno al sacar los datos
        print("Lo último que he añadido es el precio de "+df["Player"][i]+" que es "+precios[i])
        print("Que por cierto es "+exact_position[i]+" y usa el pie "+good_foot[i])
        print("A descansar")
        #print("El link de su foto es "+fotoJugador[i]) NO USADO
        if i%100==0: #De nuevo, supervisión del proceso
            outliers=0
            for x in good_foot:
                if x not in ["left","right","Revisa luego","both"]:
                    outliers+=1
            print("Hay "+str(outliers)+ " valores que no han ido bien. Espero te valga")
        time.sleep(15)
    
        
df["Market Value"]=precios
df["Position detailed"]=exact_position
df["Foot"]=good_foot
df["Transfermarkt URL"]=transferMarkturl
#df["Team Badge"]=fotoEquipo
#df["Team Badge HD"]=fotoEquipo_HD
#df["Player Photo"]=fotoJugador



#df.to_csv("transfermarkt.csv",index=False) DEJADO COMO COMENTARIO PARA EVITAR SOBRESCRIBIR EL RESULTADO



"""
MANEJO DE INCONGRUENCIAS EN EL ANTERIOR PROCESO
-----------------------------------------------

Jugadores donde "se asumió" y el valor de jugador es -, lo cual no debería pasar
df[df["Market Value"]=='-'][["Player (Squad)","Market Value"]]

queriesQueNo
df[df["Market Value"]=='No disponible'][["Player (Squad)","Market Value"]]
df[df["Market Value"]=='Revisa luego'][["Player (Squad)","Market Value"]]

#Jugadores que "se asumieron" y "se repiten en la tabla a pesar de tener queries distintas"
c = Counter(list(df["Player"]))
[k for k, v in c.items() if v > 1]
df[df["Player"].isin([k for k, v in c.items() if v > 1])][["Player (Squad)","Market Value"]]
En nuestro caso se encontraron Danilo, Rodri, Vitinha

good_foot o exact_position no disponibles en Transfermarkt
df[df["Position detailed"]=='Revisa luego']["Player (Squad)"]
NADIE
df[df["Foot"]=='Revisa luego']["Player (Squad)"]
8 jugadores
                                    
c = Counter(list(df["Transfermarkt URL"]))
[k for k, v in c.items() if v > 1]
df[df["Transfermarkt URL"].isin([k for k, v in c.items() if v > 1])][["Player (Squad)","Transfermarkt URL"]]                               
Emerson (el del Tottenham)
"""


#Función creada para actualizar los datos de la tabla de los jugadores para los que
#hemos encontrado incongruencias
def actualizar_tio(player_squad,new_link):
    responseUpdate = requests.get(new_link, headers=headers)
    if responseUpdate.status_code == 200:
        html_contentUpdate = responseUpdate.text
        soupUpdate = BeautifulSoup(html_contentUpdate, 'html.parser')
        tablitaUpdate=[z.text.strip() for z in soupUpdate.find_all('span', class_='info-table__content info-table__content--regular')]
        if "Position:" in tablitaUpdate:
            df.loc[df["Player (Squad)"] == player_squad, 'Position detailed'] = soupUpdate.find_all('span', class_='info-table__content info-table__content--bold')[tablitaUpdate.index("Position:")].text.strip()
        else:
            print("No tiene posición exacta Transfermarkt")
            df.loc[df["Player (Squad)"] == player_squad, 'Position detailed'] = "Revisa luego"
        if "Foot:" in tablitaPerfil:
            df.loc[df["Player (Squad)"] == player_squad, 'Foot'] = soupUpdate.find_all('span', class_='info-table__content info-table__content--bold')[tablitaUpdate.index("Foot:")].text.strip()
        else:
            print("No tiene pie bueno Transfermarkt")
            df.loc[df["Player (Squad)"] == player_squad, 'Foot'] = "Revisa luego"
            
        df.loc[df["Player (Squad)"] == player_squad, 'Transfermarkt URL'] = new_link
        df.loc[df["Player (Squad)"] == player_squad, 'Market Value'] = soupUpdate.find("a", class_="data-header__market-value-wrapper").text.strip().split()[0]


