from fastapi import APIRouter
from app.api.routes.endpoints import user
from app.api.routes.endpoints import auth

router = APIRouter()
router.include_router(auth.router)
router.include_router(user.router)
