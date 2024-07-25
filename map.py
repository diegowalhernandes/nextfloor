import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


# Exemplo de DataFrame com coordenadas geográficas
data = {
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'Lat': [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
    'Lon': [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740],
    'Population': [8419000, 3980000, 2716000, 2328000, 1690000]
}
df = pd.DataFrame(data)


# Criando o mapa usando plotly.express
fig = px.scatter_mapbox(
    df, 
    lat="Lat", 
    lon="Lon", 
    hover_name="City", 
    hover_data=["Population"],
    zoom=3,
    height=600
)

# Configurando o layout do mapa
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='map',
        figure=fig
    ),
    html.Div(id='click-data')
])

@app.callback(
    Output('click-data', 'children'),
    [Input('map', 'clickData')]
)
def display_click_data(clickData):
    if clickData is None:
        return "Clique em um ponto no mapa para ver os detalhes"
    else:
        point = clickData['points'][0]
        city = point['hovertext']
        return f"Cidade: {city}, População: {df[df['City'] == city]['Population'].values[0]}"


if __name__ == '__main__':
    app.run_server(debug=True)
