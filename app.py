from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from login_form import LoginForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from youtube_api import TrendingVideos
from countryfacts import search_country, list_of_names
from Take2 import getWeatherCF, message, capital
from google_images import getImages
import pandas as pd
import json
from sqlalchemy import inspect
import ast
from data import countries
from data import regions
from wikipedia_api import get_summary
from amadeus import Client, ResponseError
import requests
from flask import Flask, session
from flask_session import Session
import secrets

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///country_information.db'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

db = SQLAlchemy(app)
Session(app)

engine = db.create_engine('sqlite:///country_information.db')
class Country_Info(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    Country = db.Column(db.String(120), unique=False, nullable=False)
    City = db.Column(db.String(600),unique=False,nullable=False)
    Country_Images = db.Column(db.String(600), unique=False, nullable=False)

    def __repr__(self):
        return f"Country_Info('{self.Country}', '{self.Country_Images}')"

class City_Attraction(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    City = db.Column(db.String(120),unique=False,nullable =False)
    Country = db.Column(db.String(120), unique=False, nullable=False)
    Image = db.Column(db.String(120),unique=False,nullable=False)
    Name = db.Column(db.String(120),unique=False,nullable=False)
    Address = db.Column(db.String(120),unique=False,nullable=False)
    Tags = db.Column(db.String(900),unique=False,nullable=False)
    Summary = db.Column(db.String(5000),unique=False,nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60),unique=False, nullable=False)
    country_city = db.Column(db.String(500),unique=False, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

with app.app_context():
    db.create_all()

@app.route("/")
@app.route("/home")
def home():
    print(session.get('logged_in'))
    print(session.get('username'))
    registration_success = session.get('logged_in',False)
    user_country_city = None
    if registration_success:
        name = session.get('username')
        logged_in_user = User.query.filter_by(username=name).first()
        user_country_city = logged_in_user.country_city.split('.')
        user_country_city = [entry.split(',') for entry in user_country_city if entry]
        print(user_country_city)
    return render_template('home.html',registration_success=registration_success,user_country_city= user_country_city)

@app.route("/countryInformation")
def country_information():
    info = None
    country = request.args.get('country')
    city = request.args.get('city')
<<<<<<< HEAD
    if session.get("logged_in", False):
        name = session.get('username')
        logged_in_user = User.query.filter_by(username=name).first()
        if logged_in_user:
            country_city_list = logged_in_user.country_city.split('.') if logged_in_user.country_city else []
            if [country, city] not in [entry.split(',') for entry in country_city_list]:
                logged_in_user.country_city += f"{country},{city}."
                db.session.commit()
                print("Updated country_city:", logged_in_user.country_city)
=======
    print(city)
    print(city)
    country_info = search_country(country, list_of_names)
    regions = ['AE', 'BH', 'DZ', 'EG', 'IQ', 'JO', 'KW', 'LB', 'LY', 'MA', 'OM', 'QA', 'SA', 'TN', 'YE', 'AZ', 'BY', 'BG', 'BD', 'BA', 'CZ', 'DK', 'AT', 'CH', 'DE', 'GR', 'AU', 'BE', 'CA', 'GB', 'GH', 'IE', 'IL', 'IN', 'JM', 'KE', 'MT', 'NG', 'NZ', 'SG', 'UG', 'US', 'ZA', 'ZW', 'AR', 'BO', 'CL', 'CO', 'CR', 'DO', 'EC', 'ES', 'GT', 'HN', 'MX', 'NI', 'PA', 'PE', 'PR', 'PY', 'SV', 'UY', 'VE', 'EE', 'FI', 'PH', 'FR', 'SN', 'HR', 'HU', 'ID', 'IS', 'IT', 'JP', 'GE', 'KZ', 'KR', 'LU', 'LA', 'LT', 'LV', 'MK', 'MY', 'NO', 'NP', 'NL', 'PL', 'BR', 'PT', 'RO', 'RU', 'LK', 'SK', 'SI', 'ME', 'RS', 'SE', 'TZ', 'TH', 'TR', 'UA', 'PK', 'VN', 'HK', 'TW', 'CY', 'KH', 'LI', 'PG']
    countries = {
        'Afghanistan': 'AF',
        'Albania': 'AL',
        'Algeria': 'DZ',
        'American Samoa': 'AS',
        'Andorra': 'AD',
        'Angola': 'AO',
        'Anguilla': 'AI',
        'Antarctica': 'AQ',
        'Antigua and Barbuda': 'AG',
        'Argentina': 'AR',
        'Armenia': 'AM',
        'Aruba': 'AW',
        'Australia': 'AU',
        'Austria': 'AT',
        'Azerbaijan': 'AZ',
        'Bahamas (the)': 'BS',
        'Bahrain': 'BH',
        'Bangladesh': 'BD',
        'Barbados': 'BB',
        'Belarus': 'BY',
        'Belgium': 'BE',
        'Belize': 'BZ',
        'Benin': 'BJ',
        'Bermuda': 'BM',
        'Bhutan': 'BT',
        'Bolivia': 'BO',
        'Bonaire, Sint Eustatius and Saba': 'BQ',
        'Bosnia and Herzegovina': 'BA',
        'Botswana': 'BW',
        'Bouvet Island': 'BV',
        'Brazil': 'BR',
        'British Indian Ocean Territory': 'IO',
        'Brunei Darussalam': 'BN',
        'Bulgaria': 'BG',
        'Burkina Faso': 'BF',
        'Burundi': 'BI',
        'Cabo Verde': 'CV',
        'Cambodia': 'KH',
        'Cameroon': 'CM',
        'Canada': 'CA',
        'Cayman Islands': 'KY',
        'Central African Republic': 'CF',
        'Chad': 'TD',
        'Chile': 'CL',
        'China': 'CN',
        'Christmas Island': 'CX',
        'Cocos (Keeling) Islands': 'CC',
        'Colombia': 'CO',
        'Comoros (the)': 'KM',
        'Congo': 'CD',
        'Congo': 'CG',
        'Cook Islands': 'CK',
        'Costa Rica': 'CR',
        'Croatia': 'HR',
        'Cuba': 'CU',
        'Curaçao': 'CW',
        'Cyprus': 'CY',
        'Czechia': 'CZ',
        'Côte d\'Ivoire': 'CI',
        'Denmark': 'DK',
        'Djibouti': 'DJ',
        'Dominica': 'DM',
        'Dominican Republic': 'DO',
        'Ecuador': 'EC',
        'Egypt': 'EG',
        'El Salvador': 'SV',
        'Equatorial Guinea': 'GQ',
        'Eritrea': 'ER',
        'Estonia': 'EE',
        'Eswatini': 'SZ',
        'Ethiopia': 'ET',
        'Falkland Islands': 'FK',
        'Faroe Islands (the)': 'FO',
        'Fiji': 'FJ',
        'Finland': 'FI',
        'France': 'FR',
        'French Guiana': 'GF',
        'French Polynesia': 'PF',
        'French Southern Territories': 'TF',
        'Gabon': 'GA',
        'Gambia (the)': 'GM',
        'Georgia': 'GE',
        'Germany': 'DE',
        'Ghana': 'GH',
        'Gibraltar': 'GI',
        'Greece': 'GR',
        'Greenland': 'GL',
        'Grenada': 'GD',
        'Guadeloupe': 'GP',
        'Guam': 'GU',
        'Guatemala': 'GT',
        'Guernsey': 'GG',
        'Guinea': 'GN',
        'Guinea-Bissau': 'GW',
        'Guyana': 'GY',
        'Haiti': 'HT',
        'Heard Island and McDonald Islands': 'HM',
        'Holy See (the)': 'VA',
        'Honduras': 'HN',
        'Hong Kong': 'HK',
        'Hungary': 'HU',
        'Iceland': 'IS',
        'India': 'IN',
        'Indonesia': 'ID',
        'Iran': 'IR',
        'Iraq': 'IQ',
        'Ireland': 'IE',
        'Isle of Man': 'IM',
        'Israel': 'IL',
        'Italy': 'IT',
        'Jamaica': 'JM',
        'Japan': 'JP',
        'Jersey': 'JE',
        'Jordan': 'JO',
        'Kazakhstan': 'KZ',
        'Kenya': 'KE',
        'Kiribati': 'KI',
        'Democratic Korea': 'KP',
        'Korea': 'KR',
        'Kuwait': 'KW',
        'Kyrgyzstan': 'KG',
        'Lao People\'s Democratic Republic': 'LA',
        'Latvia': 'LV',
        'Lebanon': 'LB',
        'Lesotho': 'LS',
        'Liberia': 'LR',
        'Libya': 'LY',
        'Liechtenstein': 'LI',
        'Lithuania': 'LT',
        'Luxembourg': 'LU',
        'Macao': 'MO',
        'Madagascar': 'MG',
        'Malawi': 'MW',
        'Malaysia': 'MY',
        'Maldives': 'MV',
        'Mali': 'ML',
        'Malta': 'MT',
        'Marshall Islands': 'MH',
        'Martinique': 'MQ',
        'Mauritania': 'MR',
        'Mauritius': 'MU',
        'Mayotte': 'YT',
        'Mexico': 'MX',
        'Micronesia': 'FM',
        'Moldova': 'MD',
        'Monaco': 'MC',
        'Mongolia': 'MN',
        'Montenegro': 'ME',
        'Montserrat': 'MS',
        'Morocco': 'MA',
        'Mozambique': 'MZ',
        'Myanmar': 'MM',
        'Namibia': 'NA',
        'Nauru': 'NR',
        'Nepal': 'NP',
        'Netherlands': 'NL',
        'New Caledonia': 'NC',
        'New Zealand': 'NZ',
        'Nicaragua': 'NI',
        'Niger': 'NE',
        'Nigeria': 'NG',
        'Niue': 'NU',
        'Norfolk Island': 'NF',
        'Northern Mariana Islands': 'MP',
        'Norway': 'NO',
        'Oman': 'OM',
        'Pakistan': 'PK',
        'Palau': 'PW',
        'Palestine, State of': 'PS',
        'Panama': 'PA',
        'Papua New Guinea': 'PG',
        'Paraguay': 'PY',
        'Peru': 'PE',
        'Philippines (the)': 'PH',
        'Pitcairn': 'PN',
        'Poland': 'PL',
        'Portugal': 'PT',
        'Puerto Rico': 'PR',
        'Qatar': 'QA',
        'Republic of North Macedonia': 'MK',
        'Romania': 'RO',
        'Russian Federation': 'RU',
        'Rwanda': 'RW',
        'Réunion': 'RE',
        'Saint Barthélemy': 'BL',
        'Saint Helena, Ascension and Tristan da Cunha': 'SH',
        'Saint Kitts and Nevis': 'KN',
        'Saint Lucia': 'LC',
        'Saint Martin': 'MF',
        'Saint Pierre and Miquelon': 'PM',
        'Saint Vincent and the Grenadines': 'VC',
        'Samoa': 'WS',
        'San Marino': 'SM',
        'Sao Tome and Principe': 'ST',
        'Saudi Arabia': 'SA',
        'Senegal': 'SN',
        'Serbia': 'RS',
        'Seychelles': 'SC',
        'Sierra Leone': 'SL',
        'Singapore': 'SG',
        'Sint Maarten': 'SX',
        'Slovakia': 'SK',
        'Slovenia': 'SI',
        'Solomon Islands': 'SB',
        'Somalia': 'SO',
        'South Africa': 'ZA',
        'South Georgia and the South Sandwich Islands': 'GS',
        'South Sudan': 'SS',
        'Spain': 'ES',
        'Sri Lanka': 'LK',
        'Sudan (the)': 'SD',
        'Suriname': 'SR',
        'Svalbard and Jan Mayen': 'SJ',
        'Sweden': 'SE',
        'Switzerland': 'CH',
        'Syrian Arab Republic': 'SY',
        'Taiwan': 'TW',
        'Tajikistan': 'TJ',
        'Tanzania, United Republic of': 'TZ',
        'Thailand': 'TH',
        'Timor-Leste': 'TL',
        'Togo': 'TG',
        'Tokelau': 'TK',
        'Tonga': 'TO',
        'Trinidad and Tobago': 'TT',
        'Tunisia': 'TN',
        'Turkey': 'TR',
        'Turkmenistan': 'TM',
        'Turks and Caicos Islands': 'TC',
        'Tuvalu': 'TV',
        'Uganda': 'UG',
        'Ukraine': 'UA',
        'United Arab Emirates': 'AE',
        'United Kingdom of Great Britain and Northern Ireland': 'GB',
        'United States Minor Outlying Islands': 'UM',
        'United States of America': 'US',
        'Uruguay': 'UY',
        'Uzbekistan': 'UZ',
        'Vanuatu': 'VU',
        'Venezuela': 'VE',
        'Viet Nam': 'VN',
        'Virgin Islands': 'VG',
        'Virgin Islands': 'VI',
        'Wallis and Futuna': 'WF',
        'Western Sahara': 'EH',
        'Yemen': 'YE',
        'Zambia': 'ZM',
        'Zimbabwe': 'ZW',
        'Åland Islands': 'AX'
    }

    valid_country = {country: code for country, code in countries.items() if code in regions}

    images = None
    countryFacts = None
>>>>>>> main
    existing_country = Country_Info.query.filter_by(Country=country).first()
    existing_city = Country_Info.query.filter_by(Country=country,City=city).first()
    if existing_country:
        if existing_city:
            info = country_city_info(country,city,True,True)
        else:
            info = country_city_info(country,city,True,False)
    else:
        info = country_city_info(country,city,False,False)
    return render_template('countryInformation.html', country=country,images = info[0], country_info = info[1], youtube_videos = info[2], temperature = info[3], mess = info[4],capital= info[5], ony= info[6], ony2= info[7])


def country_city_info(country,city,countryBool,cityBool):
    valid_country = {country: code for country, code in countries.items() if code in regions}
    images = None
    country_info = None
    attractions = None
    if countryBool:
        print("IF COUNTRYBOOL")
        #pull info for country
        images_str = Country_Info.query.filter_by(Country=country).first().Country_Images
        images = json.loads(images_str) 
        #country_info = {
            #Country_Info.query.filter_by(Country=country).first().Providence
        #}
        #country_info = 
        print(f"If Query_result worked: {images}")
        if cityBool:
            city_attractions = City_Attraction.query.filter_by(Country=country, City=city).all()
            print("IF CITYBOOL")
            if city_attractions:
                attractions = {
                    'attract1': [
                        city_attractions[0].Name,
                        city_attractions[0].Image,
                        city_attractions[0].Address,
                        city_attractions[0].Tags
                    ],
                    'attract2': [
                        city_attractions[1].Name if len(city_attractions) > 1 else None,
                        city_attractions[1].Image if len(city_attractions) > 1 else None,
                        city_attractions[1].Address if len(city_attractions) > 1 else None,
                        city_attractions[1].Tags if len(city_attractions) > 1 else None
                    ],
                    'attract3': [
                        city_attractions[2].Name if len(city_attractions) > 2 else None,
                        city_attractions[2].Image if len(city_attractions) > 2 else None,
                        city_attractions[2].Address if len(city_attractions) > 2 else None,
                        city_attractions[2].Tags if len(city_attractions) > 2 else None
                    ]
                }
                print(attractions)     
        else:
            attractions = get_attractions()
            for item in attractions: 
                attraction_image = getImages(item['name'],1)
                attraction_image = ast.literal_eval(attraction_image)
                attraction_information = City_Attraction(
                    City = city,
                    Country = country,
                    Image = attraction_image[0],
                    Name = item['name'],
                    Address = item['geoCode']['latitude'], 
                    Tags = json.dumps(item['tags']),
                    Summary = get_summary(item['name'])
                    )
            db.session.add(attraction_information)
            db.session.commit()
            query_result2 = City_Attraction.query.all()
            print("ELSE WHEN CITY BOOL FAILS: " + query_result2)
    else:
        images = getImages(country, 3)
        print(f"Else Block: for attractiosn and country info")
        images_str = json.dumps(images) 
        #country_info = search_country(country, list_of_names)
        country_information = Country_Info(
            Country=country,
            Country_Images=images_str,  
            City = city
            #Providence = country_info[2][1],
            #SubRegion = country_info[3][1],
            #Capital = country_info[4][1],
            #Time = country_info[8][1][0],
        )
        attractions = get_attractions()
        db.session.add(country_information)
        db.session.commit()
        for item in attractions: 
            attraction_image = getImages(item['name'],1)
            attraction_image = ast.literal_eval(attraction_image)
            attraction_information = City_Attraction(
                City = city,
                Country = country,
                Image = attraction_image[0],
                Name = item['name'],
                Address = item['geoCode']['latitude'], 
                Tags = json.dumps(item['tags']),
                Summary = get_summary(item['name'])
                )
            db.session.add(attraction_information)
            db.session.commit()
        query_result2 = City_Attraction.query.all()
        query_result = Country_Info.query.all()
        print(query_result)
        print(query_result2)
    query_result2 = City_Attraction.query.all()
    query_result = Country_Info.query.all()
    print(query_result)
    print(query_result2)
    country_info = search_country(country, list_of_names)
    images2 = images.split()
    images3 = ast.literal_eval(images)
    imagg1 = str(images3[0])
    imagg2 = str(images3[1])
    trending = TrendingVideos('AIzaSyAUTGuVJmt1eCA33Se8Nvu1Pl8_KYi8RdU')
    trending.get_most_popular_specific(valid_country[country],5)
    youtube_info = trending.get_video_information()
    capital_city = capital(country)
    temp = getWeatherCF(capital_city)
    messa = message(temp)
    return images,country_info,youtube_info,temp,messa,capital_city,imagg1,imagg2

def get_attractions():
    amadeus = Client(
    client_id='uj8JO5AizIUIzeAoK0vF3qAVcMNi5EfD',
    client_secret='dMudNMOE8FAcszeS'
    )
    response = []
    #try:
       # response = amadeus.reference_data.locations.points_of_interest.get(
           # latitude=41.397158, 
            #longitude=2.160873
        #)
        #print(response.data)
    #except ResponseError as error:
        #print(error)
    #print(response)
    return  [{'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '9CB40CB5D0', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/9CB40CB5D0', 'methods': ['GET']}, 'geoCode': {'latitude': 41.39165, 'longitude': 2.164772}, 'name': 'Casa Batlló', 'category': 'SIGHTS', 'rank': 5, 'tags': ['sightseeing', 'sights', 'museum', 'landmark', 'tourguide', 'restaurant', 'attraction', 'activities', 'commercialplace', 'shopping', 'souvenir']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '4690B83DCA', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/4690B83DCA', 'methods': ['GET']}, 'geoCode': {'latitude': 41.397987, 'longitude': 2.161159}, 'name': 'La Pepita', 'category': 'RESTAURANT', 'rank': 30, 'tags': ['restaurant', 'tapas', 'pub', 'bar', 'sightseeing', 'commercialplace']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '3EF139D861', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/3EF139D861', 'methods': ['GET']}, 'geoCode': {'latitude': 41.38827, 'longitude': 2.161604}, 'name': 'Brunch & Cake', 'category': 'RESTAURANT', 'rank': 30, 'tags': ['vegetarian', 'restaurant', 'breakfast', 'shopping', 'bakery', 'transport', 'patio', 'garden']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': 'AB3F122E3E', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/AB3F122E3E', 'methods': ['GET']}, 'geoCode': {'latitude': 41.392376, 'longitude': 2.160919}, 'name': 'Cervecería Catalana', 'category': 'RESTAURANT', 'rank': 30, 'tags': ['restaurant', 'tapas', 'sightseeing', 'traditionalcuisine', 'bar', 'activities', 'commercialplace']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '752402FCA2', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/752402FCA2', 'methods': ['GET']}, 'geoCode': {'latitude': 41.40043, 'longitude': 2.15463}, 'name': 'Botafumeiro', 'category': 'RESTAURANT', 'rank': 30, 'tags': ['restaurant', 'seafood', 'sightseeing', 'professionalservices', 'transport', 'commercialplace']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '5F1CED3994', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/5F1CED3994', 'methods': ['GET']}, 'geoCode': {'latitude': 41.39148, 'longitude': 2.164981}, 'name': 'Casa Amatller', 'category': 'SIGHTS', 'rank': 100, 'tags': ['sightseeing', 'sights', 'museum', 'landmark', 'restaurant', 'tourguide', 'historicplace', 'historic', 'attraction', 'commercialplace', 'activities', 'shopping', 'events']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '30601A1A90', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/30601A1A90', 'methods': ['GET']}, 'geoCode': {'latitude': 41.390785, 'longitude': 2.167414}, 'name': 'Tapas 24', 'category': 'RESTAURANT', 'rank': 100, 'tags': ['restaurant', 'tapas', 'traditionalcuisine', 'sightseeing', 'commercialplace', 'transport', 'patio', 'garden', 'activities', 'bar']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '15C8B8148C', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/15C8B8148C', 'methods': ['GET']}, 'geoCode': {'latitude': 41.392677, 'longitude': 2.153942}, 'name': 'Dry Martini', 'category': 'NIGHTLIFE', 'rank': 100, 'tags': ['bar', 'restaurant', 'nightlife', 'club', 'sightseeing', 'attraction', 'activities']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': 'BD29CF2CCD', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/BD29CF2CCD', 'methods': ['GET']}, 'geoCode': {'latitude': 41.399193, 'longitude': 2.159853}, 'name': 'Con Gracia', 'category': 'RESTAURANT', 'rank': 100, 'tags': ['restaurant', 'sightseeing', 'commercialplace', 'professionalservices', 'activities']}, {'type': 'location', 'subType': 'POINT_OF_INTEREST', 'id': '24DE6CE737', 'self': {'href': 'https://test.api.amadeus.com/v1/reference-data/locations/pois/24DE6CE737', 'methods': ['GET']}, 'geoCode': {'latitude': 41.390198, 'longitude': 2.156974}, 'name': 'Osmosis', 'category': 'RESTAURANT', 'rank': 100, 'tags': ['restaurant', 'shopping', 'transport', 'professionalservices']}]

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # checks if entries are valid
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            country_city = ''
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        session['logged_in']= True
        session['username']= form.username.data
        print(User.query.all())
        print(session['logged_in'])
        print(session['username'])
        return redirect(url_for('home'))  # if so - send to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['logged_in'] = True
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))

        flash('Login unsuccessful. Please check your username and password.', 'danger')

    return render_template('login.html', title='Login', form=form)
@app.route("/signout")
def signout():
    session.clear()  # Clear all session data
    return redirect(url_for('home'))  # Redirect to the home page

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    
