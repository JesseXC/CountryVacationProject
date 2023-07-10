import requests
import json
import IP3
import pandas as pd
import sqlalchemy as db
import os

url = "https://weatherapi-com.p.rapidapi.com/current.json"
datadic = {'city': [], 'temperature': [], 'condition': []}
# api_key = os.environ.get('keyy')
api_key = "21e93e2c23msh82e86793cfb9b11p1ee6cfjsnf1750e6150b1"
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}


def getName(name=None):
    global namee
    if name is None:
        namee = input("What is your name? ")
        location = IP3.getLocation()
        print(
            f"Hello {namee}, the weather in "
            f"{location['city']} is {Weather(location)}F°")
        print(' ')
        c = input('Where are you going to? ')
        getWeather(c)
    else:
        location = IP3.getLocation()
        print(
            f"Hello again {namee}, the weather in "
            f"{location['city']} is {Weather(location)}F°")
        print(' ')
        c = input('Where are you going next? ')
        getWeather(c)


def getWeather(location):
    global datadic
    param = {'q': location}
    try:
        response = requests.get(url, headers=headers, params=param)
        data = response.json()
        condition = data['current']['condition']['text']
        temp = data['current']['temp_f']
        name1 = data['location']['name']
        datadic['city'].append(name1)
        datadic['temperature'].append(temp)
        datadic['condition'].append(condition)
        print(f"It's {temp}°F in {name1}!")
        if temp < 40:
            print("I would just relocate if I was you")
            print(' ')
        elif temp < 60:
            print("Don't forget to grab a jacket!")
            print(' ')
        elif temp < 80:
            print("Grab some flowers on the way!")
            print(' ')
        elif temp < 90:
            print("Don’t forget to drink plenty of water!")
            print(' ')
        elif temp < 100:
            print("Try to stay indoors & ")
            print("don't worry about polar bears!")
            print(' ')
        else:
            print("I would just relocate if I was you")
    except BaseException:
        print("I dont think that is a place!")
    b = input('Do you want to go to another place? [Y/N] ')
    if b == 'Y':
        getName(namee)
    else:
        print('Goodbye, have a great day!')


def Weather(location):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    headers = {
        "X-RapidAPI-Key": "21e93e2c23msh82e86793cfb9b11p1ee6cfjsnf1750e6150b1",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}
    try:
        location = IP3.getLocation()
        param = {'q': location}
        response = requests.get(url, headers=headers, params=param)
        data = response.json()
        temp = data['current']['temp_f']
        name1 = data['location']['name']
        return temp
    except BaseException:
        print('You should not go there!')


def WeatherCelsius(location):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    headers = {
        "X-RapidAPI-Key": "21e93e2c23msh82e86793cfb9b11p1ee6cfjsnf1750e6150b1",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}
    try:
        location = IP3.getLocation()
        param = {'q': location}
        response = requests.get(url, headers=headers, params=param)
        data = response.json()
        temp = data['current']['temp_c']
        name1 = data['location']['name']
        return temp
    except BaseException:
        print('You should not go there!')


def getWeatherCelsius(location):
    param = {'q': location}
    try:
        response = requests.get(url, headers=headers, params=param)
        data = response.json()

        condition = data['current']['condition']['text']
        temp = data['current']['temp_c']
        name1 = data['location']['name']
        datadic['city'].append(name1)
        datadic['temperature'].append(temp)
        datadic['condition'].append(condition)

        print(f"It's {temp}°C in {name1}!")
        if temp < 5:
            print("I would just relocate if I was you")
        elif temp < 16:
            print("Don't forget to grab a jacket!")
        elif temp < 27:
            print("Grab some flowers on the way!")
        elif temp < 32:
            print("Don’t forget to drink plenty of water!")
        elif temp < 38:
            print("Try to stay indoors & ")
            print("don't worry about polar bears!")
        else:
            print("I would just relocate if I was you")
    except BaseException:
        print("error")
    b = input('Do you want to go to another place? [Y/N] ')
    if b == 'Y':
        getNameCelsius(namee)
    else:
        print('Goodbye, have a great trip!')


def getNameCelsius(name=None):
    global namee
    if name is None:
        namee = input("What is your name? ")
        location = IP3.getLocation()
        print(
            f"Hello {namee}, the weather in "
            f"{location['city']} is {WeatherCelsius(location)}C°")
        c = input('Where are you going to? ')
        getWeatherCelsius(c)
    else:
        location = IP3.getLocation()
        print(
            f"Hello again {namee}, the weather in "
            f"{location['city']} is {WeatherCelsius(location)}C°")
        c = input('Where are you going next? ')
        getWeatherCelsius(c)


cof = input(
    'Hello! Do you want the information in Celsius or Farenheit? [C/F] ')
if cof == 'C':
    getNameCelsius()
else:
    getName()
data_frame = pd.DataFrame(datadic)
engine = db.create_engine('sqlite:///diffweathers.db')
data_frame.to_sql('articles', con=engine, if_exists='replace', index=False)
with engine.connect() as connection:
    query_result = connection.execute(
        db.text("SELECT * FROM articles ORDER BY temperature;")).fetchall()
    print(pd.DataFrame(query_result))
