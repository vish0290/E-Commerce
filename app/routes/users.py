from fastapi import APIRouter
from app.crud.user import *

router = APIRouter()





"""Landing page"""

@router.get("/")
def 