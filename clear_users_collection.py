import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clear_collection(collection_name):
    try:
        # Load credentials from environment variable
        service_account_info = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON'))
        cred = credentials.Certificate(service_account_info)

        # Initialize Firebase app if not already initialized
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        collection_ref = db.collection(collection_name)

        # Get all documents in the collection
        docs = collection_ref.stream()
        deleted_count = 0

        for doc in docs:
            doc.reference.delete()
            deleted_count += 1
            logging.info(f"Deleted document: {doc.id}")

        logging.info(f"Successfully deleted {deleted_count} documents from collection '{collection_name}'.")

    except KeyError:
        logging.error("GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable not set.")
    except json.JSONDecodeError:
        logging.error("GOOGLE_APPLICATION_CREDENTIALS_JSON is not a valid JSON string.")
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    collection_to_clear = 'mock-users-feed'  # Specify the collection name for users
    clear_collection(collection_to_clear)
