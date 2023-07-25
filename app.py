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
import json
from attractions_api import get_attractions
from attractions_api import get_flights
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
    if session.get("logged_in", False):
        name = session.get('username')
        logged_in_user = User.query.filter_by(username=name).first()
        if logged_in_user:
            country_city_list = logged_in_user.country_city.split('.') if logged_in_user.country_city else []
            if [country, city] not in [entry.split(',') for entry in country_city_list]:
                logged_in_user.country_city += f"{country},{city}."
                db.session.commit()
                print("Updated country_city:", logged_in_user.country_city)
    existing_country = Country_Info.query.filter_by(Country=country).first()
    existing_city = Country_Info.query.filter_by(Country=country,City=city).first()
    if existing_country:
        if existing_city:
            info = country_city_info(country,city,True,True)
        else:
            info = country_city_info(country,city,True,False)
    else:
        info = country_city_info(country,city,False,False)
    return render_template('countryInformation.html', city=city,country=country,images = info[0], country_info = info[1], youtube_videos = info[2], temperature = info[3], mess = info[4],capital= info[5], ony= info[6], ony2= info[7],attractions = info[8])

def country_city_info(country,city,countryBool,cityBool):
    valid_country = {country: code for country, code in countries.items() if code in regions}
    images = None
    country_info = None
    attractions = None
    if countryBool:
        print("IF COUNTRYBOOL")
        images_str = Country_Info.query.filter_by(Country=country).first().Country_Images
        images = json.loads(images_str) 
        print(f"If Query_result worked: {images}")
        if cityBool:
            attractions = create_attractions(city,country)    
        else:
            store_attractions(city,country)
            attractions = create_attractions(city,country)
            query_result2 = City_Attraction.query.all()
    else:
        images = getImages(country, 3)
        print(f"Else Block: for attractiosn and country info")
        images_str = json.dumps(images)
        store_attractions(city,country)
        attractions = create_attractions(city,country)
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
    if country not in valid_country.keys():
        youtube_info = None
    else:
        trending.get_most_popular_specific(valid_country[country],5)
        youtube_info = trending.get_video_information()
    temp = getWeatherCF(city)
    messa = message(temp)
    return images,country_info,youtube_info,temp,messa, None, imagg1,imagg2,attractions

def create_attractions(city,country):
    city_attractions = City_Attraction.query.filter_by(Country=country, City=city).all()
    if city_attractions:
        attractions = {
            'attract1': [
                city_attractions[0].Name,
                city_attractions[0].Image,
                city_attractions[0].Address,
                ast.literal_eval(city_attractions[0].Tags)
            ],
            'attract2': [
                city_attractions[1].Name if len(city_attractions) > 1 else None,
                city_attractions[1].Image if len(city_attractions) > 1 else None,
                city_attractions[1].Address if len(city_attractions) > 1 else None,
                ast.literal_eval(city_attractions[1].Tags) if len(city_attractions) > 1 else None
            ],
            'attract3': [
                city_attractions[2].Name if len(city_attractions) > 2 else None,
                city_attractions[2].Image if len(city_attractions) > 2 else None,
                city_attractions[2].Address if len(city_attractions) > 2 else None,
                ast.literal_eval(city_attractions[2].Tags) if len(city_attractions) > 2 else None
            ]
        }
        return attractions
    else:
        return None
    
def store_attractions(city,country):
    attractions = get_attractions(city,country)
    if attractions is None:
        return None
    else: 
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
        return True

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

@app.route('/get_ticket_info', methods=['POST'])
def get_ticket_info():
    data = request.get_json()
    departure = data['departure']
    arrival = data['arrival']
    travel_date = data['travelDate']
    passengers = data['passengers']
    print(data)
    ticket_info = get_flights(departure,arrival,travel_date,passengers)
    print(ticket_info)
    return ticket_info

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    
