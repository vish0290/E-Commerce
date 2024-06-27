from app.model.models import Product
from app.config.database import product_db
from app.schemas.schemas import list_product,product_serial
from bson import ObjectId

def get_product(product_id):
    query = {'_id':ObjectId(product_id)}
    try:
        product = product_serial(product_db.find_one(query))
    except:
        product = None
    return product

def get_product_name(name):
    query = {'name':name}
    try:
        return product_serial(product_db.find_one(query))
    except:
        return None
    
def get_all_product():
    try:
        return list_product(product_db.find())
    except:
        return None
    
def get_product_cat(cat_id):
    query = {'cat_id':cat_id}
    try:
        return list_product(product_db.find(query))
    except:
        return None

def get_random_product():
    try:
        return list_product(product_db.aggregate([{'$sample':{'size':12}}]))
    except:
        return None

def add_new_product(product: Product):
    ack = product_db.insert_one(dict(product)) 
    if ack.acknowledged:
        return True
    else:
        return False

def update_product(product: Product,product_id):
    query = {'_id':ObjectId(product_id)}
    product_db.find_one_and_update(query,dict(product))

def del_product(product_id):
    query = {'_id':ObjectId(product_id)}
    product_db.find_one_and_delete(query)
    
