import requests
import json
import IP3
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
            print("When the weather is less than 40 degrees Fahrenheit, it is important to take some precautions to stay warm and safe. Dressing in layers is key to retaining body heat, so make sure to wear a thermal undershirt, sweater, jacket, and a hat. Do not forget to protect your extremities by wearing warm socks, insulated waterproof boots, gloves or mittens, a scarf, and earmuffs or a hat. A heavy winter coat that provides insulation and wind resistance is essential to shield you from the cold. Stay hydrated by drinking warm fluids like tea or hot water, even though it is cold outside. Be cautious of icy surfaces and take extra care while walking or driving. If you need to go outdoors, minimize your exposure and take regular breaks in warm indoor areas. Ensure that your home's heating system is working properly to maintain a warm and comfortable indoor environment. Check on vulnerable individuals like elderly neighbors, young children, or those who may be more susceptible to the cold. Lastly, when planning outdoor activities, choose appropriate winter sports or exercises and be prepared with the right gear and safety precautions. Stay warm and stay safe!")
            print(' ')
        elif temp < 60:
            print("When the temperature is below 60 degrees Fahrenheit but above 40, it's still important to take some precautions to stay comfortable in the cooler weather. Dressing in layers is a good approach, starting with a light sweater or long-sleeved shirt as a base layer. Consider carrying a light jacket or hoodie with you for added warmth, especially during cooler evenings or if the temperature drops unexpectedly. Keep a lightweight scarf or shawl handy, as it can be a versatile accessory to provide extra warmth when needed. Opt for comfortable pants or jeans made of thicker material to help keep you insulated. Don't forget to protect your extremities by wearing comfortable socks and closed-toe shoes, and consider having a pair of lightweight gloves or mittens on hand. Keep an eye on the weather forecast for any potential changes and be prepared with an umbrella or waterproof jacket if rain is expected. Remember to stay hydrated by drinking enough water throughout the day. Adjust the indoor heating to maintain a cozy environment when spending time indoors. Consider the activities you have planned and dress appropriately for the specific weather conditions. Embrace the pleasant cooler weather while staying comfortable and prepared. Enjoy outdoor activities like hiking or taking walks, and take the opportunity to savor a warm beverage outdoors. Stay comfortable and make the most of the weather!!")
            print(' ')
        elif temp < 80:
            print("When the temperature rises above 60 degrees Fahrenheit but stays below 80, it's important to take certain precautions to stay comfortable in the warmer weather. Dress in light and breathable clothing such as shorts, skirts, or lightweight pants made of fabrics like cotton or linen. Opt for short-sleeved shirts, tank tops, or lightweight blouses to keep cool. Wearing a hat or cap can provide shade and protect your face from the sun. Don't forget to apply sunscreen to exposed skin and wear sunglasses to shield your eyes from harmful UV rays. Stay hydrated by drinking plenty of water throughout the day, especially if you're engaging in outdoor activities. Seek shade or take breaks in air-conditioned or well-ventilated areas to prevent overheating. If possible, plan outdoor activities during the cooler parts of the day, such as early morning or late afternoon. Use fans or air conditioning to maintain a comfortable indoor environment. Be mindful of the signs of heat exhaustion or heat stroke, such as dizziness, fatigue, excessive sweating, or rapid heartbeat. If you experience any of these symptoms, seek shade, rest, and hydrate. Enjoy the pleasant weather by participating in outdoor activities like picnics, walks, or outdoor sports. Stay comfortable and make the most of the warmer temperatures while taking care of your well-being.")
            

        elif temp < 90:
            print("When the temperature climbs above 80 degrees Fahrenheit but stays below 90, it's important to take precautions to stay comfortable and cool in the warmer weather. Opt for lightweight and breathable clothing, such as loose-fitting cotton shirts, shorts, skirts, or dresses, to allow air circulation and help with heat dissipation. Wearing a wide-brimmed hat or a cap can provide shade and protect your face and head from the sun's rays. Apply sunscreen generously to exposed skin and wear sunglasses to protect your eyes from UV rays. Stay hydrated by drinking plenty of water throughout the day, especially during outdoor activities. Seek shade or create your own shade with umbrellas, canopies, or sunshades. Plan your outdoor activities during the cooler parts of the day, such as early morning or evening. If possible, choose shaded routes or trails for walks or runs. Use fans, air conditioning, or natural ventilation to cool indoor spaces. Take frequent breaks in cool or air-conditioned areas to prevent overheating. Be mindful of the signs of heat-related illnesses, such as dizziness, nausea, headache, or muscle cramps. If you experience any of these symptoms, find a cool place to rest, hydrate, and seek medical attention if necessary. Enjoy outdoor activities like swimming, water sports, or picnics near water bodies. Stay cool and make the most of the warmer weather while prioritizing your well-being.")

        elif temp < 100:
            print("Try to stay indoors & ")

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


def getWeatherCF(location):
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
        return temp
    except BaseException:
        print("I dont think that is a place!")
        
def message(temp):
    if temp < 40:
        m = "When the weather is less than 40 degrees Fahrenheit, it is important to take some precautions to stay warm and safe. Dressing in layers is key to retaining body heat, so make sure to wear a thermal undershirt, sweater, jacket, and a hat. Do not forget to protect your extremities by wearing warm socks, insulated waterproof boots, gloves or mittens, a scarf, and earmuffs or a hat. A heavy winter coat that provides insulation and wind resistance is essential to shield you from the cold. Stay hydrated by drinking warm fluids like tea or hot water, even though it is cold outside. Be cautious of icy surfaces and take extra care while walking or driving. If you need to go outdoors, minimize your exposure and take regular breaks in warm indoor areas. Ensure that your home's heating system is working properly to maintain a warm and comfortable indoor environment. Check on vulnerable individuals like elderly neighbors, young children, or those who may be more susceptible to the cold. Lastly, when planning outdoor activities, choose appropriate winter sports or exercises and be prepared with the right gear and safety precautions. Stay warm and stay safe!"
                    
    elif temp < 60:
        m = "When the temperature is below 60 degrees Fahrenheit but above 40, it's still important to take some precautions to stay comfortable in the cooler weather. Dressing in layers is a good approach, starting with a light sweater or long-sleeved shirt as a base layer. Consider carrying a light jacket or hoodie with you for added warmth, especially during cooler evenings or if the temperature drops unexpectedly. Keep a lightweight scarf or shawl handy, as it can be a versatile accessory to provide extra warmth when needed. Opt for comfortable pants or jeans made of thicker material to help keep you insulated. Don't forget to protect your extremities by wearing comfortable socks and closed-toe shoes, and consider having a pair of lightweight gloves or mittens on hand. Keep an eye on the weather forecast for any potential changes and be prepared with an umbrella or waterproof jacket if rain is expected. Remember to stay hydrated by drinking enough water throughout the day. Adjust the indoor heating to maintain a cozy environment when spending time indoors. Consider the activities you have planned and dress appropriately for the specific weather conditions. Embrace the pleasant cooler weather while staying comfortable and prepared. Enjoy outdoor activities like hiking or taking walks, and take the opportunity to savor a warm beverage outdoors. Stay comfortable and make the most of the weather!!"

    elif temp < 80:
        m = "When the temperature rises above 60 degrees Fahrenheit but stays below 80, it's important to take certain precautions to stay comfortable in the warmer weather. Dress in light and breathable clothing such as shorts, skirts, or lightweight pants made of fabrics like cotton or linen. Opt for short-sleeved shirts, tank tops, or lightweight blouses to keep cool. Wearing a hat or cap can provide shade and protect your face from the sun. Don't forget to apply sunscreen to exposed skin and wear sunglasses to shield your eyes from harmful UV rays. Stay hydrated by drinking plenty of water throughout the day, especially if you're engaging in outdoor activities. Seek shade or take breaks in air-conditioned or well-ventilated areas to prevent overheating. If possible, plan outdoor activities during the cooler parts of the day, such as early morning or late afternoon. Use fans or air conditioning to maintain a comfortable indoor environment. Be mindful of the signs of heat exhaustion or heat stroke, such as dizziness, fatigue, excessive sweating, or rapid heartbeat. If you experience any of these symptoms, seek shade, rest, and hydrate. Enjoy the pleasant weather by participating in outdoor activities like picnics, walks, or outdoor sports. Stay comfortable and make the most of the warmer temperatures while taking care of your well-being."
                    
    elif temp < 90:
        m = "When the temperature climbs above 80 degrees Fahrenheit but stays below 90, it's important to take precautions to stay comfortable and cool in the warmer weather. Opt for lightweight and breathable clothing, such as loose-fitting cotton shirts, shorts, skirts, or dresses, to allow air circulation and help with heat dissipation. Wearing a wide-brimmed hat or a cap can provide shade and protect your face and head from the sun's rays. Apply sunscreen generously to exposed skin and wear sunglasses to protect your eyes from UV rays. Stay hydrated by drinking plenty of water throughout the day, especially during outdoor activities. Seek shade or create your own shade with umbrellas, canopies, or sunshades. Plan your outdoor activities during the cooler parts of the day, such as early morning or evening. If possible, choose shaded routes or trails for walks or runs. Use fans, air conditioning, or natural ventilation to cool indoor spaces. Take frequent breaks in cool or air-conditioned areas to prevent overheating. Be mindful of the signs of heat-related illnesses, such as dizziness, nausea, headache, or muscle cramps. If you experience any of these symptoms, find a cool place to rest, hydrate, and seek medical attention if necessary. Enjoy outdoor activities like swimming, water sports, or picnics near water bodies. Stay cool and make the most of the warmer weather while prioritizing your well-being."
    else:
        m = "When the mercury soars to a sweltering 100 degrees Fahrenheit, it’s crucial to prioritize your well-being and take measures to stay cool and safe. To combat the scorching heat, follow these recommendations:First and foremost, stay hydrated by drinking plenty of water throughout the day. Dehydration can occur rapidly in high temperatures, so carry a water bottle with you and make a conscious effort to sip on fluids regularly. Avoid sugary or alcoholic beverages, as they can exacerbate dehydration. Seek shade or air-conditioned spaces to escape the direct heat. Limit your exposure to the sun and spend time in shaded areas whenever possible. If air conditioning is available, take advantage of it by staying indoors in cooled environments such as your home, shopping malls, or public buildings. If you lack access to air conditioning, use fans or create cross-ventilation by opening windows and doors to circulate air. Dressing appropriately can make a significant difference in staying cool. Opt for loose-fitting, lightweight clothing made of breathable fabrics like cotton or linen. Light colors help reflect sunlight, keeping you cooler. Don’t forget to shield yourself from the sun’s rays by wearing a wide-brimmed hat and sunglasses."
    return m

def capital(country):
    url = "https://restcountries.com/v3.1/name"
    params = {
        "fullText": "true",
        "fields": "name,capital",
    }
    response = requests.get(f"{url}/{country}", params=params)
    data = response.json()

    if response.status_code == 200 and data:
        return data[0]['capital'][0]
    else:
        return None
