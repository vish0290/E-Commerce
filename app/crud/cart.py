from app.model.models import Cart
from app.config.database import cart_db, order_db
from app.schemas.schemas import cart_serial, list_cart
from bson import ObjectId


def get_cart_user(user_id):
    query = {'user_id':user_id}
    try:
        return list_cart(cart_db.find(query))
    except:
        return None

        
def update_cart_quantity(cart_id,quantity):
    query = {'_id':ObjectId(cart_id)}
    cart = cart_db.find_one(query)
    cart['quantity'] = quantity
    cart['total_price'] = str(float(cart['price']) * quantity)
    ack = cart_db.update_one(query,{'$set':cart})
    if ack.acknowledged:
        return True
    else:
        return False

def delete_cart(cart_id):
    query = {'_id':ObjectId(cart_id)}
    ack = cart_db.delete_one(query)
    if ack.acknowledged:
        return True
    else:
        return False
    
def del_product_cart(product_id,cart_id):
    query = {'_id':ObjectId(cart_id)}
    cart = cart_db.find_one(query)
    if cart['product_id'] == product_id:
        ack = cart_db.delete_one(query)
        if ack.acknowledged:
            return True
        else:
            return False
    return False
    

def add_new_cart(cart: Cart):
    ack = cart_db.insert_one(dict(cart)) 
    if ack.acknowledged:
        return True
    else:
        return False
        
def add_product_cart(cart: Cart):
    query = {'user_id':cart.user_id,'product_id':cart.product_id}
    try:
        cart = cart_db.find_one(query)
        cart['quantity'] = cart['quantity'] + 1
        cart['total_price'] = str(float(cart['price']) * cart['quantity'])
        ack = cart_db.update_one(query,{'$set':cart})
        if ack.acknowledged:
            return True
        else:
            return False
    except:
        ack = cart_db.insert_one(dict(cart)) 
        if ack.acknowledged:
            return True
        else:
            return False
    
def cart_to_order(user_id):
    query = {'user_id':user_id}
    cart = list_cart(cart_db.find(query))
    for c in cart:
        ack = cart_db.delete_one({'_id':c['id']})
        ack2 = order_db.insert_one(c)
        if not ack.acknowledged:
            return False
    return True
