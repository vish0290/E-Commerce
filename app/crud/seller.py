from app.model.models import Seller
from app.config.database import seller_db
from app.schemas.schemas import list_seller,seller_serial
from bson import ObjectId

def get_seller(seller_id):
    query = {'_id':ObjectId(seller_id),'status':'active'}
    try:
        seller = seller_serial(seller_db.find_one(query))
    except:
        seller = None
    return seller

def get_seller_mail(email):
    query = {'email':email,'status':'active'}
    try:
        return seller_serial(seller_db.find_one(query))
    except:
        return None

def get_all_seller():
    try:
        return list_seller(seller_db.find({'status':'active'}))
    except:
        return None

def add_seller(seller: Seller):
    ack = seller_db.insert_one(seller.dict()) 
    if ack.acknowledged:
        return True
    else:
        return False
    
def update_seller(seller: Seller,seller_id):
    seller = seller.dict()
    find_seller = seller_serial(seller_db.find_one({'email':seller['email']}))
    if find_seller != None:
        if str(find_seller['id']) != seller_id:
            return False
        else:
            query = {'_id':ObjectId(seller_id)}
            setdata = {'$set':seller}
            seller_db.update_one(query,setdata)
            return True
        
    
def del_seller(seller_id):
    query = {'_id':ObjectId(seller_id)}
    setdata = {'$set':{'status':'inactive'}}
    seller_db.update_one(query,setdata)
