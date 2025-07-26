# City Pulse Mock API

This project provides a mock API for the City Pulse application, simulating various data feeds (tweets, news, events, weather, users) using Flask and Firestore.

## Project Structure

- `app.py`: Main Flask application.
- `src/models/`: Pydantic models for data validation.
- `src/routes/`: Flask Blueprints for API endpoints.
- `src/services/`: Business logic for Firestore interactions.
- `src/utils/db_initializer.py`: Initializes Firestore collections with sample data.
- `sample_*.json`: Sample data files for initialization.
- `clear_*.py`: Scripts to clear Firestore collections.
- `docker-compose.yml`: Docker Compose configuration for local development.
- `Dockerfile`: Dockerfile for building the application image.
- `MockAPI.postman_collection.json`: Postman collection for API testing.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Google Cloud Project with Firestore enabled
- A service account key for your Google Cloud Project (downloaded as a JSON file)

### Setup

1.  **Place your Google Service Account Key:**
    Rename your service account JSON key file to `service_account.json` and place it in the root directory of this project.

2.  **Set Environment Variable:**
    The `GOOGLE_APPLICATION_CREDENTIALS_JSON` environment variable needs to be set with the content of your `service_account.json` file. This is handled by the `.env` file and `docker-compose.yml`.

    Create a `.env` file in the root directory with the following content:
    ```
    GOOGLE_APPLICATION_CREDENTIALS_JSON='<content_of_your_service_account.json>'
    ```
    **Note:** Replace `<content_of_your_service_account.json>` with the actual JSON content of your service account key file. Ensure it's a single line and properly escaped if necessary (though usually not needed for direct JSON string). Alternatively, you can set this environment variable directly in your shell before running Docker Compose.

3.  **Build and Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    This will build the Docker image, start the Flask application, and initialize the Firestore collections with sample data if they are empty.

## API Endpoints

The API will be available at `http://localhost:8080`.

### Tweets
-   `GET /mock-tweets`: Get all tweets.
-   `GET /mock-tweets/{id}`: Get a tweet by ID.
-   `POST /mock-tweets`: Add a new tweet.
-   `PUT /mock-tweets/{id}`: Update a tweet by ID.
-   `DELETE /mock-tweets/{id}`: Delete a tweet by ID.

### News
-   `GET /mock-news`: Get all news articles.
-   `GET /mock-news/{id}`: Get a news article by ID.
-   `POST /mock-news`: Add a new news article.
-   `PUT /mock-news/{id}`: Update a news article by ID.
-   `DELETE /mock-news/{id}`: Delete a news article by ID.

### Events
-   `GET /mock-events`: Get all events.
-   `GET /mock-events/{id}`: Get an event by ID.
-   `POST /mock-events`: Add a new event.
-   `PUT /mock-events/{id}`: Update an event by ID.
-   `DELETE /mock-events/{id}`: Delete an event by ID.

### Weather
-   `GET /mock-weather`: Get all weather forecasts.
-   `GET /mock-weather/{id}`: Get a weather forecast by ID.
-   `POST /mock-weather`: Add a new weather forecast.
-   `PUT /mock-weather/{id}`: Update a weather forecast by ID.
-   `DELETE /mock-weather/{id}`: Delete a weather forecast by ID.

### Users
-   `GET /mock-users`: Get all users.
-   `GET /mock-users/{id}`: Get a user by ID.
-   `POST /mock-users`: Add a new user.
-   `PUT /mock-users/{id}`: Update a user by ID.
-   `DELETE /mock-users/{id}`: Delete a user by ID.

## Clearing Firestore Collections

To clear specific Firestore collections, you can use the provided scripts:

-   `clear_collection.py`: Clears the `mock-twitter-feed` collection.
-   `clear_news_collection.py`: Clears the `mock-news-feed` collection.
-   `clear_events_collection.py`: Clears the `mock-events-feed` collection.
-   `clear_weather_collection.py`: Clears the `mock-weather-feed` collection.
-   `clear_users_collection.py`: Clears the `mock-users-feed` collection.

To run these scripts using Docker Compose:

```bash
docker-compose run --rm web python clear_collection.py
docker-compose run --rm web python clear_news_collection.py
docker-compose run --rm web python clear_events_collection.py
docker-compose run --rm web python clear_weather_collection.py
docker-compose run --rm web python clear_users_collection.py
```

## Postman Collection

The `MockAPI.postman_collection.json` file contains a Postman collection with all the API endpoints and example requests. You can import this file into Postman to easily test the API.
