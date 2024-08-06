import asyncio
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from api import deps
from sqlalchemy.orm import Session
import datetime
import requests
import json
from decouple import config
from requests.exceptions import ConnectionError
from services.services import zpl_cmd,sgd_cmd,do_sgd,get_sgd,replace_attributes,object_as_dict,VENDOR_MODEL,decode_or_return
from models.LabelPrinter import PrinterTask,PrinterService,Template
from models.Goods import Goods



router = APIRouter()
now = datetime.datetime.now()

@router.get("/printer/zpl",summary="Вызвать действие на принтере",description="Отправить команду DО на принтер")
def do_sgd_to_print(host:str,port:int,zpl:str):
    return zpl_cmd(host,port,zpl)

@router.get("/printer/do",summary="Вызвать действие на принтере",description="Отправить команду DО на принтер. Например, перезагрузить принтер")
def do_sgd_to_print(host:str,port:int,cmd:str):
    return sgd_cmd(host,port,do_sgd(cmd))

@router.get("/printer/getvalue",summary="Получить значение настройки",description="Получение значения настройки от принтера. Например, проверить доступность принтера")
def get_sgd_to_print(host:str,port:int,get_key:str):
    return sgd_cmd(host,port,get_sgd(get_key))

@router.post("/print")
def print_task(task:PrinterTask,db: Session = Depends(deps.get_db)):
    try:
        print(task.json())
        temp_goods = db.query(Goods).filter(Goods.id == task.goods_id).first()
        if task.template_id != None:
            temp_temp = db.query(Template).filter(Template.id == task.template_id).first()
        else:
            temp_temp= db.query(Template).filter(Template.is_default == 1).first()

        if task.printer_id != None:
            temp_printer = db.query(PrinterService).filter(PrinterService.id == task.printer_id).first()
        else:
            temp_printer=db.query(PrinterService).filter(PrinterService.is_default == 1).first()
        cmd = replace_attributes(temp_temp.templ_data,object_as_dict(temp_goods))
        print(cmd)
        print(sgd_cmd(temp_printer.url,temp_printer.port,get_sgd(VENDOR_MODEL)))
        if sgd_cmd(temp_printer.url,temp_printer.port,get_sgd(VENDOR_MODEL)):
            print('Print ZPL')
            zpl_cmd(temp_printer.url,temp_printer.port,cmd)
            return JSONResponse(status_code=200, content={'status': 'Success'})
        else:
            return JSONResponse(status_code=500, content={'status': 'Error'})
    except:
        return JSONResponse(status_code=500, content={'status': 'Error'})

@router.get("/barcode_print",summary="Печать КМ в новый шаблон",description="Получаем в base64  штрихкод, затем получаем принтер по умолчанию и шаблон по умолчанию")
async def barcode(code, db: Session = Depends(deps.get_db)):
    code = decode_or_return(code)

    temp_temp = db.query(Template).filter(Template.is_default == 1).first()
    temp_printer = db.query(PrinterService).filter(PrinterService.is_default == 1).first()
    code = code.replace('@', '\\1D')
    data1 = code
    print(code)
    cmd = str(temp_temp.templ_data)
    cmd = cmd.replace('GS1_DM_CRPT',data1)
    print(cmd)
    print(sgd_cmd(temp_printer.url, temp_printer.port, get_sgd(VENDOR_MODEL)))
    if sgd_cmd(temp_printer.url, temp_printer.port, get_sgd(VENDOR_MODEL)):
        print('Print ZPL')
        zpl_cmd(temp_printer.url, temp_printer.port, cmd)
        return JSONResponse(status_code=200, content={'status': 'Success'})