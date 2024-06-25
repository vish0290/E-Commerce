from app.model.models import User
from app.config.database import user_db
from app.schemas.schemas import list_user,user_serial
from bson import ObjectId



def get_user(user_id):
    query = {'_id':ObjectId(user_id)}
    try:
        user = user_serial(user_db.find_one(query))
    except:
        user = None
    return user

def get_user_mail(email):
    query = {'email':email}
    try:
        return user_serial(user_db.find_one(query))
    except:
        return None

def get_all_user():
    try:
        return list_user(user_db.find())
    except:
        return None
    
def add_user(user: User):
    ack = user_db.insert_one(dict(user)) 
    if ack.acknowledged:
        return True
    else:
        return False 
                
def update_user(user: User,user_id):
    query = {'_id':ObjectId(user_id)}
    user_db.find_one_and_update(query,dict(user))

def del_user(user_id):
    query = {'_id':ObjectId(user_id)}
    user_db.find_one_and_delete(query)
    
