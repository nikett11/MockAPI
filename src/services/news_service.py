import uuid
from datetime import datetime, timezone
import logging
from ..models.news import News

class NewsService:
    def __init__(self, db_client):
        self.db = db_client
        self.collection_name = 'mock-news-feed'

    def _format_news_for_api(self, news_data):
        # Ensure source is an object with id and name
        if not isinstance(news_data.get('source'), dict):
            news_data['source'] = {"id": "", "name": str(news_data.get('source', ''))}
        else:
            news_data['source']['id'] = news_data['source'].get('id', '')
            news_data['source']['name'] = news_data['source'].get('name', '')

        # Ensure urlToImage is present (can be None)
        news_data['urlToImage'] = news_data.get('urlToImage', None)

        # Ensure other fields are present with defaults
        news_data['author'] = news_data.get('author', '')
        news_data['title'] = news_data.get('title', '')
        news_data['description'] = news_data.get('description', '')
        news_data['url'] = news_data.get('url', '')
        news_data['content'] = news_data.get('content', '')

        return news_data

    def get_all_news(self):
        logging.info(f"Fetching documents from '{self.collection_name}' collection.")
        items_ref = self.db.collection(self.collection_name).stream()
        items_list = [item.to_dict() for item in items_ref]
        
        formatted_news = [self._format_news_for_api(news) for news in items_list]
        logging.info(f"Retrieved {len(formatted_news)} news articles.")
        return formatted_news, 200

    def get_news_by_id(self, news_id):
        logging.info(f"Fetching news article with id: {news_id} from '{self.collection_name}'.")
        query = self.db.collection(self.collection_name).where('id', '==', news_id).limit(1)
        docs = query.stream()
        item = next(docs, None)

        if item is None:
            return {"error": "News article not found."}, 404

        formatted_news = self._format_news_for_api(item.to_dict())
        return formatted_news, 200

    def add_news(self, news_data):
        # Generate ID and publishedAt before saving
        news_data['id'] = uuid.uuid4().hex
        news_data['publishedAt'] = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

        doc_ref = self.db.collection(self.collection_name).add(news_data)
        logging.info(f"News article added to Firestore with document ID: {doc_ref[1].id}")
        return {"status": "success", "message": "News article added to Firestore."}, 201

    def update_news(self, news_id, news_data):
        logging.info(f"Attempting to update news article with id: {news_id} in '{self.collection_name}'.")
        query = self.db.collection(self.collection_name).where('id', '==', news_id).limit(1)
        docs = query.stream()
        item_to_update = next(docs, None)

        if item_to_update is None:
            return {"error": "News article not found."}, 404

        # Validate update data against the model (partial update)
        existing_data = item_to_update.to_dict()
        existing_data.update(news_data)
        validated_data = News(**existing_data)

        item_to_update.reference.update(validated_data.model_dump())
        logging.info(f"Successfully updated news article with id '{news_id}'.")
        return {"status": "success", "message": f"News article with id {news_id} updated successfully."}, 200

    def delete_news(self, news_id):
        logging.info(f"Attempting to delete news article with id: {news_id} from '{self.collection_name}'.")
        query = self.db.collection(self.collection_name).where('id', '==', news_id).limit(1)
        docs = query.stream()
        item_to_delete = next(docs, None)

        if item_to_delete is None:
            return {"error": "News article not found."}, 404

        item_to_delete.reference.delete()
        logging.info(f"Successfully deleted news article with id '{news_id}'.")
        return {"status": "success", "message": f"News article with id {news_id} deleted successfully."}, 200