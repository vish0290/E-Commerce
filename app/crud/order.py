from app.model.models import Order
from app.config.database import order_db
from app.schemas.schemas import order_serial, list_order
from bson import ObjectId

def get_order_user(user_id):
    query = {'user_id':user_id, 'status':'active'}
    try:
        return list_order(order_db.find(query).sort('order_date',-1))
    except:
        return None

def get_all_order():
    try:
        return list_order(order_db.find({'status':'active'}))
    except:
        return None

def del_order(order_id):
    query = {'_id':ObjectId(order_id)}
    setdata = {'$set':{'status':'inactive'}}
    order_db.update_one(query,setdata)
    order_db.update_one(query,setdata)
    
def get_order(order_id):
    query = {'_id':ObjectId(order_id),'status':'active'}
    try:
        return order_serial(order_db.find_one(query))
    except:
        return None