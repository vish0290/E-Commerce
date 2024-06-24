from fastapi import APIRouter,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from app.model.models import User
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from app.crud.user import get_user_mail
from app.config.session import login_user, get_current_user,logout_user

router = APIRouter()
templates =  Jinja2Templates(directory='app/templates')


@router.get('/user_login',response_class= HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("user_login.html",{'request':request})

@router.post('/user_login',response_class=RedirectResponse)
def login(request: Request, email:str = Form(...), password:str = Form(...)):
    user = get_user_mail(email)
    if user and user['password'] == password:
        login_user(request,str(user['email']))
        return RedirectResponse(url='/',status_code=302)
    return templates.TemplateResponse('user_login.html',{'request':request,"error":"invalid email or password"})

@router.get('/user_logout',response_class=RedirectResponse)
def user_logout(request: Request):
    logout_user(request)
    return RedirectResponse(url='/')
        
@router.get('/', response_class=HTMLResponse)
def landing_page(request: Request):
    user = get_current_user(request)
    return templates.TemplateResponse("user_landing.html",{"request":request,"user":user})

