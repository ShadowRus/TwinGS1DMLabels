import asyncio
from fastapi import APIRouter, UploadFile, File, Depends, Request
from fastapi.responses import JSONResponse
from models.Goods import Goods,GoodsId
from models.LabelPrinter import TemplateResponse,Template,PrinterService,PrinterRespone,DeviceService,DeviceRespone
from services.services import get_value_or_none
from sqlalchemy.orm import Session
from api import deps

import aiofiles as aiofiles
import os
import requests

from decouple import config

import pandas as pd
import datetime

UPLOAD = config('UPLOAD_DIR', default='./uploaded_files')

router = APIRouter()
now = datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')




@router.get("/getmyip", summary="Получить IP4 подключенного устройства",
             description="Реализуем регистрацию устройства")
async def get_my_ip(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}

#--Загрузка файла с шаблоном
@router.post("/template", summary="Загружаем шаблон этикетки",
             description="Этикетка ZPL")
async def template(data:TemplateResponse,db: Session = Depends(deps.get_db)):
    try:
    # if 5 ==5 :
        template = Template(templ_data = data.label,
                            templ_name = data.name,
                            is_default = data.is_default,
                            is_deleted = 0)
        db.add(template)
        db.commit()
        db.close()
        return JSONResponse(status_code=200, content={'status': 'Success'})
    except:
        return JSONResponse(status_code=500, content={'status': 'Error'})



@router.post("/printer", summary="Добавляем принтер в БД",
             description=" ")
async def printer(data:PrinterRespone,db: Session = Depends(deps.get_db)):
    try:
        printer = PrinterService(print_name = data.name,url = data.url,is_default = data.is_default,
                                 port = data.port,type = data.type,is_deleted = 0)
        db.add(printer)
        db.commit()
        db.close()
        return JSONResponse(status_code=200, content={'status': 'Success'})
    except:
        return JSONResponse(status_code=500, content={'status': 'Error'})

@router.post("/device", summary="Добавляем устройство в БД",
             description=" ")
async def printer(data:DeviceRespone,db: Session = Depends(deps.get_db)):
    try:
        device = DeviceService(device_name = data.name,url = data.url,is_deleted = 0)
        db.add(device)
        db.commit()
        db.close()
        return JSONResponse(status_code=200, content={'status': 'Success'})
    except:
        return JSONResponse(status_code=500, content={'status': 'Error'})


@router.get("/printers",summary="Получаем список принтеров",
             description="Возвращает список всех принтеров")
async def goods(db: Session = Depends(deps.get_db)):
    return db.query(PrinterService).filter(PrinterService.is_deleted == 0).all()

@router.get("/devices",summary="Получаем список устройств",
             description="Возвращает список всех устройств")
async def goods(db: Session = Depends(deps.get_db)):
    return db.query(DeviceService).filter(DeviceService.is_deleted == 0).all()

@router.get("/template",summary="Получаем список этикеток'",
             description="Возвращает список всех этикеток")
async def goods(db: Session = Depends(deps.get_db)):
    return db.query(Template).filter(Template.is_deleted == 0).all()

@router.get("/clear_db/label_templ", summary="Очистка БД с данными О шаблонах этикеток",
             description="Очищаем таблицу с Шаблонами этикеток")
async def clear_label(db: Session = Depends(deps.get_db)):
    db.query(Template).delete()
    db.commit()
    return JSONResponse(status_code=200, content={'status': 'Success'})

@router.get("/clear_db/printers", summary="Очистка БД с данными о подключенных принтерах",
             description="Очищаем таблицу с Принтерами")
async def clear_printer(db: Session = Depends(deps.get_db)):
    db.query(PrinterService).delete()
    db.commit()
    return JSONResponse(status_code=200, content={'status': 'Success'})

@router.get("/clear_db/devices", summary="Очистка БД с данными о подключенных Устройствах",
             description="Очищаем таблицу с Устройствами")
async def clear_printer(db: Session = Depends(deps.get_db)):
    db.query(DeviceService).delete()
    db.commit()
    return JSONResponse(status_code=200, content={'status': 'Success'})

@router.get("/clear_db", summary="Очистка БД с всеми данными",
             description="Очищаем таблицы с Номенклатурой, Шаблона, Принтерами")
async def clear_all(db: Session = Depends(deps.get_db)):
    db.query(Template).delete()
    db.query(PrinterService).delete()
    db.commit()
    return JSONResponse(status_code=200, content={'status': 'Success'})