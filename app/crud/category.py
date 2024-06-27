from app.model.models import Category
from app.config.database import category_db
from app.schemas.schemas import list_category,category_serial
from bson import ObjectId

def get_category(category_id):
    query = {'_id':ObjectId(category_id)}
    try:
        category = category_serial(category_db.find_one(query))
    except:
        category = None
    return category

def get_category_name(name):
    query = {'name':name}
    try:
        return category_serial(category_db.find_one(query))
    except:
        return None
    
def get_all_category():
    try:
        return list_category(category_db.find())
    except:
        return None

def add_category(category: Category):
    ack = category_db.insert_one(dict(category)) 
    if ack.acknowledged:
        return True
    else:
        return False

def update_category(category: Category,category_id):
    query = {'_id':ObjectId(category_id)}
    category_db.find_one_and_update(query,dict(category))
    
def del_category(category_id):
    query = {'_id':ObjectId(category_id)}
    category_db.find_one_and_delete(query)
