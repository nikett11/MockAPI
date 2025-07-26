from flask import Blueprint, jsonify, request
from ..services.user_service import UserService
from ..models.user import User

def create_user_blueprint(db):
    user_routes = Blueprint('user_routes', __name__)
    user_service = UserService(db)

    @user_routes.route('/mock-users', methods=['GET'])
    def get_users():
        response_data, status_code = user_service.get_all_users()
        return jsonify(response_data), status_code

    @user_routes.route('/mock-users/<string:id>', methods=['GET'])
    def get_user_by_id(id):
        response_data, status_code = user_service.get_user_by_id(id)
        return jsonify(response_data), status_code

    @user_routes.route('/mock-users', methods=['POST'])
    def add_user():
        try:
            response_data, status_code = user_service.add_user()
            return jsonify(response_data), status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @user_routes.route('/mock-users/<string:id>', methods=['PUT'])
    def update_user(id):
        try:
            response_data, status_code = user_service.update_user(id)
            return jsonify(response_data), status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @user_routes.route('/mock-users/<string:id>', methods=['DELETE'])
    def delete_user(id):
        response_data, status_code = user_service.delete_user(id)
        return jsonify(response_data), status_code

    return user_routes
