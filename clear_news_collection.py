import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    service_account_info = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON'))
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    collection_ref = db.collection('mock-news-feed')
    docs = collection_ref.stream()

    for doc in docs:
        doc.reference.delete()
        logging.info(f"Deleted document: {doc.id}")

    logging.info("Collection 'mock-news-feed' cleared.")

except Exception as e:
    logging.error(f"Error clearing collection: {e}", exc_info=True)
