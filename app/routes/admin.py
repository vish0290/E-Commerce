from fastapi import APIRouter,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from app.model.models import Admin, Category, Product, User, Order
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from app.crud.admin import get_admin_username
from app.crud.category import add_new_category, get_all_category, get_category
from app.crud.product import get_all_product
from app.crud.user import get_all_user
from app.crud.seller import get_all_seller
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
    

@router.get('/manage_user',response_class=HTMLResponse)
def manage_user(request: Request):
    admin = get_current_admin(request)
    users = get_all_user()
    return templates.TemplateResponse('manage_user.html',{'request':request,"admin":admin,"users":users})

@router.get('/order_logs',response_class=HTMLResponse)
def order_logs(request: Request):
    admin = get_current_admin(request)
    return templates.TemplateResponse('manage_order.html',{'request':request,"admin":admin})

@router.get('/manage_category',response_class=HTMLResponse)
def manage_category(request: Request):
    admin = get_current_admin(request)
    categories = get_all_category()
    return templates.TemplateResponse('manage_category.html',{'request':request,"admin":admin,"categories":categories})

@router.get('/manage_product',response_class=HTMLResponse)
def manage_product(request: Request):
    admin = get_current_admin(request)
    products = get_all_product()
    categories = get_all_category()
    categories = {category['id']:category['name'] for category in categories}
    
    seller = get_all_seller()
    seller = {seller['id']:seller['name'] for seller in seller}
    data = []
    for product in products:
        temp = {}
        temp['product'] = product['name']
        temp['category'] = categories[product['cat_id']]
        temp['price'] = product['price']
        temp['seller'] = seller[product['seller_id']]
        temp['quantity'] = product['stock']
        data.append(temp)
    return templates.TemplateResponse('manage_product.html',{'request':request,"admin":admin,"data":data})

@router.get('/manage_seller',response_class=HTMLResponse)
def manage_seller(request: Request):
    admin = get_current_admin(request)
    sellers = get_all_seller()
    return templates.TemplateResponse('manage_seller.html',{'request':request,"admin":admin,"sellers":sellers})