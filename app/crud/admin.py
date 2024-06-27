from app.schemas.schemas import admin_serial
from app.config.database import admin_db
from bson import ObjectId

def get_admin_username(username):
    query = {'username':username}
    try:
        return admin_serial(admin_db.find_one(query))
    except:
        return None