from flask import Flask, render_template
import logging
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

from .routes.tweet_routes import create_tweet_blueprint
from .routes.news_routes import create_news_blueprint
from .routes.event_routes import create_event_blueprint
from .routes.weather_routes import create_weather_blueprint
from .routes.user_routes import create_user_blueprint
from .utils.db_initializer import initialize_tweets, initialize_news, initialize_users, initialize_events, initialize_weather

# --- Firebase Admin SDK Initialization ---
# Initialize Firebase Admin SDK using default application credentials.
# This will automatically pick up the service account attached to the Cloud Run service.
firebase_admin.initialize_app()
db = firestore.client()
# -----------------------------------------

# --- Global Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# --- Initialize Database ---
initialize_tweets(db)
initialize_news(db)
initialize_users(db)
initialize_events(db)
initialize_weather(db)

# --- Register Blueprints ---
app.register_blueprint(create_tweet_blueprint(db))
app.register_blueprint(create_news_blueprint(db))
app.register_blueprint(create_event_blueprint(db))
app.register_blueprint(create_weather_blueprint(db))
app.register_blueprint(create_user_blueprint(db))

# --- UI Route ---
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)