import json
import os
import random
from datetime import datetime, timezone, timedelta
import logging
import uuid

logger = logging.getLogger(__name__)

def initialize_tweets(db_client):
    collection_ref = db_client.collection('mock-twitter-feed')
    
    # Check if collection is empty
    if next(collection_ref.limit(1).stream(), None) is None:
        logger.info("'mock-twitter-feed' collection is empty. Initializing with sample data.")
        
        try:
            with open('sample_tweets_bangalore.json', 'r', encoding='utf-8') as f:
                sample_tweets = json.load(f)
            
            today = datetime.now(timezone.utc).date()

            for tweet_data in sample_tweets:
                # Generate random time for today
                random_hour = random.randint(0, 23)
                random_minute = random.randint(0, 59)
                random_second = random.randint(0, 59)
                random_time = datetime(today.year, today.month, today.day, 
                                       random_hour, random_minute, random_second, 
                                       tzinfo=timezone.utc)
                
                # Format created_at to X API format
                tweet_data['created_at'] = random_time.strftime("%a %b %d %H:%M:%S +0000 %Y")
                
                # Generate unique ID
                tweet_data['id'] = uuid.uuid4().hex
                
                collection_ref.add(tweet_data)
            logger.info(f"Successfully added {len(sample_tweets)} sample tweets to 'mock-twitter-feed'.")
        except FileNotFoundError:
            logger.error("sample_tweets_bangalore.json not found. Cannot initialize tweets.")
        except Exception as e:
            logger.error(f"Error initializing tweets: {e}", exc_info=True)
    else:
        logger.info("'mock-twitter-feed' collection is not empty. Skipping initialization.")

def initialize_news(db_client):
    collection_ref = db_client.collection('mock-news-feed')

    # Check if collection is empty
    if next(collection_ref.limit(1).stream(), None) is None:
        logger.info("'mock-news-feed' collection is empty. Initializing with sample data.")
        logger.info(f"Attempting to open sample_news_bangalore.json from: {os.getcwd()}") # Added for debugging

        try:
            with open('sample_news_bangalore.json', 'r', encoding='utf-8') as f:
                sample_news = json.load(f)

            today = datetime.now(timezone.utc).date()

            for news_data in sample_news:
                # Generate random time for today
                random_hour = random.randint(0, 23)
                random_minute = random.randint(0, 59)
                random_second = random.randint(0, 59)
                random_time = datetime(today.year, today.month, today.day,
                                       random_hour, random_minute, random_second,
                                       tzinfo=timezone.utc)

                # Format publishedAt to ISO format
                news_data['publishedAt'] = random_time.isoformat(timespec='seconds').replace('+00:00', 'Z')

                # Generate unique ID
                news_data['id'] = uuid.uuid4().hex

                collection_ref.add(news_data)
            logger.info(f"Successfully added {len(sample_news)} sample news articles to 'mock-news-feed'.")
        except FileNotFoundError:
            logger.error("sample_news_bangalore.json not found. Cannot initialize news.")
        except Exception as e:
            logger.error(f"Error initializing news: {e}", exc_info=True)
    else:
        logger.info("'mock-news-feed' collection is not empty. Skipping initialization.")

def initialize_users(db_client):
    collection_ref = db_client.collection('mock-users-feed')

    # Check if collection is empty
    if next(collection_ref.limit(1).stream(), None) is None:
        logger.info("'mock-users-feed' collection is empty. Initializing with sample data.")

        try:
            with open('sample_users_bangalore.json', 'r', encoding='utf-8') as f:
                sample_users = json.load(f)

            for user_data in sample_users:
                # The sample data already contains 'created_at', so no need to generate
                collection_ref.add(user_data)
            logger.info(f"Successfully added {len(sample_users)} sample users to 'mock-users-feed'.")
        except FileNotFoundError:
            logger.error("sample_users_bangalore.json not found. Cannot initialize users.")
        except Exception as e:
            logger.error(f"Error initializing users: {e}", exc_info=True)
    else:
        logger.info("'mock-users-feed' collection is not empty. Skipping initialization.")

def initialize_events(db_client):
    collection_ref = db_client.collection('mock-events-feed')

    # Check if collection is empty
    if next(collection_ref.limit(1).stream(), None) is None:
        logger.info("'mock-events-feed' collection is empty. Initializing with sample data.")

        try:
            with open('sample_events_bangalore.json', 'r', encoding='utf-8') as f:
                sample_events = json.load(f)

            base_date = datetime.now(timezone.utc)

            for event_data in sample_events:
                # Adjust start_date to be within a week of the current date
                original_start_date = datetime.fromisoformat(event_data['start_date'].replace('Z', '+00:00'))
                days_offset = (original_start_date.date() - base_date.date()).days
                
                # Ensure events are within the next 7 days from base_date
                if days_offset < 0 or days_offset > 6:
                    # If event is in the past or too far in the future, adjust it
                    adjusted_start_date = base_date + timedelta(days=random.randint(0, 6))
                    event_data['start_date'] = adjusted_start_date.replace(hour=original_start_date.hour, minute=original_start_date.minute, second=original_start_date.second).isoformat(timespec='seconds').replace('+00:00', 'Z')
                else:
                    # Keep original time, but ensure date is relative to base_date
                    event_data['start_date'] = original_start_date.isoformat(timespec='seconds').replace('+00:00', 'Z')

                # Calculate end_date if duration_hours is present
                if "duration_hours" in event_data:
                    start_dt = datetime.fromisoformat(event_data['start_date'].replace('Z', '+00:00'))
                    end_dt = start_dt + timedelta(hours=event_data['duration_hours'])
                    event_data['end_date'] = end_dt.isoformat(timespec='seconds').replace('+00:00', 'Z')
                    del event_data['duration_hours'] # Remove duration_hours as it's not part of the model
                
                # Generate unique ID
                event_data['id'] = uuid.uuid4().hex

                collection_ref.add(event_data)
            logger.info(f"Successfully added {len(sample_events)} sample events to 'mock-events-feed'.")
        except FileNotFoundError:
            logger.error("sample_events_bangalore.json not found. Cannot initialize events.")
        except Exception as e:
            logger.error(f"Error initializing events: {e}", exc_info=True)
    else:
        logger.info("'mock-events-feed' collection is not empty. Skipping initialization.")

def initialize_weather(db_client):
    collection_ref = db_client.collection('mock-weather-feed')

    # Check if collection is empty
    if next(collection_ref.limit(1).stream(), None) is None:
        logger.info("'mock-weather-feed' collection is empty. Initializing with sample data.")

        try:
            with open('sample_weather_bangalore.json', 'r', encoding='utf-8') as f:
                sample_weather = json.load(f)

            for weather_data in sample_weather:
                # Generate unique ID
                weather_data['id'] = uuid.uuid4().hex

                collection_ref.add(weather_data)
            logger.info(f"Successfully added {len(sample_weather)} sample weather entries to 'mock-weather-feed'.")
        except FileNotFoundError:
            logger.error("sample_weather_bangalore.json not found. Cannot initialize weather.")
        except Exception as e:
            logger.error(f"Error initializing weather: {e}", exc_info=True)
    else:
        logger.info("'mock-weather-feed' collection is not empty. Skipping initialization.")