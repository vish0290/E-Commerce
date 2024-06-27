from fastapi import Request, FastAPI
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
def init_session_middleware(app: FastAPI):
    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


def login_user(request: Request, user_id: str):
    request.session["user_id"] = user_id
    request.session["role"] = "user"

def logout_user(request: Request):
    request.session.clear()


def login_seller(request: Request, seller_id: str):
    request.session["seller_id"] = seller_id
    request.session["role"] = "seller"

def logout_seller(request: Request):
    request.session.clear()


def login_admin(request: Request, admin_id: str):
    request.session["admin_id"] = admin_id
    request.session["role"] = "admin"
    
def logout_admin(request: Request):
    request.session.clear()




def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    role = request.session.get("role")
    if user_id and role == "user":
        return user_id
    return None

def get_current_seller(request: Request):
    seller_id = request.session.get("seller_id")
    role = request.session.get("role")
    if seller_id and role == "seller":
        return seller_id
    return None

def get_current_admin(request: Request):
    admin_id = request.session.get("admin_id")
    role = request.session.get("role")
    if admin_id and role == "admin":
        return admin_id
    return None

