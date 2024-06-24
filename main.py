from fastapi import FastAPI,Request
from app.routes.users import router
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



app = FastAPI()


templates = Jinja2Templates(directory="app/templates") 


app.include_router(router= users.router)


product = [{'product':'iphone 15', 'price':'50000'},{'product':'iphone 14','price':'60000'}]
@app.get("/",response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("home.html",{"request":request, 'product_list':product})