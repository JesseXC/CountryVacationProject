from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from youtube_api import TrendingVideos
from Take2 import getWeatherCF, message, capital
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '7753df06aa5ee8fc7318aada4d2fafaa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

with app.app_context():
    db.create_all()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/countryInformation")
def country_information():
    country = request.args.get('country')
    trending = TrendingVideos('AIzaSyAUTGuVJmt1eCA33Se8Nvu1Pl8_KYi8RdU')
    trending.get_most_popular_specific("US",5)
    youtube_info = trending.get_video_information()
    capital_city = capital(country)
    temp = getWeatherCF(capital_city)
    messa = message(temp)
    print(capital_city)
    return render_template('countryInformation.html', country=country,youtube_videos=youtube_info, temperature=temp, mess=messa, capital=capital_city)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # checks if entries are valid
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))  # if so - send to home page
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
