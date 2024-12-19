from get_weather_api import get_forecast_weather_gor_n_days
from get_coords_by_name import get_coords_by_name
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio

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



def create_photo_weather(city, days):
    data = get_data_for_plot(city, days)
    temp_fig = px.line(data, x='time', y='temp', title='Temperature', markers=True)
    humidity_fig = px.line(data, x='time', y='humidity', title='Humidity', markers=True)
    speed_wind_fig = px.line(data, x='time', y='speed_wind', title='Speed Wind', markers=True)
    rain_fig = px.line(data, x='time', y='rain', title='Rain', markers=True)
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=('Temperature', 'Humidity', 'Speed Wind', 'Rain'))
    fig.add_trace(temp_fig.data[0], row=1, col=1)
    fig.add_trace(humidity_fig.data[0], row=1, col=2)
    fig.add_trace(speed_wind_fig.data[0], row=2, col=1)
    fig.add_trace(rain_fig.data[0], row=2, col=2)
    fig.update_layout(height=800, width=800, title_text=f'Прогноз погоды в городе {city} на {days} дней ',
                      showlegend=False)
    fig.write_image("photos/subplot_layout.png")


def create_map_for_trip(start_sity, end_city, city_points = [], type_map = 'png'):
    try:
        coords_cities_with_info = pd.DataFrame(
            columns=['lat', 'lon', 'time', 'city', 'temp', 'humidity', 'speed_wind', 'rain'])
        for i in [start_sity] + city_points + [end_city]:
            data = get_data_for_plot(i, 1).iloc[0]
            coords = get_coords_by_name(i)
            new_data = pd.DataFrame(
                {'lat': [coords['lat']], 'lon': [coords['lon']], 'time': data['time'], 'city': [i], 'temp': [data['temp']],
                 'humidity': [data['humidity']], 'speed_wind': [data['speed_wind']], 'rain': [data['rain']]})
            coords_cities_with_info = pd.concat([coords_cities_with_info, new_data], ignore_index=True)
            map_fig = px.line_map(coords_cities_with_info, lat="lat", lon="lon", zoom=3, height=600,
                                  hover_name='city',  # Основное название во всплывающей подсказке
                                  hover_data={
                                      'time': True,  # Показываем время
                                      'temp': True,
                                      'humidity': True,
                                      'speed_wind': True,
                                      'rain': True,
                                      'lat': False,
                                      'lon': False
                                  },
                                  text='city'
                                  )
            map_fig.update_traces(
                mode='markers+lines',
                marker=dict(size=5, color='red'),
                textposition='top right'
            )
        if type_map == 'png':
            pio.write_image(map_fig, file="photos/map_layout.png")
        elif type_map == 'html':
            pio.write_html(map_fig, file="photos/map_layout.html", full_html=True)
    except Exception as e:
        print(f'Ошибка при создании карты: {e}')
        return None


