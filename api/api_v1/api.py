from fastapi import APIRouter
from api.api_v1.endpoints import admin_console
from api.api_v1.endpoints import print_label_service



api_router = APIRouter()
api_router.include_router(admin_console.router, tags=["Настройки системы, добавление принтеров и шаблонов этикеток"])
api_router.include_router(print_label_service.router,tags=["Печать этикеток на принтеры этикеток"])

