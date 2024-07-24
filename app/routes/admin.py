from fastapi import APIRouter,Request,Form,Query
from fastapi.responses import HTMLResponse,RedirectResponse
from app.model.models import Admin, Category, Product, User, Order, Seller
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from app.crud.admin import get_admin_username
from app.crud.category import add_new_category, get_all_category, get_category, del_category, restore_category
from app.crud.product import get_all_product,del_product,get_product,search_product
from app.crud.user import get_all_user, get_user, del_user,search_users_by_name
from app.crud.seller import get_all_seller, get_seller_mail, add_seller, del_seller,get_seller
from app.crud.order import get_all_order, del_order
from app.config.session import login_admin, get_current_admin,logout_admin
from app.config.cypher import verify_password,hash_password
import datetime

router = APIRouter()
templates =  Jinja2Templates(directory='app/templates')

@router.get('/admin_login',response_class= HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("admin_login.html",{'request':request})

@router.post('/admin_login',response_class=HTMLResponse)
def login(request: Request, username:str = Form(...), password:str = Form(...)):
    admin = get_admin_username(username)
    if admin != None and verify_password(admin['password'],password):
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
    category = Category(name=name, description=description, image=image, last_change=str(datetime.datetime.now()), status='active')
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

@router.get('/del_user/{user_id}',response_class=HTMLResponse)
def delete_user_data(request:Request,user_id:str):
    admin=get_current_admin(request)
    del_user(user_id)
    return RedirectResponse(url="/manage_user")
                            
                            

@router.get('/order_logs',response_class=HTMLResponse)
def order_logs(request: Request):
    admin = get_current_admin(request)
    orders_data = get_all_order()
    orders = []
    for item in orders_data:
        order = {}
        user_data = get_user(item['user_id'])
        for product_id, quantity in item['product_data'].items():
            product = get_product(product_id)
            seller = get_seller(product['seller_id'])
            order['id'] = item['id']
            order['seller'] = seller['name']
            order['product'] = product['name']
            order['quantity'] = quantity
            order['user'] = user_data['name']
            order['category'] = get_category(product['cat_id'])['name']
            order['price'] = int(product['price']) * quantity
            orders.append(order)
        
    return templates.TemplateResponse('manage_order.html',{'request':request,"admin":admin,"orders":orders})

@router.get('/delete_order/{order_id}',response_class=HTMLResponse)
def delete_order_data(request:Request,order_id:str):
    admin=get_current_admin(request)
    del_order(order_id)
    return RedirectResponse(url="/order_logs")


@router.get('/manage_category',response_class=HTMLResponse)
def manage_category(request: Request):
    admin = get_current_admin(request)
    categories = get_all_category()
    return templates.TemplateResponse('manage_category.html',{'request':request,"admin":admin,"categories":categories})

@router.get('/manage_category_del/{item_id}',response_class=HTMLResponse)
def del_category_item(request:Request,item_id:str):
    admin=get_current_admin(request)
    del_category(item_id)
    return RedirectResponse(url="/manage_category" )

@router.get('/restore_category/{item_id}',response_class=HTMLResponse)
def restore_category_item(request:Request,item_id:str):
    admin=get_current_admin(request)
    restore_category(item_id)
    return RedirectResponse(url="/manage_category" )

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
        temp['id']=product['id']
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

@router.get('/manage_product_del/{item_id}',response_class=HTMLResponse)
def del_product_item(request:Request,item_id:str):
    admin=get_current_admin(request)
    del_product(item_id)
    return RedirectResponse(url="/manage_product" )

@router.get('/add_seller',response_class=HTMLResponse)
def seller_register(request: Request):
    admin = get_current_admin(request)
    return templates.TemplateResponse('add_seller.html',{'request':request,"admin":admin})

@router.post('/add_seller',response_class=HTMLResponse)
def seller_register(request: Request, name:str = Form(...), email: str=Form(...), password: str=Form(...), number: int=Form(...)): 
    admin = get_current_admin(request)
    item = get_seller_mail(email)
    if item != None:
        return templates.TemplateResponse("add_seller.html", {"request": request,"message":"Seller Already exist"})
    else:
        password = hash_password(password)
        seller = Seller(name=name,email=email,password=password,phone=number,status='active')
        ack = add_seller(seller)
        if ack:
          return templates.TemplateResponse("add_seller.html", {"request": request,"admin":admin,"success":"Seller registered successfully"})
        else:
            return templates.TemplateResponse("add_seller.html", {"request": request,"admin":admin,"message":"Something went wrong"})

@router.get('/delete_seller/{seller_id}',response_class=HTMLResponse)
def delete_seller(request:Request,seller_id:str):
    admin=get_current_admin(request)
    del_seller(seller_id)
    return RedirectResponse(url="/manage_seller" )


@router.get('/search_user',response_class=HTMLResponse)
def search_user(request: Request, query:str=Query(...)):
    admin = get_current_admin(request)
    users =  search_users_by_name(query)
    return templates.TemplateResponse('manage_user.html',{'request':request,"admin":admin,"users":users})

@router.get('/search_product_name', response_class=HTMLResponse)
def search_product_name(request: Request,query:str=Query(...)): 
    admin = get_current_admin(request)
    products = search_product(query)
    categories = get_all_category()
    categories = {category['id']:category['name'] for category in categories}
    
    seller = get_all_seller()
    seller = {seller['id']:seller['name'] for seller in seller}
    data = []
    for product in products:
        temp = {}
        temp['id']=product['id']
        temp['product'] = product['name']
        temp['category'] = categories[product['cat_id']]
        temp['price'] = product['price']
        temp['seller'] = seller[product['seller_id']]
        temp['quantity'] = product['stock']
        data.append(temp)
    return templates.TemplateResponse('manage_product.html',{'request':request,"admin":admin,"data":data})