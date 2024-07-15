from fastapi import APIRouter,Request,Form,Query,HTTPException, FastAPI
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from app.model.models import User, Cart
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from app.crud.user import get_user_mail,add_user, update_last_login,update_user
from app.config.session import login_user, get_current_user,logout_user
from app.crud.category import get_all_category,get_category,search_category
from app.crud.product import get_product_cat, get_random_product, search_product,get_product,get_product_by_cat_id_sort
from app.crud.cart import add_cart_product, get_cart_user, remove_cart_product, update_cart_product, checkout_cart
from app.crud.order import get_order_user
from datetime import datetime
from app.config.cypher import verify_password,hash_password


router = APIRouter()
templates =  Jinja2Templates(directory='app/templates')

#user login and logout
@router.get('/user_login',response_class= HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("user_login.html",{'request':request})

@router.post('/user_login',response_class=RedirectResponse)
def login(request: Request, email:str = Form(...), password:str = Form(...)):
    user = get_user_mail(email)
    if user != None and  verify_password(user['password'],password):
        login_user(request,str(user['email']))
        update_last_login(user['id'])
        return RedirectResponse(url='/',status_code=302)
    return templates.TemplateResponse('user_login.html',{'request':request,"error":"invalid email or password"})

@router.get('/user_logout',response_class=RedirectResponse)
def user_logout(request: Request):
    logout_user(request)
    return RedirectResponse(url='/')

#user registration        
@router.post('/add_user', response_class=HTMLResponse)
def user_register(request: Request, name:str = Form(...), email: str=Form(...), password: str=Form(...), address: str=Form(...)): 
    item = get_user_mail(email)
    if item != None:
        return templates.TemplateResponse("user_register.html", {"request": request,"message":"User Already exist"})
    else:
        password = hash_password(password)
        user = User(name=name,password=password,email=email,address=address)
        ack = add_user(user)
        if ack:
          return templates.TemplateResponse("user_register.html", {"request": request,"success":"User registered successfully"})
        else:
            return templates.TemplateResponse("user_register.html", {"request": request,"message":"Something went wrong"})
            
@router.get('/add_user', response_class=HTMLResponse)
def user_registration(request: Request):
    return templates.TemplateResponse("user_register.html",{"request":request})

#user landing page
@router.get('/', response_class=HTMLResponse)
def landing_page(request: Request):
    user = get_current_user(request)
    categories = get_all_category()
    products = get_random_product()
    return templates.TemplateResponse("user_landing.html",{"request":request,"user":user,"categories":categories,"products":products})
#category page
@router.get('/user_category/{cat_id}')
def cat_page(request: Request, cat_id: str):
    user = get_current_user(request)
    category = get_category(cat_id)
    categories = get_all_category()
    products = get_product_cat(cat_id)
    return templates.TemplateResponse("users_category.html",{'request':request,"user":user,"category":category,"categories":categories,"products":products})
    
@router.get('/search/', response_class=HTMLResponse)
def search(request: Request, query: str):
    user = get_current_user(request)
    categories = get_all_category()
    res_products = []
    cat_product = []
    res_products = search_product(query)
    cat_list = search_category(query)
    for cat in cat_list:
        cat_product += get_product_cat(str(cat['id']))
        print(cat_product)
    if res_products != None and cat_list != None:
        res_products += cat_product
    elif res_products == None and cat_list != None:
        res_products += cat_product
    return templates.TemplateResponse("search_page.html",{"request":request,"user":user,"categories":categories,"products":res_products,"query":query})

#product page
@router.get('/user_product/{prod_id}', response_class=HTMLResponse)
def product_page(request: Request, prod_id: str):
    user = get_current_user(request)
    categories = get_all_category()
    product = get_product(prod_id)
    return templates.TemplateResponse("product_page.html",{"request":request,"user":user,"categories":categories,"product":product})

@router.get('/add_to_cart', response_class=HTMLResponse)
def cart_page(request: Request, product_id: str= Query(...), quantity: int = Query(...)):
    user = get_current_user(request)
    categories = get_all_category()
    product_data = get_product(product_id)
    if quantity > product_data['stock']:
        return JSONResponse(status_code=400, content={"success": False, "message": "Not enough stock available"})
    user_data = get_user_mail(user)
    ack = add_cart_product(user_data['id'],product_id,quantity)
    if ack:
         return JSONResponse(status_code=200, content={"success": True, "message": "Product added to cart successfully"})
    else:
         return JSONResponse(status_code=400, content={"success": False, "message": "Something went wrong. Please try again later"}) 
     
@router.get('/buy_now', response_class=HTMLResponse)
def buy_now(request: Request, product_id: str= Query(...), quantity: int = Query(...)):
    user = get_current_user(request)
    categories = get_all_category()
    product_data = get_product(product_id)
    if quantity > product_data['stock']:
        return JSONResponse(status_code=400, content={"success": False, "message": "Not enough stock available"})
    user_data = get_user_mail(user)
    ack = add_cart_product(user_data['id'],product_id,quantity)
    if ack:
        return JSONResponse(status_code=200, content={"redirect": True, "message": "Redirecting..", "url": "/user_cart"})
    else:
        return JSONResponse(status_code=400, content={"success": False, "message": "Something went wrong. Please try again later"})


# 404_page_not_found
@router.get("/404", response_class=HTMLResponse)
async def catch_all(request: Request):
    return templates.TemplateResponse("error_page.html", {"request": request})

@router.get('/user_cart',response_class=HTMLResponse)
def cart(request: Request):
    user = get_current_user(request)
    if user == None:
        return RedirectResponse(url="/404")
    user_data = get_user_mail(user)
    categories = get_all_category()
    cart_data = get_cart_user(user_data['id'])
    products = []
    super_total = 0
    if cart_data != None:
        for prod_id, qty in cart_data['product_data'].items():
            temp_dict = {}
            product = get_product(prod_id)
            temp_dict['id'] = prod_id
            temp_dict['image'] = product['images'][0]
            temp_dict['name'] = product['name']
            temp_dict['description'] = product['base_feature']
            temp_dict['price'] = product['price']
            temp_dict['qty'] = qty
            temp_dict['total_price'] = str(int(product['price']) * qty)
            products.append(temp_dict)
        super_total = cart_data['total_price']
    return templates.TemplateResponse("cart.html",{"request":request,"user":user,"categories":categories,"products":products,"super_total":super_total})


@router.delete('/remove_cart_item', response_class=RedirectResponse)
def remove_cart_item(request: Request, product_id: str = Query(...)):
    user = get_current_user(request)
    user_data = get_user_mail(user)
    ack = remove_cart_product(user_data['id'],product_id)
    if ack:
        return RedirectResponse(url='/user_cart')
    return RedirectResponse(url='/404')

@router.get('/qty_update', response_class=JSONResponse)
def qty_update(request: Request, product_id: str = Query(...), flag: bool = Query(...)):
    user = get_current_user(request)
    user_data = get_user_mail(user)
    ack = update_cart_product(user_data['id'],product_id,flag)
    if ack:
        return JSONResponse(status_code=200, content={"success": True, "message": "Quantity updated successfully"})
    else:
        return JSONResponse(status_code=400, content={"success": False, "message": "Not Enough Stock Available"})

@router.get('/order_confirmed', response_class=HTMLResponse)
def order_confirmed(request: Request):
    user = get_current_user(request)
    categories = get_all_category()
    user_data = get_user_mail(user)
    order = checkout_cart(user_data['id'])
    return templates.TemplateResponse("order-confirmed.html",{"request":request,"user":user,"categories":categories})

@router.get('/stock_check', response_class=JSONResponse)
def stock_check(request: Request, product_id: str = Query(...), quantity: int = Query(...)):
    product = get_product(product_id)
    if quantity > product['stock']:
        return JSONResponse(status_code=400, content={"success": False, "message": "Not enough stock available"})
    return JSONResponse(status_code=200, content={"success": True, "message": "Stock available"})
@router.get('/sort_category/{cat_id}/{sort}')
def cat_sort_page(request: Request, cat_id: str, sort: str):
    user = get_current_user(request)
    categories = get_all_category()
    products = get_product_by_cat_id_sort(cat_id,int(sort))
    category = get_category(cat_id)
    return templates.TemplateResponse("users_category.html",{'request':request,"user":user,"category":category,"categories":categories,"products":products})

@router.get('/500')
def server_error(request: Request):
    return templates.TemplateResponse("500.html",{"request":request})

@router.get('/user_profile', response_class=HTMLResponse)
def user_profile(request: Request):
    user = get_current_user(request)
    user_data = get_user_mail(user)
    categories = get_all_category()
    orders = get_order_user(user_data['id'])
    products = []
    for i in orders:
        temp = {}
        temp['order_id'] = i['id']
        temp['order_date'] = i['order_date']
        for product_id, qty in i['product_data'].items():
            product = get_product(product_id)
            temp['name'] = product['name']
            temp['base_feature'] = product['base_feature']
            temp['images'] = product['images']
            temp['price'] = product['price']
            temp['stock'] = qty
            temp['total_price'] = str(int(product['price']) * qty)
            products.append(temp)
    
    return templates.TemplateResponse("user_profile.html",{"request":request,"user":user_data,"categories":categories,"products":products})

@router.get('/user_edit_profile', response_class=HTMLResponse)
def user_edit_profile(request: Request):
    user = get_current_user(request)
    user_data = get_user_mail(user)
    categories = get_all_category()
    return templates.TemplateResponse("edit_user.html",{"request":request,"user":user_data,"categories":categories})

@router.post('/user_profile_update', response_class=RedirectResponse)
def user_edit_profile(request: Request, name:str = Form(...), email: str=Form(...), address: str=Form(...)):
    user = get_current_user(request)
    user_data = get_user_mail(user)
    categories = get_all_category()
    user = User(name=name,email=email,address=address,password=user_data['password'],id=user_data['id'])
    ack = update_user(user,user_data['id'])
    if ack == False:
        return templates.TemplateResponse("edit_user.html",{"request":request,"error":"Email already exist","user":user,"categories":categories})
    elif ack == True:
        return templates.TemplateResponse("edit_user.html",{"request":request,"success":"Profile updated successfully","user":user,"categories":categories})
    else:
        return templates.TemplateResponse("500.html",{"request":request})