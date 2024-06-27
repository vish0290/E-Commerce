from app.model.models import Seller
from app.config.database import seller_db
from app.schemas.schemas import list_seller,seller_serial
from bson import ObjectId

def get_seller(seller_id):
    query = {'_id':ObjectId(seller_id)}
    try:
        seller = seller_serial(seller_db.find_one(query))
    except:
        seller = None
    return seller

def get_seller_mail(email):
    query = {'email':email}
    try:
        return seller_serial(seller_db.find_one(query))
    except:
        return None

def get_all_seller():
    try:
        return list_seller(seller_db.find())
    except:
        return None

def add_seller(seller: Seller):
    ack = seller_db.insert_one(dict(seller)) 
    if ack.acknowledged:
        return True
    else:
        return False
    
def update_seller(seller: Seller,seller_id):
    query = {'_id':ObjectId(seller_id)}
    seller_db.find_one_and_update(query,dict(seller))
    
def del_seller(seller_id):
    query = {'_id':ObjectId(seller_id)}
    seller_db.find_one_and_delete(query)
