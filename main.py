from fastapi import FastAPI
from app.routes.users import router as user_routes
from app.config.session import init_session_middleware


app = FastAPI()
init_session_middleware(app)

app.include_router(user_routes)
