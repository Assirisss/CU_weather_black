from geopy import Nominatim

def check_city(city_name, language='en'):
    geolocator = Nominatim(user_agent="city_checker")
    location = geolocator.geocode(city_name, language=language)
    return location is not None

