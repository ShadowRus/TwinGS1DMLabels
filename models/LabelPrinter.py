from sqlalchemy import Column, Integer, String
from api.deps import Base

from pydantic import BaseModel, HttpUrl, Field
from typing import Sequence, List, Optional

class Template(Base):
    __tablename__ = "PrintTemplates"
    id = Column(Integer, primary_key=True, index=True)
    templ_name = Column(String)
    templ_data = Column(String)
    is_default = Column(Integer)
    is_deleted = Column(Integer)

class TemplateResponse(BaseModel):
    name:str=Field(default=None)
    label: str = Field()
    is_default: int = Field(default=0)

class PrinterService(Base):
    __tablename__="Printer"
    id = Column(Integer, primary_key=True, index=True)
    print_name = Column(String)
    url = Column(String)
    port = Column(Integer)
    type = Column(Integer)
    # 1 - net printer, 2 - printer service pdt
    is_default = Column(Integer)
    is_online = Column(Integer)
    is_deleted = Column(Integer)

class DeviceService(Base):
    __tablename__="Device"
    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String)
    url = Column(String)
    is_deleted = Column(Integer)

class PrinterRespone(BaseModel):
    name: str=Field()
    url: str=Field()
    port:int= Field(default=9100)
    type:int=Field(default=1)
    is_default: int=Field(default = 0)

class DeviceRespone(BaseModel):
    name: str=Field()
    url: str=Field()

class PrinterTask(BaseModel):
    goods_id:int= Field()
    printer_id:Optional[int]=None
    template_id:Optional[int]=None
    data:Optional[dict]=None