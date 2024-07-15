from app.model.models import User
from app.config.database import user_db,order_db
from app.schemas.schemas import list_user,user_serial
from datetime import datetime
from bson import ObjectId



def get_user(user_id):
    query = {'_id':ObjectId(user_id),'status':'active'}
    try:
        user = user_serial(user_db.find_one(query))
    except:
        user = None
    return user

def get_user_mail(email):
    query = {'email':email,'status':'active'}
    try:
        return user_serial(user_db.find_one(query))
    except:
        return None

def get_all_user():
    try:
        return list_user(user_db.find({'status':'active'}))
    except:
        return None
    
def add_user(user: User):
    ack = user_db.insert_one(dict(user)) 
    if ack.acknowledged:
        return True
    else:
        return False 
                
def update_user(user: User,user_id):
    user = user.dict()
    find_user = user_serial(user_db.find_one({'email':user['email']}))
    if find_user != None:
        if str(find_user['id']) != user_id:
            return False
        else:
            query = {'_id':ObjectId(user_id)}
            setdata = {'$set':user}
            user_db.update_one(query,setdata)
            return True
        
    
    
def del_user(user_id):
    query = {'_id':ObjectId(user_id)}
    setdata = {'$set':{'status':'inactive'}}
    user_db.update_one(query,setdata)
    order_db.find_and_modify({'user_id':user_id},{'$set':{'status':'inactive'}})        
def update_last_login(user_id):
    query = {'_id':ObjectId(user_id)}
    user_db.find_one_and_update(query,{"$set":{"last_login":datetime.now().strftime("%d/%m/%Y %H:%M:%S")}})
    
