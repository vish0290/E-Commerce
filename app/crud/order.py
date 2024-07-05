from app.model.models import Order
from app.config.database import order_db
from app.schemas.schemas import order_serial, list_order
from bson import ObjectId

def get_order_user(user_id):
    query = {'user_id':user_id}
    try:
        return list_order(order_db.find(query))
    except:
        return None

def get_all_order():
    try:
        return list_order(order_db.find())
    except:
        return None
    
