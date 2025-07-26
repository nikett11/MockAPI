from flask import Blueprint, jsonify, request
from ..services.twitter_service import TwitterService
from ..models.tweet import Tweet

def create_tweet_blueprint(db):
    tweet_routes = Blueprint('tweet_routes', __name__)
    twitter_service = TwitterService(db)

    @tweet_routes.route('/mock-tweets', methods=['GET'])
    def get_tweets():
        response_data, status_code = twitter_service.get_all_tweets()
        return jsonify(response_data), status_code

    @tweet_routes.route('/mock-tweets/<string:id>', methods=['GET'])
    def get_tweet_by_id(id):
        response_data, status_code = twitter_service.get_tweet_by_id(id)
        return jsonify(response_data), status_code

    @tweet_routes.route('/mock-tweets', methods=['POST'])
    def add_tweet():
        try:
            new_tweet_data = request.get_json()
            # Validate with Pydantic model first
            validated_tweet = Tweet(**new_tweet_data)
            response_data, status_code = twitter_service.add_tweet(validated_tweet.model_dump())
            return jsonify(response_data), status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @tweet_routes.route('/mock-tweets/<string:id>', methods=['PUT'])
    def update_tweet(id):
        try:
            update_data = request.get_json()
            response_data, status_code = twitter_service.update_tweet(id, update_data)
            return jsonify(response_data), status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @tweet_routes.route('/mock-tweets/<string:id>', methods=['DELETE'])
    def delete_tweet(id):
        response_data, status_code = twitter_service.delete_tweet(id)
        return jsonify(response_data), status_code

    return tweet_routes