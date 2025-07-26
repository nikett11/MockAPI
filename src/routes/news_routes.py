from flask import Blueprint, jsonify, request
from ..services.news_service import NewsService
from ..models.news import News

def create_news_blueprint(db):
    news_routes = Blueprint('news_routes', __name__)
    news_service = NewsService(db)

    @news_routes.route('/mock-news', methods=['GET'])
    def get_news():
        response_data, status_code = news_service.get_all_news()
        return jsonify(response_data), status_code

    @news_routes.route('/mock-news/<string:id>', methods=['GET'])
    def get_news_by_id(id):
        response_data, status_code = news_service.get_news_by_id(id)
        return jsonify(response_data), status_code

    @news_routes.route('/mock-news', methods=['POST'])
    def add_news():
        try:
            new_news_data = request.get_json()
            # Validate with Pydantic model first
            validated_news = News(**new_news_data)
            response_data, status_code = news_service.add_news(validated_news.model_dump())
            return jsonify(response_data), status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @news_routes.route('/mock-news/<string:id>', methods=['PUT'])
    def update_news(id):
        try:
            update_data = request.get_json()
            response_data, status_code = news_service.update_news(id, update_data)
            return jsonify(response_data), status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @news_routes.route('/mock-news/<string:id>', methods=['DELETE'])
    def delete_news(id):
        response_data, status_code = news_service.delete_news(id)
        return jsonify(response_data), status_code

    return news_routes