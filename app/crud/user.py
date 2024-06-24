from app.model.models import User
from app.config.database import user_db
from app.schemas.schemas import list_user,user_serial
from bson import ObjectId



def get_user(user_id):
    query = {'_id':ObjectId(user_id)}
    user = user_serial(user_db.find_one(query))
    return user

def get_user_mail(email):
    query = {'email':email}
    return user_serial(user_db.find_one(query))

def get_all_user():
    return list_user(user_db.find())
    
def add_user(user: User):
    user_db.insert_one(dict(user))
    
def update_user(user: User,user_id):
    query = {'_id':ObjectId(user_id)}
    user_db.find_one_and_update(query,dict(user))

def del_user(user_id):
    query = {'_id':ObjectId(user_id)}
    user_db.find_one_and_delete(query)
    
