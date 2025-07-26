from flask import Blueprint, jsonify, request
from ..services.firestore_service import FirestoreCRUD
from ..models.weather import Weather

def create_weather_blueprint(db):
    weather_routes = Blueprint('weather_routes', __name__)

    weather_crud = FirestoreCRUD(db, 'mock-weather-feed', Weather)

    @weather_routes.route('/mock-weather', methods=['GET'])
    def get_weather():
        response_data, status_code = weather_crud.get_all()
        return jsonify(response_data), status_code

    @weather_routes.route('/mock-weather/<string:id>', methods=['GET'])
    def get_weather_by_id(id):
        response_data, status_code = weather_crud.get_by_id(id)
        return jsonify(response_data), status_code

    @weather_routes.route('/mock-weather', methods=['POST'])
    def add_weather():
        try:
            response_data, status_code = weather_crud.add_item()
            return jsonify(response_data), status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @weather_routes.route('/mock-weather/<string:id>', methods=['PUT'])
    def update_weather(id):
        try:
            response_data, status_code = weather_crud.update_item(id)
            return jsonify(response_data), status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @weather_routes.route('/mock-weather/<string:id>', methods=['DELETE'])
    def delete_weather(id):
        response_data, status_code = weather_crud.delete_item(id)
        return jsonify(response_data), status_code

    return weather_routes