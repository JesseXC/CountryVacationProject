# Import the required library
from amadeus import Client, ResponseError
import requests

def get_city(city,country):
    amadeus = Client(
        client_id='XL0O1puwmIuXvtHVgZQmgzjjAQkAmoKW',
        client_secret='Li9lNYdIKT162SRB'
    )
    response = amadeus.reference_data.locations.cities.get(countryCode=get_iso_country_code(country), keyword = city,max = 5).data
    print(response)
    return response[0]['geoCode']['latitude'],response[0]['geoCode']['longitude']

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
    latitude, longitude = get_city(city, country)
    if not latitude or not longitude:
        return None
    print(latitude,longitude)
    #print(str(float(latitude)),str(float(longitude)))
    #print(amadeus.reference_data.locations.points_of_interest.get(
           # latitude=41.397158,
            #longitude=2.060873,
           # radius = 10
        #).data)
    try:
        response = amadeus.reference_data.locations.points_of_interest.get(
            latitude=float(latitude),
            longitude=float(longitude),
            radius = 20
        )
        return response.data
    except ResponseError as error:
        print("fail")
        return None
    
def get_flights(airport1,airport2,departureDate,passengers):
    amadeus = Client(
        client_id='XL0O1puwmIuXvtHVgZQmgzjjAQkAmoKW',
        client_secret='Li9lNYdIKT162SRB'
    )
    try:
        response = amadeus.shopping.flight_offers_search.get(originLocationCode=f'{airport1}', destinationLocationCode=f'{airport2}', departureDate=f'{departureDate}', adults=f'{passengers}',max=9)
    except ResponseError as error:
        print("fail")
        return None
    flights = response.data

    flight_info = create_flight_info(flights)
    return flight_info


def create_flight_info(flights):
    flight_info = {}
    i = 1
    for flight in flights:
        if not isinstance(flight,dict):
            print("skipped")
            continue
        segments = flight['itineraries'][0]['segments']  # Assuming there's only one itinerary per flight
        flight_info[f'flight{i}'] = {
            'numberofBookableSeats': flight['numberOfBookableSeats'],
            'oneWay': flight['oneWay'],
            'totalDuration': flight['itineraries'][0]['duration'],
            'currency':flight['price']['currency'],
            'total_price':flight['price']['grandTotal'],
            'segments': []
        }
        for segment in segments:
            segment_info = {
                'departureAirport': segment['departure']['iataCode'],
                'departureDate': segment['departure']['at'],
                'arrivalAirport': segment['arrival']['iataCode'],
                'arrivalDate': segment['arrival']['at'],
                'carrierCode': segment['carrierCode'],
                'number': segment['number'],
                'duration': segment['duration']
            }
            flight_info[f'flight{i}']['segments'].append(segment_info)
        i += 1
    return flight_info
