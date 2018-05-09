import requests
import json
import pprint
import time
import os

URL = 'https://query.yahooapis.com/v1/public/yql?'

city = 'st-petersburg'
params = {
    'q': 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="{}")'.format(city),
    'format': 'json'
}


# API_KEY = config.weather_api_key


def temperature(f):
    return (int(f) - 32) / 9 * 5


def ru_week_day(week_day):
    week_dict = {
        'Mon': 'Понедельник',
        'Tue': 'Вторник',
        'Wed': 'Среда',
        'Thu': 'Четверг',
        'Fri': 'Пятница',
        'Sat': 'Суббота',
        'Sun': 'Воскресенье'
    }

    return week_dict[str(week_day)]

    # Солнечно: b'\xe2\x98\x80\xef\xb8\x8f',
    # Малооблачно: b'\xf0\x9f\x8c\xa4',
    # Переменная облачность: b'\xe2\x9b\x85\xef\xb8\x8f',
    # Облачно с прояснениями: b'\xf0\x9f\x8c\xa5',
    # Местами дожди: b'\xf0\x9f\x8c\xa6',
    # Радуга: b'\xf0\x9f\x8c\x88',
    # Облачно: b'\xe2\x98\x81\xef\xb8\x8f',
    # Дождь: b'\xf0\x9f\x8c\xa7',
    # Дождь с грозой: b'\xe2\x9b\x88',
    # Гроза: b'\xf0\x9f\x8c\xa9',
    # Снег: b'\xf0\x9f\x8c\xa8',
    # Снеговик1: b'\xe2\x98\x83\xef\xb8\x8f',
    # Снеговик2: b'\xe2\x9b\x84\xef\xb8\x8f',
    # Снежинка: b'\xe2\x9d\x84\xef\xb8\x8f',
    # Стужа: b'\xf0\x9f\x8c\xac',
    # Ветер: b'\xf0\x9f\x92\xa8',
    # Ураган: b'\xf0\x9f\x8c\xaa'


def yahoo_weather_smile(weather):
    code_dict = {
        '0': b'\xf0\x9f\x8c\xaa',
        '1': b'\xf0\x9f\x8c\xaa',
        '2': b'\xf0\x9f\x8c\xaa',
        '3': b'\xf0\x9f\x8c\xa9',
        '4': b'\xf0\x9f\x8c\xa9',
        '5': b'\xf0\x9f\x8c\xa7 \xf0\x9f\x8c\xa8',
        '6': b'\xf0\x9f\x8c\xa7 \xf0\x9f\x8c\xa8',
        '7': b'\xf0\x9f\x8c\xa7 \xf0\x9f\x8c\xa8',
        '8': b'\xf0\x9f\x8c\xac',
        '9': b'\xf0\x9f\x8c\xac',
        '10': b'\xf0\x9f\x8c\xac \xf0\x9f\x8c\xa7',
        '11': b'\xf0\x9f\x8c\xa7',
        '12': b'\xf0\x9f\x8c\xa7',
        '13': b'\xf0\x9f\x92\xa8 \xf0\x9f\x8c\xa8',
        '14': b'\xf0\x9f\x8c\xa8 \xf0\x9f\x8c\xa7',
        '15': b'\xf0\x9f\x8c\xac \xf0\x9f\x92\xa8',
        '16': b'\xf0\x9f\x8c\xa8',
        '17': b'\xf0\x9f\x8c\xa8',
        '18': b'\xf0\x9f\x8c\xa8 \xf0\x9f\x8c\xa7',
        '19': b'\xf0\x9f\x92\xa8',
        '20': b'\xf0\x9f\x92\xa8',
        '21': b'\xf0\x9f\x92\xa8',
        '22': b'\xf0\x9f\x92\xa8',
        '23': b'\xf0\x9f\x92\xa8',
        '24': b'\xf0\x9f\x92\xa8',
        '25': b'\xf0\x9f\x8c\xac',
        '26': b'\xe2\x98\x81\xef\xb8\x8f',
        '27': b'\xf0\x9f\x8c\xa5',
        '28': b'\xf0\x9f\x8c\xa5',
        '29': b'\xe2\x9b\x85\xef\xb8\x8f',
        '30': b'\xf0\x9f\x8c\xa4',
        '31': b'\xe2\x98\x80\xef\xb8\x8f',
        '32': b'\xe2\x98\x80\xef\xb8\x8f',
        '33': b'\xe2\x98\x80\xef\xb8\x8f',
        '34': b'\xe2\x98\x80\xef\xb8\x8f',
        '35': b'\xe2\x9b\x88',
        '36': b'\xe2\x98\x80\xef\xb8\x8f',
        '37': b'\xf0\x9f\x8c\xa9 \xe2\x98\x80\xef\xb8\x8f',
        '38': b'\xf0\x9f\x8c\xa9 \xe2\x98\x80\xef\xb8\x8f',
        '39': b'\xf0\x9f\x8c\xa9 \xe2\x98\x80\xef\xb8\x8f',
        '40': b'\xf0\x9f\x8c\xa7 \xe2\x98\x80\xef\xb8\x8f',
        '41': b'\xe2\x98\x83\xef\xb8\x8f',
        '42': b'\xf0\x9f\x8c\xa8 \xf0\x9f\x8c\xa7',
        '43': b'\xe2\x98\x83\xef\xb8\x8f',
        '44': b'\xf0\x9f\x8c\xa4',
        '45': b'\xf0\x9f\x8c\xa9',
        '46': b'\xf0\x9f\x8c\xa8 \xf0\x9f\x8c\xa7',
        '47': b'\xf0\x9f\x8c\xa9'
    }
    return code_dict[weather]


def wether_smile(icon_num):
    icon_dict = {
        '1': b'\xe2\x98\x80\xef\xb8\x8f',
        '2': b'\xf0\x9f\x8c\xa4',
        '3': b'\xe2\x9b\x85\xef\xb8\x8f',
        '4': b'\xe2\x9b\x85\xef\xb8\x8f',
        '5': b'\xf0\x9f\x8c\xa5',
        '6': b'\xf0\x9f\x8c\xa5',
        '7': b'\xe2\x98\x81\xef\xb8\x8f',
        '8': b'\xe2\x98\x81\xef\xb8\x8f',
        '9': b'\xe2\x98\x81\xef\xb8\x8f',
        '10': b'\xe2\x98\x81\xef\xb8\x8f',
        '11': b'\xf0\x9f\x8c\xac',
        '12': b'\xf0\x9f\x8c\xa7',
        '13': b'\xf0\x9f\x8c\xa6',
        '14': b'\xf0\x9f\x8c\xa6',
        '15': b'\xe2\x9b\x88',
        '16': b'\xf0\x9f\x8c\xa6 \xf0\x9f\x8c\xa9',
        '17': b'\xf0\x9f\x8c\xa4 \xf0\x9f\x8c\xa9',
        '18': b'\xf0\x9f\x8c\xa7',
        '19': b'\xe2\x98\x81\xef\xb8\x8f \xf0\x9f\x92\xa8',
        '20': b'\xf0\x9f\x8c\xa5 \xf0\x9f\x92\xa8',
        '21': b'\xf0\x9f\x8c\xa5 \xf0\x9f\x92\xa8',
        '22': b'\xf0\x9f\x8c\xa8',
        '23': b'\xe2\x9b\x85\xef\xb8\x8f \xf0\x9f\x8c\xa8',
        '24': b'\xf0\x9f\x8c\xa8 \xf0\x9f\x8c\xac',
        '25': b'\xf0\x9f\x8c\xa7 \xf0\x9f\x8c\xa8',
        '26': b'\xf0\x9f\x8c\xa7 \xf0\x9f\x8c\xa8',
        '27': b'\xf0\x9f\x8c\xa7 \xf0\x9f\x8c\xa8',
        '28': b'\xe2\x98\x80\xef\xb8\x8f',
        '29': b'\xf0\x9f\x8c\xa7 \xf0\x9f\x8c\xa8',
        '30': b'\xe2\x98\x80\xef\xb8\x8f',
        '31': b'\xf0\x9f\x8c\xac',
        '32': b'\xf0\x9f\x92\xa8',
    }

    return icon_dict[str(icon_num)]


def is_relevant():
    if time.time() - os.path.getmtime('weather.json') < 3600:
        return True
    else:
        return False


def get_weather_from_api():
    r = requests.get(URL, params)
    with open('weather.json', 'w') as f:
        json.dump(r.json()['query']['results']['channel']['item']['forecast'], f, ensure_ascii=False, indent=4)

    return True


def weather_keyboard():
    if not is_relevant():
        get_weather_from_api()

    with open('weather.json', 'r') as file:
        forecast = json.load(file)

        keyboard = []
        for day_weather in forecast:
            day = {}

            week_day = ' '.join([ru_week_day(day_weather['day']), day_weather['date'][:-5]])

            t = round(temperature(day_weather['high']), 1)

            smile = yahoo_weather_smile(day_weather['code']).decode()

            text = '{} {}Сº {}'.format(week_day, t, smile)
            day['text'] = text
            day['callback_data'] = 'choose_date'
            keyboard.append(day)

    pprint.pprint(keyboard)

    return keyboard


if __name__ == '__main__':
    weather_keyboard()
