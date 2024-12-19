from get_weather_api import get_forecast_weather_gor_n_days
from get_coords_by_name import get_coords_by_name
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

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



def create_photo(city, days ):
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