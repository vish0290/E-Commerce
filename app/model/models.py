from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    name: str
    email: str
    password: str
    address: Optional[str] = None
    last_login: Optional[str] = None
    
class Product(BaseModel):
    name: str 
    images: List[str]
    price: str
    base_feature: str
    stock: int
    description: str
    cat_id: str
    seller_id: str
    last_change: str 
    
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

class Cart(BaseModel):
    user_id: str
    product_id: str
    seller_id: str
    quantity: int
    price: str
    total_price: str
    last_change: str
    
class Order(BaseModel):
    user_id: str
    product_id: str
    seller_id: str
    quantity: int
    price: str
    total_price: str
    last_change: str