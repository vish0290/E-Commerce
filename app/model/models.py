from pydantic import BaseModel
from typing import List, Optional, Dict


class User(BaseModel):
    name: str
    email: str
    password: str
    address: Optional[str] = None
    last_login: Optional[str] = None
    status: str = "active"
    
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
    status: str = "active"
    
class Category(BaseModel):
    name: str
    description: str
    image: str
    last_change: str 
    status: str = "active"
    
class Seller(BaseModel):
    name: str
    email: str
    password: str
    phone: int
    last_login: Optional[str] = None
    status: str = "active"
     
    
class Admin(BaseModel):
    username: str
    password: str


class Cart(BaseModel):
    user_id: str
    product_data: Dict[str, int] 
    total_price: str
    last_change: str
    
class Order(BaseModel):
    user_id: str
    product_data: Dict[str, int]
    total_price: str
    order_date: str
    last_change: str
    status: str = "active"