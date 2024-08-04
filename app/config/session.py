from fastapi import Request, FastAPI
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
def init_session_middleware(app: FastAPI):
    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


def login_user(request: Request, user_id: str, role: str):
    request.session["user_id"] = user_id
    request.session["role"] = "user"
    request.session["status"] = role

def logout_user(request: Request):
    request.session.clear()


def login_seller(request: Request, seller_id: str,role: str ):
    request.session["seller_id"] = seller_id
    request.session["role"] = "seller"
    request.session["status"] = role

def logout_seller(request: Request):
    request.session.clear()

def login_admin(request: Request, username: str):
    request.session['username'] = username
    request.session['role'] = 'admin'
    
def logout_admin(request: Request):
    request.session.clear()




def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    role = request.session.get("role")
    status = request.session.get("status")
    if user_id and role == "user" and status == "auth":
        return user_id
    return None

def get_temp_user(request: Request):
    user_id = request.session.get("user_id")
    role = request.session.get("role")
    status = request.session.get("status")
    if user_id and role == "user" and status == "temp":
        return user_id
    return None

def get_current_seller(request: Request):
    seller_id = request.session.get("seller_id")
    role = request.session.get("role")
    status = request.session.get("status")
    if seller_id and role == "seller" and status == "auth":
        return seller_id
    return None

def get_temp_seller(request: Request):
    seller_id = request.session.get("seller_id")
    role = request.session.get("role")
    status = request.session.get("status")
    if seller_id and role == "seller" and status == "temp":
        return seller_id
    return None

def get_current_admin(request: Request):
    admin_id = request.session.get("username")
    role = request.session.get("role")
    if admin_id and role == "admin":
        return admin_id
    return None


