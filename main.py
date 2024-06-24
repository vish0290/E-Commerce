from fastapi import FastAPI,Request,Form, Depends
from app.routes import users
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates



app = FastAPI()
secret_key = os.getenv('SECRET_KEY')
serializer = URLSafeSerializer(secret_key)
app.add_middleware(SessionMiddleware,secret_key = secret_key)

templates = Jinja2Templates(directory="app/templates") 

app.include_router(router= users.router)
