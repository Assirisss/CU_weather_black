# from flask import Flask, render_template, request
import pandas as pd

from get_coords_by_name import get_coords_by_name
from get_weather_api import get_current_weather, get_forecast_weather, get_forecast_weather_gor_n_days
from get_coords_by_name import get_coords_by_name
from weather_assessment import weather_assessment

from dash import Dash, html,dcc, callback, Output, Input, jupyter_dash
import plotly.express as px
import dash_bootstrap_components as dbc
import ast
import pandas as pd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


def get_data_for_plot(city, days):
    coords = get_coords_by_name(city)
    data = pd.DataFrame(columns=['time', 'temp', 'humidity', 'speed_wind', 'rain'])
    for s in get_forecast_weather_gor_n_days(coords['lat'], coords['lon'], days):
        forecast = s[0]
        time = s[1]
        new_data = pd.DataFrame({'time': [time], 'temp': [forecast['temp']], 'humidity': [forecast['humidity']],
                                 'speed_wind': [forecast['speed_wind']], 'rain': [forecast['rain']]})
        data = pd.concat([data, new_data], ignore_index=True)
    return data



app.layout = html.Div([
    html.Header('Weather assessment'),

    dbc.Col([html.P('Город')]),
    dcc.Input(id='main_city', type='text', value='Moscow'),

    dcc.Dropdown(
        id='days-dropdown',
        options=[{'label': f'{i} day(s)', 'value': i} for i in range(1, 6)],
        value=1,
        clearable=False
    ),
    dbc.Row([
        dbc.Col([dcc.Graph(id='temp-graph')], width=3),
        dbc.Col([dcc.Graph(id='humidity-graph')], width=3),
        dbc.Col([dcc.Graph(id='speed-wind-graph')], width=3),
        dbc.Col([dcc.Graph(id='rain-graph')], width=3),
    ]),
    dbc.Row([
        dbc.Col([html.P('Город Отправления')]),
        dcc.Input(id='start_city', type='text', value='Moscow'),
        dbc.Col([html.P('Промежуточный пункт')]),
        dcc.Input(id='middle_city', type='text', value='Rostov-on-Don'),
        dbc.Col([html.P('Город назначения')]),
        dcc.Input(id='finish_city', type='text', value='Sochi'),
    ]),
    dcc.Graph(id='map_fig'),
    ])

@app.callback(
    [Output('temp-graph', 'figure'),
     Output('humidity-graph', 'figure'),
     Output('speed-wind-graph', 'figure'),
     Output('rain-graph', 'figure'),
    Output('map_fig', 'figure')],

    [Input('days-dropdown', 'value'),
     Input('start_city', 'value'),
     Input('middle_city', 'value'),
     Input('finish_city', 'value'),
     Input('main_city', 'value')]
)
def update_graphs(days, start_city, middle_city, finish_city, main_city):
    data = get_data_for_plot(main_city, days)
    temp_fig = px.line(data, x='time', y='temp', title='Temperature',markers=True)
    humidity_fig = px.line(data, x='time', y='humidity', title='Humidity',markers=True)
    speed_wind_fig = px.line(data, x='time', y='speed_wind', title='Speed Wind',markers=True)
    rain_fig = px.line(data, x='time', y='rain', title='Rain',markers=True)
    coords_cities_with_info = pd.DataFrame(columns=['lat', 'lon', 'time', 'city', 'temp', 'humidity', 'speed_wind', 'rain'])
    for i in [start_city, middle_city, finish_city]:
        data = get_data_for_plot(i, days).iloc[0]
        coords = get_coords_by_name(i)
        new_data = pd.DataFrame({'lat': [coords['lat']], 'lon': [coords['lon']], 'time':data['time'], 'city': [i], 'temp': [data['temp']],
                                 'humidity': [data['humidity']], 'speed_wind': [data['speed_wind']], 'rain': [data['rain']]})
        coords_cities_with_info = pd.concat([coords_cities_with_info, new_data], ignore_index=True)


    map_fig = px.line_map(coords_cities_with_info, lat="lat", lon="lon", zoom=3, height=600,
    hover_name = 'city',  # Основное название во всплывающей подсказке
    hover_data = {
        'time': True,  # Показываем время
        'temp': True,
        'humidity': True,
        'speed_wind': True,
        'rain': True,
        'lat': False,
        'lon': False
    },
    )
    map_fig.update_traces(
        mode='markers+lines',  # режим отображения: линии + маркеры
        marker=dict(size=5, color='red')  # размер и цвет точек
    )




    return temp_fig, humidity_fig, speed_wind_fig, rain_fig, map_fig

if __name__ == '__main__':
    app.run_server(port=8010, use_reloader=True)

