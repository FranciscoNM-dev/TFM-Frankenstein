# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 11:04:37 2024

@author: Cuchu
"""

import pandas as pd



#JOIN DE LOS DOS CSV
fbref=pd.read_csv("fbref.csv")
transfermarkt=pd.read_csv("transfermarkt.csv")
transfermarkt=transfermarkt[["Player (Squad)", 'Market Value',
       'Position detailed', 'Foot', "fbref URL", "Transfermarkt URL"]]
print("fbref dimensiones "+str(fbref.shape))
print("transfermarkt dimensiones "+str(transfermarkt.shape)) 


join = pd.merge(fbref,transfermarkt,how='outer',
                left_on=["Player (Squad)"],right_on=["Player (Squad)"])

join.to_csv("preClean.csv",index='False')
print("Después del join dimensiones "+str(join.shape))

#LIMPIAR Y AÑADIR COLUMNAS (las que se me ocurran)
join['statsPK%'] = join.apply(lambda row: round(100*int(row.statsPK) / int(row.statsPKatt),2) if int(row.statsPKatt) != 0 else 0, axis=1)

print("Después de añadir columnas dimensiones "+str(join.shape))


columnas=list(join.columns)

#De momento solo se ha considerado una columna añadida


#A estas les haré un punto drop. Tienen el nombre exacto de la tabla
droppear=['statsPlayer', 'statsSquad', 'stats90s', 'statsGls.1',
            'statsAst.1', 'statsG+A.1', 'statsG-PK.1', 'statsG+A-PK', 
            'statsxG.1', 'statsxAG.1', 'statsxG+xAG', 'statsnpxG.1',
            'statsnpxG+xAG.1', 'keepersMP', 'keepersStarts', 'keepersMin',
            'keepersGA90', 'keepersW', 'keepersD', 'keepersL', 'keepersadvGA',
            'keepersadvPKA', 'keepersadv/90', 'keepersadv#OPA/90', 'shootingGls',
            'shootingSh/90', 'shootingSoT/90', 'shootingPK', 'shootingPKatt',
            'shootingxG', 'shootingnpxG', 'passingAst', 'passingxAG', 'passingPrgP',
            'passing_typesAtt', 'passing_typesCmp', 'gcaSCA90', 'gcaGCA90',
            'possessionPrgC', 'possessionPrgR', 'miscCrdY', 'miscCrdR', 'miscCrs',
            'miscInt', 'miscTklW']

#Por esta lista de aquí cambiaré columns
columnasTabla=["Player (Squad)", "Nation", "Pos.", "Comp.", "Age", "Born", "Matches",
               "Starts", "Mins", "Gls", "Assists", "G+A", "Gls-PKGls", "PKGls",
               "PKatt", "Y. Cards", "R. Cards", "xG", "npxG", "xAG", "npxG+xAG",
               "PrgC", "PrgP", "PrgR", 'GK Gls Ag', 'GK SoTA', 'GK Saves',
               'GK Save%', 'GK Cl. Sh.', 'GK Cl. Sh%', 'GK PKag', 'GK PKGls Ag',
               'GK PK Saves', 'GK PK Missed', 'GK PK Save%', 'GK FKGls Ag',
               'GK Corner Gls Ag', 'GK Own Gls Ag', 'GK PSxG Ag', 'GK PSxG/SoT Ag',
               'GK PSxG-Gls Ag', 'GK LaunchCmp', 'GK LaunchAtt', 'GK LaunchCmp%',
               'GK Pass-GK att', 'GK ThrowsAtt', 'GK Launch Pass%', 'GK PassAvgLen',
               'GK GK Att', 'GK GK Launch%', 'GK GK AvgLen', 'GK Crs Ag', 'GK Crs Caught',
               'GK Crs Caught%', 'GK Out PenArea', 'GK AvgGoalDist', 'Shots', 'SoT',
               'SoT%', 'Gls/Sh', 'Gls/SoT', 'Shot Avg Dist', 'FK Shots', 'npxG/Sh',
               'Gls-xG', 'npGls-npxG', 'Cmp Pass', 'Att Pass', 'Cmp Pass%', 'Pass Tot Dist',
               'Pass Prog Dist', 'SPass Cmp', 'SPass Att', 'SPass Cmp%', 'MPass Cmp',
               'MPass Att', 'MPass Cmp%', 'LPass Cmp', 'LPass Att', 'LPass Cmp%',
               'xA', 'Assists-xAG', 'Key Pass', '1/3 Pass', 'Area Pass', 'Area Cross',
               'Live Pass', 'Dead Pass', 'FK Pass', 'TB Pass', 'Switches', 'Crosses',
               'Throw Ins', 'Corners', 'In. Corners', 'Out. Corners', 'Str. Corners',
               'Pass Off.', 'Pass Blk.', 'SCA', 'SCA Live', 'SCA Dead', 'SCA TO',
               'SCA Sh', 'SCA Foul', 'SCA Def.', 'GCA', 'GCA Live', 'GCA Dead', 'GCA TO',
               'GCA Sh', 'GCA Foul', 'GCA Def.', 'Tkl', 'TklW', 'Tkl Def', 'Tkl Mid',
               'Tkl Att', 'Drib Tkl', 'Drib Chall.', 'Drib Tkl%', 'Chall. Lost',
               'Blocks', 'Sh. Bl.', 'Pass bl.', 'Int', 'Tkl+Int', 'Clr', 'Def Err',
               'Tch', 'Tch DefArea', 'Tch DefThird', 'Tch MidThird', 'Thc AttThird',
               'Tch AttArea', 'Thc Live', 'TO Att', 'TO Succ', 'TO Succ%', 'TO Tkld',
               'TO Tkld%', 'Carries', 'Crr TotD', 'Crr PrgD', 'Crr AttThird', 'Crr AttArea',
               'MisCtrl', 'Disp', 'Pass Rec', '2Y. Cards', 'FoulC', 'FoulD', 'Offsides',
               'PKWon', 'PKConc', 'Own Gls', 'Recov', 'AirW', 'AirL', 'AirW%', 'Value',
               'Pos. Det.', 'Foot', 'fbref URL', 'Transfermarkt URL', 'PKGls%'] 



#DE REFERENCIA SOLO, PARA ACTIVAR LAS MÉTRICAS /90s
no90bles=["Player (Squad)", "Nation", "Pos.", "Comp.", "Age", "Born", "Matches",
          "Starts", "Mins", 'GK Save%', 'GK Cl. Sh%', 'GK PK Save%', 'GK LaunchCmp%',
          'GK Launch Pass%', 'GK PassAvgLen', 'GK GK Launch%', 'GK GK AvgLen',
          'GK Crs Caught%', 'GK AvgGoalDist', 'SoT%', 'Gls/Sh','Gls/SoT',
          'Shot Avg Dist', 'npxG/Sh', 'Cmp Pass%', 'SPass Cmp%', 'MPass Cmp%',
          'LPass Cmp%', 'Drib Tkl%', 'TO Succ%', 'TO Tkld%', 'AirW%', 'PKGls%',
          'Value', 'Pos. Det.', 'Foot', 'fbref URL', 'Transfermarkt URL']




join.drop(droppear, axis=1, inplace=True)

join.columns=columnasTabla

columnasNew=list(join.columns)

#Comp
join["Comp."]=[x[x.index(" ")+1:] for x in join["Comp."]]

#Age
join.loc[join["Player (Squad)"] == "Marco Pellegrino (Salernitana)", 'Age'] = 21.0

#Born
join.loc[join["Player (Squad)"] == "Marco Pellegrino (Salernitana)", 'Born'] = 2002.0

#Nation (pre cleanse)
join.loc[join["Player (Squad)"] == "Marco Pellegrino (Salernitana)", 'Nation'] = "ar ARG"

#Las demás todas juntas
join = join.fillna(value=0)

#Ahora pequeño cleanse, de momento a Value y a Nation
join["Nation"]=[x.split()[1] for x in list(join["Nation"])]

#Unificar formato Precios
preciosNew=[]
for x in join['Value']:
    if 'mill' in x:
        preciosNew.append("€"+x.split()[0].replace(",",".")+"m")
    elif "mil" in x:
        preciosNew.append("€"+x.split()[0].replace(",",".")+"k")
    else:
        preciosNew.append(x)

join["Value"]=preciosNew




join.to_csv("pruebaDefinitivo.csv", index=False)

#DATOS POR 90. Hacemos una hard copy para empezar
join90=join.copy()

for x in columnasNew:
    if x not in no90bles:
        join90[x]=round(join[x]*(90/join90['Mins']),2)
        



    
join90.to_csv("pruebaDefinitivo90.csv", index=False)



    
    
    
    
    
    
