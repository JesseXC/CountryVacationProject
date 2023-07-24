# Import the required library
from geopy.geocoders import Nominatim
from amadeus import Client, ResponseError
import requests
# Initialize Nominatim API

#geolocator = Nominatim(user_agent="MyApp")

#location = geolocator.geocode("Barcelona")

#print("The latitude of the location is: ", location.latitude)
#print("The longitude of the location is: ", location.longitude)

params = {
    'key': 'AIzaSyBDEJUeTXgUq04aOQFue5ZNf9-GtuEdaHM',
    'address': 'Barcelona'
}

#base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
#response = requests.get(base_url,params=params).json()
#response.keys()
#print(response)
#geometry = response['results'][0]['geometry']
#lat = geometry['location']['lat']
#lon = geometry['location']['lng']

#print(lat,lon)

amadeus = Client(
    client_id='uj8JO5AizIUIzeAoK0vF3qAVcMNi5EfD',
    client_secret='dMudNMOE8FAcszeS'
)
def get_attractions():
    try:
        response = amadeus.reference_data.locations.points_of_interest.get(
            latitude=41.397158, 
            longitude=2.160873
        )
        return response
        #print(response.data)
    except ResponseError as error:
        print(error)

#attractions = [{'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '9CB40CB5D0', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/9CB40CB5D0', 'methods': ['GET']}, 'geoCode': {'latitude': 41.39165, 'longitude': 2.164772}, 'name': 'Casa Batlló', 'category': 'SIGHTS', 'rank': 5, 'tags': ['sightseeing', 'sights', 'museum', 'landmark', 'tourguide', 'restaurant', 'attraction', 'activities', 'commercialplace', 'shopping', 'souvenir']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '4690B83DCA', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/4690B83DCA', 'methods': ['GET']}, 'geoCode': {'latitude': 41.397987, 'longitude': 2.161159}, 'name': 'La Pepita', 'category': 'RESTAURANT', 'rank': 30, 'tags': ['restaurant', 'tapas', 'pub', 'bar', 'sightseeing', 'commercialplace']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '3EF139D861', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/3EF139D861', 'methods': ['GET']}, 'geoCode': {'latitude': 41.38827, 'longitude': 2.161604}, 'name': 'Brunch & Cake', 'category': 'RESTAURANT', 'rank': 30, 'tags': ['vegetarian', 'restaurant', 'breakfast', 'shopping', 'bakery', 'transport', 'patio', 'garden']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': 'AB3F122E3E', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/AB3F122E3E', 'methods': ['GET']}, 'geoCode': {'latitude': 41.392376, 'longitude': 2.160919}, 'name': 'Cervecería Catalana', 'category': 'RESTAURANT', 'rank': 30, 'tags': ['restaurant', 'tapas', 'sightseeing', 'traditionalcuisine', 'bar', 'activities', 'commercialplace']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '752402FCA2', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/752402FCA2', 'methods': ['GET']}, 'geoCode': {'latitude': 41.40043, 'longitude': 2.15463}, 'name': 'Botafumeiro', 'category': 'RESTAURANT', 'rank': 30, 'tags': ['restaurant', 'seafood', 'sightseeing', 'professionalservices', 'transport', 'commercialplace']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '5F1CED3994', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/5F1CED3994', 'methods': ['GET']}, 'geoCode': {'latitude': 41.39148, 'longitude': 2.164981}, 'name': 'Casa Amatller', 'category': 'SIGHTS', 'rank': 100, 'tags': ['sightseeing', 'sights', 'museum', 'landmark', 'restaurant', 'tourguide', 'historicplace', 'historic', 'attraction', 'commercialplace', 'activities', 'shopping', 'events']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '30601A1A90', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/30601A1A90', 'methods': ['GET']}, 'geoCode': {'latitude': 41.390785, 'longitude': 2.167414}, 'name': 'Tapas 24', 'category': 'RESTAURANT', 'rank': 100, 'tags': ['restaurant', 'tapas', 'traditionalcuisine', 'sightseeing', 'commercialplace', 'transport', 'patio', 'garden', 'activities', 'bar']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '15C8B8148C', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/15C8B8148C', 'methods': ['GET']}, 'geoCode': {'latitude': 41.392677, 'longitude': 2.153942}, 'name': 'Dry Martini', 'category': 'NIGHTLIFE', 'rank': 100, 'tags': ['bar', 'restaurant', 'nightlife', 'club', 'sightseeing', 'attraction', 'activities']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': 'BD29CF2CCD', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/BD29CF2CCD', 'methods': ['GET']}, 'geoCode': {'latitude': 41.399193, 'longitude': 2.159853}, 'name': 'Con Gracia', 'category': 'RESTAURANT', 'rank': 100, 'tags': ['restaurant', 'sightseeing', 'commercialplace', 'professionalservices', 'activities']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '24DE6CE737', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/24DE6CE737', 'methods': ['GET']}, 'geoCode': {'latitude': 41.390198, 'longitude': 2.156974}, 'name': 'Osmosis', 'category': 'RESTAURANT', 'rank': 100, 'tags': ['restaurant', 'shopping', 'transport', 'professionalservices']}] 