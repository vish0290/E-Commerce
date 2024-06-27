from fastapi import APIRouter,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from app.model.models import Admin
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from app.crud.admin import get_admin_username
from app.config.session import login_admin, get_current_admin,logout_admin

router = APIRouter()
templates =  Jinja2Templates(directory='app/templates')

@router.get('/admin_login',response_class= HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("admin_login.html",{'request':request})

@router.post('/admin_login',response_class=HTMLResponse)
def login(request: Request, username:str = Form(...), password:str = Form(...)):
    admin = get_admin_username(username)
    if admin != None and admin['password'] == password:
        login_admin(request,str(admin['username']))
        return RedirectResponse(url='/admin_dashboard',status_code=302)
    return templates.TemplateResponse('admin_login.html',{'request':request,"error":"invalid username or password"})

@router.get('/admin_dashboard',response_class=HTMLResponse)
def dashboard(request: Request):
    admin = get_current_admin(request)
    if admin == None:
        return RedirectResponse(url='/admin_login',status_code=302)
    return templates.TemplateResponse('admin_dashboard.html',{'request':request,'admin':admin})

@router.get('/admin_logout',response_class=HTMLResponse)
def logout(request: Request):
    logout_admin(request)
    return RedirectResponse(url='/admin_login',status_code=302)

@router.post('/add_category',response_class=HTMLResponse)
def add_category(request: Request, name:str = Form(...), description:str = Form(...), image:str = Form(...)):
    category = Category(name=name,description=description,image=image,last_change=str(datetime.datetime.now()))
    ack = add_category(category)
    if ack:
        return RedirectResponse(url='/admin_dashboard',status_code=302)
    else:
        return templates.TemplateResponse("add_category.html", {"request": request,"message":"Something went wrong"})