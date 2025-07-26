import uuid
from datetime import datetime, timezone
import logging
from ..models.tweet import Tweet

class TwitterService:
    def __init__(self, db_client):
        self.db = db_client
        self.collection_name = 'mock-twitter-feed'

    def _format_tweet_for_x_api(self, tweet_data):
        # Ensure author_id is a string
        tweet_data['author_id'] = str(tweet_data.get('author_id', ''))

        # Reformat created_at to X API format
        if 'created_at' in tweet_data and isinstance(tweet_data['created_at'], str):
            try:
                # Assuming current format is ISO 8601
                dt_object = datetime.fromisoformat(tweet_data['created_at'].replace('Z', '+00:00'))
                tweet_data['created_at'] = dt_object.strftime("%a %b %d %H:%M:%S +0000 %Y")
            except ValueError:
                pass # Keep as is if parsing fails

        # Ensure username and public_metrics are present
        tweet_data['username'] = tweet_data.get('username', '')
        tweet_data['public_metrics'] = tweet_data.get('public_metrics', {"retweet_count": 0, "reply_count": 0, "like_count": 0, "quote_count": 0})
        tweet_data['source'] = tweet_data.get('source', {"id": "", "name": ""})
        tweet_data['lang'] = tweet_data.get('lang', 'en')
        tweet_data['possibly_sensitive'] = tweet_data.get('possibly_sensitive', False)
        tweet_data['entities'] = tweet_data.get('entities', {})
        tweet_data['referenced_tweets'] = tweet_data.get('referenced_tweets', [])
        tweet_data['reply_settings'] = tweet_data.get('reply_settings', 'everyone')

        return tweet_data

    def get_all_tweets(self):
        logging.info(f"Fetching documents from '{self.collection_name}' collection.")
        items_ref = self.db.collection(self.collection_name).stream()
        items_list = [item.to_dict() for item in items_ref]
        
        formatted_tweets = [self._format_tweet_for_x_api(tweet) for tweet in items_list]
        logging.info(f"Retrieved {len(formatted_tweets)} tweets.")
        return formatted_tweets, 200

    def get_tweet_by_id(self, tweet_id):
        logging.info(f"Fetching tweet with id: {tweet_id} from '{self.collection_name}'.")
        query = self.db.collection(self.collection_name).where('id', '==', tweet_id).limit(1)
        docs = query.stream()
        item = next(docs, None)

        if item is None:
            return {"error": "Tweet not found."}, 404

        formatted_tweet = self._format_tweet_for_x_api(item.to_dict())
        return formatted_tweet, 200

    def add_tweet(self, tweet_data):
        # Generate ID and created_at in X API format before saving
        tweet_data['id'] = uuid.uuid4().hex
        tweet_data['created_at'] = datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S +0000 %Y")

        doc_ref = self.db.collection(self.collection_name).add(tweet_data)
        logging.info(f"Tweet added to Firestore with document ID: {doc_ref[1].id}")
        return {"status": "success", "message": "Tweet added to Firestore."}, 201

    def update_tweet(self, tweet_id, update_data):
        logging.info(f"Attempting to update tweet with id: {tweet_id} in '{self.collection_name}'.")
        query = self.db.collection(self.collection_name).where('id', '==', tweet_id).limit(1)
        docs = query.stream()
        item_to_update = next(docs, None)

        if item_to_update is None:
            return {"error": "Tweet not found."}, 404

        # Validate update data against the model (partial update)
        existing_data = item_to_update.to_dict()
        existing_data.update(update_data)
        validated_data = Tweet(**existing_data)

        item_to_update.reference.update(validated_data.model_dump())
        logging.info(f"Successfully updated tweet with id '{tweet_id}'.")
        return {"status": "success", "message": f"Tweet with id {tweet_id} updated successfully."}, 200

    def delete_tweet(self, tweet_id):
        logging.info(f"Attempting to delete tweet with id: {tweet_id} from '{self.collection_name}'.")
        query = self.db.collection(self.collection_name).where('id', '==', tweet_id).limit(1)
        docs = query.stream()
        item_to_delete = next(docs, None)

        if item_to_delete is None:
            return {"error": "Tweet not found."}, 404

        item_to_delete.reference.delete()
        logging.info(f"Successfully deleted tweet with id '{tweet_id}'.")
        return {"status": "success", "message": f"Tweet with id {tweet_id} deleted successfully."}
