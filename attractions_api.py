# Import the required library

from amadeus import Client, ResponseError
import requests

def get_iso_country_code(country):
    url = f'https://restcountries.com/v3/name/{country}'
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        print(data)
        if 'cca2' in data[0]:
            return data[0]['cca2']
    return ""

def get_city_coordinates(city, country):
    iso_country_code = get_iso_country_code(country)
    if not iso_country_code:
        return None, None
    username = 'jessemeci'
    url = f'http://api.geonames.org/searchJSON?q={city}&country={iso_country_code}&maxRows=1&username={username}'
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        print(data)
        if 'geonames' in data and data['geonames']:
            latitude = data['geonames'][0]['lat']
            longitude = data['geonames'][0]['lng']
            return latitude, longitude
    return None, None

def get_attractions(city, country):
    amadeus = Client(
        client_id='XL0O1puwmIuXvtHVgZQmgzjjAQkAmoKW',
        client_secret='Li9lNYdIKT162SRB'
    )
    latitude, longitude = get_city_coordinates(city, country)
    if not latitude or not longitude:
        return None
    print(latitude,longitude)
    try:
        response = amadeus.reference_data.locations.points_of_interest.get(
            latitude=float(latitude),
            longitude=float(longitude)
        )
        print('jijijiijijijijiji')
        print(response.data)
        print('aoaoaoaoaoa')
        return response.data
    except ResponseError as error:
        print("fail")
        return None

