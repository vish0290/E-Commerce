from fastapi import Request, FastAPI
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
def init_session_middleware(app: FastAPI):
    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if user_id:
        return user_id
    return None

def login_user(request: Request, user_id: str):
    request.session["user_id"] = user_id

def logout_user(request: Request):
    request.session.clear()