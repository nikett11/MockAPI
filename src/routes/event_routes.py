from flask import Blueprint, jsonify, request
from ..services.firestore_service import FirestoreCRUD
from ..models.event import Event

def create_event_blueprint(db):
    event_routes = Blueprint('event_routes', __name__)

    events_crud = FirestoreCRUD(db, 'mock-events-feed', Event)

    @event_routes.route('/mock-events', methods=['GET'])
    def get_events():
        response_data, status_code = events_crud.get_all()
        return jsonify(response_data), status_code

    @event_routes.route('/mock-events/<string:id>', methods=['GET'])
    def get_event_by_id(id):
        response_data, status_code = events_crud.get_by_id(id)
        return jsonify(response_data), status_code

    @event_routes.route('/mock-events', methods=['POST'])
    def add_event():
        try:
            response_data, status_code = events_crud.add_item()
            return jsonify(response_data), status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @event_routes.route('/mock-events/<string:id>', methods=['PUT'])
    def update_event(id):
        try:
            response_data, status_code = events_crud.update_item(id)
            return jsonify(response_data), status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @event_routes.route('/mock-events/<string:id>', methods=['DELETE'])
    def delete_event(id):
        response_data, status_code = events_crud.delete_item(id)
        return jsonify(response_data), status_code

    return event_routes