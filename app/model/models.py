from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str
    address: str
    last_login: str
    
class Product(BaseModel):
    name: str
    price: str
    description: str
    stock: int
    images: list[str]
    cat_id: str
    last_change: str 
    
class Category(BaseModel):
    name: str
    description: str
    last_change: str 
    
class Seller(BaseModel):
    name: str
    email: str
    password: str
    phone: int
     
    
class Admin(BaseModel):
    name: str
    password: str

