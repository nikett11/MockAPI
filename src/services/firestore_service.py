import uuid
from datetime import datetime, timezone
from flask import request
import logging
import firebase_admin
from firebase_admin import firestore

class FirestoreCRUD:
    def __init__(self, db_client, collection_name, model, post_add=None):
        self.db = db_client
        self.collection_name = collection_name
        self.model = model
        self.post_add = post_add

    def get_all(self):
        try:
            logging.info(f"Fetching documents from '{self.collection_name}' collection.")
            items_ref = self.db.collection(self.collection_name).stream()
            items_list = [item.to_dict() for item in items_ref]

            logging.info(f"Retrieved {len(items_list)} items.")
            return items_list, 200
        except firebase_admin.exceptions.FirebaseError as e:
            logging.error(f"Error fetching items from '{self.collection_name}': {e}", exc_info=True)
            return {"error": f"A database error occurred."}, 500

    def get_by_id(self, id):
        try:
            logging.info(f"Fetching document with id: {id} from '{self.collection_name}'.")
            query = self.db.collection(self.collection_name).where('id', '==', id).limit(1)
            docs = query.stream()
            item = next(docs, None)

            if item is None:
                return {"error": "Item not found."}, 404

            return item.to_dict(), 200
        except firebase_admin.exceptions.FirebaseError as e:
            logging.error(f"Error fetching item with id {id} from '{self.collection_name}': {e}", exc_info=True)
            return {"error": f"A database error occurred."}, 500
    def add_item(self):
        try:
            new_item_data = request.get_json()
            validated_data = self.model(**new_item_data)

            # Convert Pydantic model to dictionary for Firestore
            item_to_save = validated_data.model_dump()

            # Generate ID and apply post_add hook to the dictionary
            item_to_save['id'] = uuid.uuid4().hex
            if self.post_add:
                self.post_add(item_to_save)

            doc_ref = self.db.collection(self.collection_name).add(item_to_save)
            logging.info(f"Item added to '{self.collection_name}' with document ID: {doc_ref[1].id}")
            return {"status": "success", "message": f"Item added to '{self.collection_name}'."}, 201
        except ValueError as e:
            logging.warning(f"Invalid data received for '{self.collection_name}': {e}")
            return {"error": str(e)}, 400
        except firebase_admin.exceptions.FirebaseError as e:
            logging.error(f"Error adding item to '{self.collection_name}': {e}", exc_info=True)
            return {"error": f"A database error occurred."}, 500
    def update_item(self, id):
        try:
            update_data = request.get_json()
            if not isinstance(update_data, dict) or not update_data:
                return {"error": "Invalid JSON format for update."}, 400

            query = self.db.collection(self.collection_name).where('id', '==', id).limit(1)
            docs = query.stream()
            item_to_update = next(docs, None)

            if item_to_update is None:
                return {"error": "Item not found."}, 404

            # Validate update data against the model (partial update)
            # Fetch existing data, apply updates, then validate
            existing_data = item_to_update.to_dict()
            existing_data.update(update_data)
            validated_data = self.model(**existing_data)

            item_to_update.reference.update(validated_data.model_dump())
            logging.info(f"Successfully updated item with id '{id}' in '{self.collection_name}'.")
            return {"status": "success", "message": f"Item with id {id} updated successfully."}, 200
        except ValueError as e:
            logging.warning(f"Invalid data received for update in '{self.collection_name}': {e}")
            return {"error": str(e)}, 400
        except firebase_admin.exceptions.FirebaseError as e:
            logging.error(f"Error updating item with id {id} in '{self.collection_name}': {e}", exc_info=True)
            return {"error": f"A database error occurred."}, 500
    def delete_item(self, id):
        try:
            logging.info(f"Attempting to delete item with id: {id} from '{self.collection_name}'.")
            query = self.db.collection(self.collection_name).where('id', '==', id).limit(1)
            docs = query.stream()
            item_to_delete = next(docs, None)

            if item_to_delete is None:
                return {"error": "Item not found."}, 404

            item_to_delete.reference.delete()
            logging.info(f"Successfully deleted item with id '{id}'.")
            return {"status": "success", "message": f"Item with id {id} deleted successfully."},
        except firebase_admin.exceptions.FirebaseError as e:
            logging.error(f"Error deleting item with id {id} from '{self.collection_name}': {e}", exc_info=True)
            return {"error": f"Failed to delete item from '{self.collection_name}'."}, 500