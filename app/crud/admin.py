from app.model.models import Admin
from app.schemas.schemas import admin_serial
from app.config.database import admin_db
from bson import ObjectId
from pymongo.errors import PyMongoError

def get_admin_username(username):
    query = {'username':username}
    admin = admin_db.find_one(query)
    if admin:
        return admin_serial(admin)
    return None



def update_admin(admin:str, new_password: str):
    query = {'username':admin}
    update = {
        '$set': {
            'password': new_password
        }
    }
    try:
        result = admin_db.update_one(query, update)
        return result.modified_count > 0
    except Exception as e:
        print(f"Error updating admin: {e}")
        return False