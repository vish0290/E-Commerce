from fastapi import APIRouter,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from app.model.models import Admin, Category, Product
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from app.crud.admin import get_admin_username
from app.crud.category import add_new_category
from app.crud.product import add_new_product
from app.config.session import login_admin, get_current_admin,logout_admin
import datetime

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




#category routes
# @router.post('/add_category',response_class=HTMLResponse)
# def add_category(request: Request, name:str = Form(...), description:str = Form(...), image:str = Form(...)):
#     category = Category(name=name,description=description,image=image,last_change=str(datetime.datetime.now()))
#     ack = add_category(category)
#     if ack:
#         return RedirectResponse(url='/admin_dashboard',status_code=302)
#     else:
#         return templates.TemplateResponse("add_category.html", {"request": request,"message":"Something went wrong"})

@router.post('/add_category')
def add_category(name:str, description:str, image:str):
    category = Category(name=name, description=description, image=image, last_change=str(datetime.datetime.now()))
    ack = add_new_category(category)
    if ack:
        return {'message':'category added successfully'}
    else:
        return {'message':'something went wrong'}
    
@router.post('/add_product')
def add_product(name:str, images:str, price:str, base_feature:str, stock:int):
    product = Product(name=name, images=images, price=price, base_feature=base_feature, stock=stock)
    ack = add_new_product(product)
    if ack:
        return {'message':'product added successfully'}
    else:
        return {'message':'something went wrong'}