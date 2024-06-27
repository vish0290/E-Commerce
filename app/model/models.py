from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    name: str
    email: str
    password: str
    address: Optional[str] = None
    last_login: Optional[str] = None
    
class Product(BaseModel):
    name: str #basic model
    images: str
    price: str
    base_feature: str
    stock: int
    # description: str
    # cat_id: str
    # last_change: str 
    
class Category(BaseModel):
    name: str
    description: str
    image: str
    last_change: str 
    
class Seller(BaseModel):
    name: str
    email: str
    password: str
    phone: int
     
    
class Admin(BaseModel):
    username: str
    password: str

