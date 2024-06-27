from fastapi import APIRouter,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from app.model.models import Seller
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from app.crud.seller import get_seller_mail, add_seller
from app.config.session import login_seller, get_current_seller,logout_seller

router = APIRouter()
templates =  Jinja2Templates(directory='app/templates')

@router.get('/seller_login',response_class= HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("seller_login.html",{'request':request})

@router.post('/seller_login',response_class=HTMLResponse)
def login(request: Request, email:str = Form(...), password:str = Form(...)):
    seller = get_seller_mail(email)
    print(seller['name'])
    if seller != None and seller['password'] == password:
        login_seller(request,str(seller['email']))
        return RedirectResponse(url='/seller_dashboard',status_code=302)
    return templates.TemplateResponse('seller_login.html',{'request':request,"error":"invalid email or password"})

@router.get('/seller_logout',response_class=RedirectResponse)
def user_logout(request: Request):
    logout_seller(request)
    return RedirectResponse(url='/seller_login')


@router.get('/seller_dashboard', response_class=HTMLResponse)
def landing_page(request: Request):
    seller = get_current_seller(request)
    return templates.TemplateResponse("seller_landing.html",{"request":request,"seller":seller})

@router.post('/add_seller')
def seller_registration(seller:Seller ):
    ack = add_seller(seller)
    if ack:
        return RedirectResponse(url='/seller_login',status_code=302)
    return templates.TemplateResponse('seller_login.html',{'request':request,"error":"Error while adding seller"})