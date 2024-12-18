from platform import uname

import flask
import requests
import json


from api_key import API_KEY
lat = 55.7558
lon = 37.6173


def get_current_weather(lat, lon):
    url_weather_cur = 'https://api.openweathermap.org/data/2.5/weather'

    params_weather_cur = {
        'appid':API_KEY,
        'lat':lat,
        'lon':lon,
        'units': 'metric'
    }
    response = requests.request(url=url_weather_cur, method='GET', params=params_weather_cur).json()
    print(lat, lon)
    current = dict(
    temp = f"{response.get('main').get('temp')} °C",
    humidity = f"{response.get('main').get('humidity')} %",
    speed_wind = f"{response.get('wind').get('speed')} m/s",
    rain = f"{0 if response.get('rain') is None else 100} %"
    )

    return current

def get_forecast_weather(lat, lon):
    url_weather_cur = 'https://api.openweathermap.org/data/2.5/forecast'

    params_weather_cur = {
        'appid': API_KEY,
        'lat': lat,
        'lon': lon,
        'units': 'metric'
    }
    response = requests.request(url=url_weather_cur, method='GET', params=params_weather_cur).json()
    response =response.get('list')
    mas = []
    for i in range(7):
        tem = response[i]
        forecst = dict(
            temp=tem.get('main').get('temp'),
            humidity=tem.get('main').get('humidity'),
            speed_wind=tem.get('wind').get('speed'),
            rain = tem.get('pop') * 100
        )
        mas.append([forecst, tem.get('dt_txt')])
    return  mas


def get_forecast_weather_gor_n_days(lat, lon, n):
    url_weather_cur = 'https://api.openweathermap.org/data/2.5/forecast'

    params_weather_cur = {
        'appid': API_KEY,
        'lat': lat,
        'lon': lon,
        'units': 'metric'
    }
    response = requests.request(url=url_weather_cur, method='GET', params=params_weather_cur).json()
    response =response.get('list')
    mas = []
    for i in range(1, 8 * n + 1):

        if n <= 5:
            if n == 5:
                i -= 1
            tem = response[i]
            forecst = dict(
                temp=tem.get('main').get('temp'),
                humidity=tem.get('main').get('humidity'),
                speed_wind=tem.get('wind').get('speed'),
                rain = tem.get('pop') * 100
            )
            mas.append([forecst, tem.get('dt_txt')])
        else:
            return 'Прогноз доступен только на 5 дней'
    return mas






