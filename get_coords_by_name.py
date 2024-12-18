import requests
from api_key import API_KEY

def get_coords_by_name(name_city):
    url = 'https://api.openweathermap.org/geo/1.0/direct'
    params = {
        "q": name_city,  # Название города
        "limit": 1,  # Ограничение результатов (1 = один город)
        "appid": API_KEY  # Ваш API-ключ
    }
    response = requests.get(url, params=params).json()
    ans = dict(
        lat = response[0].get('lat'),
        lon = response[0].get('lon'),
    )

    return ans

print(get_coords_by_name('Moscow'))