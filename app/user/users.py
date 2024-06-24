from fastapi import APIRouter
from app.models.models import User
from app.schema.schemas import list_user,user_serial
from app.config.database import user_db
from bson import ObjectId


router = APIRouter()

#Get all user
@router.get('/get_all_user')
def get_all_user():
    user = list_user(user_db.find())
    return user

#Get 1 user
@router.get('/get_user/{id}')
def get_user(id: str):
    user = user_serial(user_db.find_one({'_id':ObjectId(id)}))
    return user


#add a user
@router.post('/add_user')
def add_user(user: User):
    user_db.insert_one(dict(user))
    
#update a user
@router.put('/update_user/{_id}')
def update_user(user: User,_id):
    try:
        query = {'_id':ObjectId(_id)} 
        item =  user_db.find_one(query)
    except:  
        return {'message':'no such user found'}
        
    user = user.dict() 
    for key in item.keys():
        if key != '_id':
            item[key] = user[key]
    ack = user_db.update_one(query,{"$set":dict(item)})
    if ack.acknowledged:
        return {'message':'data updated'}
    else:
        return {'message':'failed to update'}


    
#delete user
@router.delete('/del_user/{_id}')
def del_user(_id: str):
    query = {'_id':ObjectId(_id)}
    item = user_db.find_one_and_delete(query)
    if item is not None:
        return {'message':'user deleted'}
    else:
        return {'message':'no such user found'}    