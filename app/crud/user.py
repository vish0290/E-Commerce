from app.models.models import User
from app.schema.schemas import list_user,user_serial
from app.config.database import user_db
from bson import ObjectId

def get_user(user_id):
    query = {'_id':ObjectId(user_id)}
    user = user_serial(user_db.find_one(query))
    return user

def all_user():
    users = list_user(user_db.find())
    return users

def add_user(user: User):
    user_db.insert_one(dict(user))

def update_user(user: User,id):
    query = {'_id':id}
    user_db.find_one_and_update(query,dict(user))

def del_user(user_id):
    query = {'_id':user_id}
    user_db.delete_one(query)
