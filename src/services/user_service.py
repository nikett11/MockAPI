from ..services.firestore_service import FirestoreCRUD
from ..models.user import User
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

def post_add_user_hook(item_data):
    # Generate created_at in ISO 8601 format
    item_data['created_at'] = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

class UserService(FirestoreCRUD):
    def __init__(self, db_client):
        super().__init__(db_client, 'mock-users-feed', User, post_add=post_add_user_hook)

    def get_all_users(self):
        return self.get_all()

    def get_user_by_id(self, user_id):
        return self.get_by_id(user_id)

    def add_user(self):
        return self.add_item()

    def update_user(self, user_id):
        return self.update_item(user_id)

    def delete_user(self, user_id):
        return self.delete_item(user_id)
