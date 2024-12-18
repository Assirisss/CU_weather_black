
def weather_assessment(temp, humidity, wind_speed, rain_probability):
    temp, humidity, wind_speed, rain_probability = [float(i.split()[0]) for i in [temp, humidity, wind_speed, rain_probability]]

    flag = True
    try:
        if temp < 5 and wind_speed > 8:
            flag = False

        if rain_probability > 60 and wind_speed > 10:
            flag = False

        if temp < 0 and humidity > 80:
            flag = False

        if temp > 30 and humidity > 80:
            flag = False

        if humidity < 10 or humidity > 90:
            flag = False

        if wind_speed > 6:
            flag = False

        if temp < -10 or temp > 35:
            flag = False

        return 'Благоприятная погода' if flag else 'Неблагоприятная погода'
    except:
        return 'Ошибка с обработкой данных'


