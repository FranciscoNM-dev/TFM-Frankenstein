# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 01:18:43 2024

@author: Cuchu
"""

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State, MATCH, ALL
import pandas as pd
from utils import funcion_prueba_percentiles, funcion_prueba_similitud_coseno, value_transform

# Mis datos
df = pd.read_csv("data/processed/pruebaDefinitivo.csv")
df90 = pd.read_csv("data/processed/pruebaDefinitivo90.csv")
columnas=list(df.columns)
columnasTablaValues=columnas[9:160]+[columnas[-1]]

comunes=["Player (Squad)", "Nation", "Pos.", "Comp.", 'Age', "Born", "Matches",
          "Starts", "Mins", 'Value', 'Pos. Det.', 'Foot', 'fbref URL', 'Transfermarkt URL']







dropdownNames=["Goals","Assists","Goals + Assists", "Goals no Pen", "Goals Pen",
               "Pens Attempted", "Yellow Cards", "Red Cards", "Expected Goals (xG)",
               "Expected Goals no Pen (npxG)", "Expected Assisted Goals (xAG)", 
               "npxG+xAG", "Progressive Carries", "Progressive Passes", 
               "Progressive pass Receptions", "GK Goals Against", 
               'GK Shots on Target Against', 'GK Saves', 'GK Save%',
               'GK Clean Sheets', 'GK Clean Sheet%', 'GK Pens Against', 'GK Pen Goals allowed',
               'GK Pens Saved', 'GK Pens Missed', 'GK Pen Save%', 'GK Free Kick Goals allowed',
               'GK Corner Goals allowed', 'GK Own Goals allowed', 'GK Post-Shot xG allowed',
               'GK Post-Shot xG/Sh. on Target allowed', 'GK Post-Shot xG - Goals allowed',
               'GK Launch Passes completed', 'GK Launch Passes attempted', 'GK Launch Passes completed%',
               'GK Passes attempted no Goal Kick', 'GK Throws attempted', 'GK Launch Passes%',
               'GK Pass Average Length', 'GK Goal Kicks attempted', 'GK Launch Goal Kick%',
               'GK Goal Kick Average Length', 'GK Crosses faced', 'GK Crosses caught',
               'GK Crosses caught%', 'GK Actions Outside Penalty Area',
               'GK Average Distance from Goal', 'Shots', 'Shots on Target', 'Shot on Target%',
               'Goals/Shot','Goals/Shot on Target', 'Shot Average Distance', 'Free Kick Shots',
               'npxG/Shot', 'Goals - xG', 'No pen Goals - no pen xG', 'Completed Passes',
               'Attempted Passes', 'Completed Passes%', 'Passes Total Distance',
               'Passes Progressive Distance', 'Completed Short Passes', 'Attempted Short Passes',
               'Completed Short Passes%', 'Completed Medium Passes', 'Attempted Medium Passes',
               'Completed Medium Passes%', 'Completed Long Passes', 'Attempted Long Passes',
               'Completed Long Passes%', 'Expected Assists (xA)', 'Assists-xAG', 'Key Passes',
               'Passes into Final Third', 'Passes into Pen Area', 'Crosses into Pen Area',
               'Live Ball Passes', 'Dead Ball Passes', 'Free Kick Passes', 'Through Ball Passes',
               'Switches', 'Crosses Taken', 'Throw Ins taken', 'Corners taken', 
               'Inswinging Corner Kicks', 'Outswinging Corner Kicks', 'Straight Corner Kicks',
               'Passes Offside', 'Passes Blocked', 'Shot Creating Actions (SCA)',
               'SCA from Live Ball Passes', 'SCA from Dead Ball Passes', 'SCA from Take Ons',
               'SCA from Shots', 'SCA from Fouls Drawn', 'SCA from Def. Actions',
               'Goal Creating Actions (GCA)', 'GCA from Live Ball Passes',
               'GCA from Dead Ball Passes', 'GCA from Take Ons', 'GCA from Shots',
               'GCA from Fouls Drawn', 'GCA from Def. Actions', 'Tackles', 'Tackles won',
               'Tackles in Deffensive Third', 'Tackles in Middle Third',
               'Tackles in Attacking Third', 'Dribblers Tackled', 'Dribblers Challenged',
               'Dribblers Tackled%', 'Challenges lost', 'Blocks', 'Shots blocked',
               'Passes blocked', 'Interceptions', 'Tackles + interceptions', 'Clears',
               'Defensive errors', 'Touches', 'Touches in Defensive Area',
               'Touches in Defensive third', 'Touches in Middle third', 'Touches in Attacking Third',
               'Touches in Attacking Area', 'Live Ball Touches', 'Take Ons Attempted',
               'Take Ons Succeeded', 'Take Ons Succeeded%', 'Take Ons Tackled',
               'Take Ons Tackled%', 'Carries', 'Carries Total Distance',
               'Carries Progressive Distance', 'Carries into Final Third', 'Carries into Pen Area',
               'Miscontrols', 'Times dispossessed', 'Passes Received', 'Second Yellow Cards',
               'Fouls Comitted', 'Fouls Drawn', 'Offsides', 'Penalty Kicks won',
               'Penalty Kicks conceded', 'Own Goals', 'Recoveries', 'Aerial Duels won',
               'Aerial Duels lost', 'Aerial Duels Won%', 'Goals Pen%']



# Inicializa la aplicación Dash
app = dash.Dash(__name__)

# Define el layout de la aplicación
app.layout = html.Div(
    [
        html.Div(id="page",
            children=[
                html.Div(id="title",
                    children=[html.H1("FRANKENSTEIN")]
                ),
                html.Div(id="content",
                         children=[    
                    html.Div(id="cardcolumn",
                        #style={"width": "20%", "padding": "10px", "padding-top": "100px"},
                        children=[
                            # Input numérico para seleccionar la cantidad de conjuntos de Cards
                            html.Label('Number of parameters:'),
                            dcc.Input(
                                id='num-sets',
                                type='number',
                                value=1,
                                min=1
                            ),
                            # Contenedor para las Cards dinámicas
                            html.Div(id='card-container', style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start'}),

                            # Guardar el estado de los dropdowns
                            dcc.Store(id='stored-dropdowns', data={'dropdowns': []}),

                            # Componente para mostrar el resumen
                            html.P(id='resumen', style={'margin-top': '10px', 'whiteSpace': 'pre-line'})],
                    ),
                    html.Div(id="content2",
                        #style={"width": "80%", "padding": "10px"},
                        children=[
                            html.Div(id="filters-1",
                                     children=[
                                         html.Div(children=[
                                html.Label('Position: '),
                                dcc.Checklist(
                                    id='posicion',
                                    options=[
                                        {'label': 'Goalkeepers', 'value': 'Goalkeeper'},
                                        {'label': 'Defenders', 'value': 'Defender '},
                                        {'label': 'Midfielders', 'value': 'Midfield '},
                                        {'label': 'Forwards', 'value': 'Attack '}
                                    ],
                                    value=['Goalkeeper'],
                                    inline=True
                                )]),
                                html.Div(children=[
                                html.Label('Stats: '),
                                dcc.RadioItems(
                                    id='values',
                                    options=[
                                        {'label': 'Absolute', 'value': 'Abs'},
                                        {'label': 'Per 90', 'value': '90'}
                                    ],
                                    value='Abs',
                                    inline=True
                                )]),
                                html.Div(children=[
                                html.Label("Preferred foot: "),
                                dcc.RadioItems(
                                    id='foot',
                                    options=[
                                        {'label': 'Any', 'value': 'any'},
                                        {'label': 'Right', 'value': 'right'},
                                        {'label': 'Left', 'value': 'left'},
                                        {'label': 'Both', 'value': 'both'}
                                    ],
                                    value='any',
                                    inline=True
                                )])]),
                                # Filtro de edad
                                html.Div(children=[
                                html.Label('Age:'),
                                dcc.RangeSlider(
                                    id='age-slider',
                                    min=15,
                                    max=40,
                                    step=1,
                                    value=[20, 30],
                                    marks={i: str(i) for i in range(15, 41)}
                                )]),
                                # Filtro de precio
                                html.Div(children=[
                                html.Label("Market Value (€m): "),
                                dcc.RangeSlider(
                                    id='price-slider',
                                    min=0,
                                    max=200,
                                    step=5,
                                    value=[20, 70],
                                    marks={i: str(i) for i in range(0, 201, 10)}
                                )]),
                                # Radio buttons para decidir la función de similaridad
                                dash_table.DataTable(
                                    data=df.to_dict('records'),
                                    page_size=7,
                                    id="laTabla"
                                ),
                                # Componente para mostrar el resumen2
                                html.Div(id="last-div",
                                children=[
                                html.Div(id='function-div',children=[
                                html.Label("Similarity function: "),
                                dcc.RadioItems(id="function",
                                    options=[
                                        {'label': 'Percentiles', 'value': 'Percentiles'},
                                        {'label': 'Cosine similarity', 'value': 'Similitud coseno'}
                                    ],
                                    value='Similitud coseno',
                                    inline=True
                                )]),
                                html.Div(children=[
                                html.P(id='resumen2')])]),
                                ]
                )])
        ],
        #style={
            #"display": "flex",
            #"flexDirection": "row",
            #"justifyContent": "space-between",
        #},
        ),
    ]
)


# Función para generar las Cards dinámicas
def display_cards(num_sets, stored_dropdowns, posicion):
    card_children = []

    for i in range(num_sets):
        column_value = stored_dropdowns['dropdowns'][i]['column'] if i < len(
            stored_dropdowns['dropdowns']) else columnasTablaValues[0]
        jugador_value = stored_dropdowns['dropdowns'][i]['jugador'] if i < len(
            stored_dropdowns['dropdowns']) else df["Player (Squad)"].unique()[0]
        importancia_value = stored_dropdowns['dropdowns'][i]['importancia'] if i < len(
            stored_dropdowns['dropdowns']) else 1

        new_card = html.Div([
            html.Div([
                dcc.Dropdown(
                    id={'type': 'columnas-tabla', 'index': f'{i}-1'},
                    options=[{'label': dropdownNames[i], 'value': columnasTablaValues[i]} for i in
                             range(len(dropdownNames))],
                    value=column_value,
                    style={'width': '100%', 'margin-bottom': '10px'}  # Personalizar la anchura y margen del primer dropdown
                ),
                dcc.Dropdown(
                    id={'type': 'jugador', 'index': f'{i}-2'},
                    options=[{'label': players, 'value': players} for players in
                             df["Player (Squad)"].unique()],
                    value=jugador_value,
                    style={'width': '100%',
                           'margin-bottom': '10px'}  # Personalizar la anchura y margen del segundo dropdown
                ),
                dcc.Slider(
                    id={'type': 'importancia', 'index': f'{i}-3'},
                    min=1,
                    max=10,
                    marks={i: str(i) for i in range(1, 11)},
                    value=importancia_value,
                    step=1
                )
            ], style={'display': 'flex', 'flex-direction': 'column'}),  # Flexbox para dropdowns y slider verticales

        ], style={'border': '1px solid #ccc', 'padding': '10px', 'border-radius': '5px', 'margin-bottom': '20px',
                  'width': '300px'})

        card_children.append(new_card)


    return card_children


# Callback para actualizar el número de conjuntos de Cards
@app.callback(
    Output('card-container', 'children'),
    [Input('num-sets', 'value'),
     Input('posicion', 'value')],
    State('stored-dropdowns', 'data')
)
def update_cards(num_sets, posicion, stored_dropdowns):
    return display_cards(num_sets, stored_dropdowns, posicion)


# Callback para mantener el estado de los dropdowns en el Store
@app.callback(
    Output('stored-dropdowns', 'data'),
    [Input({'type': 'columnas-tabla', 'index': ALL}, 'value'),
     Input({'type': 'jugador', 'index': ALL}, 'value'),
     Input({'type': 'importancia', 'index': ALL}, 'value'),
     Input('posicion', 'value')],
    State('stored-dropdowns', 'data')
)
def update_store(column_values, jugador_values, importancia_values, posicion, stored_dropdowns):
    dropdowns = [{'column': c, 'jugador': j, 'importancia': i} for c, j, i in
                 zip(column_values, jugador_values, importancia_values)]
    stored_dropdowns['dropdowns'] = dropdowns
    return stored_dropdowns


# Callback para actualizar los datos de la tabla
@app.callback(
    Output('laTabla', 'data'),
    [Input({'type': 'columnas-tabla', 'index': ALL}, 'value'),
     Input({'type': 'jugador', 'index': ALL}, 'value'),
     Input({'type': 'importancia', 'index': ALL}, 'value'),
     Input('posicion', 'value'),
     Input('foot', 'value'),
     Input('function', 'value'),
     Input('age-slider', 'value'),
     Input('price-slider', 'value'),
     Input('values','value')]
)
def update_table_data(selected_columns, selected_players, selected_importance, posicion, foot, funcion, age_range, price_range,values):
    # Determinar qué dataset usar
    if values=='Abs':
        data = df.copy()
    
    else:
        data = df90.copy()
        

    try:
        # Actualizar los datos según la función seleccionada
        if funcion == "Similitud coseno":
            updated_data = funcion_prueba_similitud_coseno(selected_columns, selected_players, selected_importance, data)
        else:
            updated_data = funcion_prueba_percentiles(selected_columns, selected_players, selected_importance, data)
            
            
        #Le meto la edad
        # Filtrar los datos según el rango de edad y el pie
        if foot!='any':
            updated_data = updated_data[updated_data["Foot"].isin([foot, 'both'])]
                
        updated_data = updated_data[(updated_data['Age'] >= age_range[0]) & (updated_data['Age'] <= age_range[1]) & (updated_data["Pos. Det."].str.contains('|'.join(posicion))) &
                                    (updated_data['Value'].apply(value_transform) >= price_range[0]*1000000) & (updated_data['Value'].apply(value_transform) <= price_range[1]*1000000)]
        
    
        return updated_data.head(7).to_dict('records')
    except:
        return data[["Player (Squad)", "Nation", 'Pos. Det.', 'Foot', "Comp.", "Age",
                      "Mins", 'Value']].head(7).to_dict('records')

# Callback para actualizar el texto debajo de dropdowns
@app.callback(
    Output("resumen", 'children'),
    [Input({'type': 'columnas-tabla', 'index': ALL}, 'value'),
     Input({'type': 'jugador', 'index': ALL}, 'value'),
     Input({'type': 'importancia', 'index': ALL}, 'value'),
     Input('posicion', 'value'),
     Input('values','value')]
)
def update_text(column, jugador, importancia, posicion, values):
    texto = ''
    if values=='Abs':
        refdf = df.copy()
    
    else:
        refdf = df90.copy()
    try:
        for x in range(len(column)):
            texto += f'{jugador[x]} has {refdf[refdf["Player (Squad)"] == jugador[x]][column[x]].item()} {column[x]}\n'
    except:
        texto += "Please fill all fields to start the query"
    return texto


# Callback para actualizar el texto debajo de la tabla
@app.callback(
    Output("resumen2", 'children'),
    [Input({'type': 'columnas-tabla', 'index': ALL}, 'value'),
     Input({'type': 'jugador', 'index': ALL}, 'value'),
     Input({'type': 'importancia', 'index': ALL}, 'value'),
     Input('laTabla', 'data')]
)
def update_text2(column, jugador, importancia, tabla):
    texto = ''
    if len(column) > len(list(set(column))):
        texto += "Some features appear more than once. Please check the query\n"
    if len(tabla)==0:
        texto+= "There are no players with those characteristics. Please refine the applied filters"
    return texto


# Ejecución de la aplicación
if __name__ == '__main__':
    app.run(debug=False,port='2024')