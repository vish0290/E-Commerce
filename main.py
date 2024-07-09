from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routes.users import router as user_routes
from app.config.session import init_session_middleware
from app.routes.seller import router as seller_routes
from app.routes.admin import router as admin_routes

app = FastAPI()
init_session_middleware(app)

app.include_router(user_routes)
app.include_router(seller_routes)
app.include_router(admin_routes)

@app.exception_handler(404)
def not_found(request, exc):
    return RedirectResponse(url='/404')