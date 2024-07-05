from fastapi import APIRouter,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from app.model.models import User
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from app.crud.user import get_user_mail,add_user
from app.config.session import login_user, get_current_user,logout_user
from app.crud.category import get_all_category,get_category,search_category
from app.crud.product import get_product_cat, get_random_product, search_product,get_product


router = APIRouter()
templates =  Jinja2Templates(directory='app/templates')

#user login and logout
@router.get('/user_login',response_class= HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("user_login.html",{'request':request})

@router.post('/user_login',response_class=RedirectResponse)
def login(request: Request, email:str = Form(...), password:str = Form(...)):
    user = get_user_mail(email)
    if user != None and user['password'] == password:
        login_user(request,str(user['email']))
        return RedirectResponse(url='/',status_code=302)
    return templates.TemplateResponse('user_login.html',{'request':request,"error":"invalid email or password"})

@router.get('/user_logout',response_class=RedirectResponse)
def user_logout(request: Request):
    logout_user(request)
    return RedirectResponse(url='/')

#user registration        
@router.post('/add_user', response_class=HTMLResponse)
def user_register(request: Request, name:str = Form(...), email: str=Form(...), password: str=Form(...)):
    item = get_user_mail(email)
    if item != None:
        return templates.TemplateResponse("user_register.html", {"request": request,"message":"User Already exist"})
    else:
        user = User(name=name,password=password,email=email)
        ack = add_user(user)
        if ack:
            return RedirectResponse(url='/user_login', status_code=302)
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