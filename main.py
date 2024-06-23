from fastapi import FastAPI,Request
from app.routes import users
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



app = FastAPI()


templates = Jinja2Templates(directory="app/templates") 


app.include_router(router= users.router)

@app.get("/",response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("index.html",{"request":request, "name":"demo"})