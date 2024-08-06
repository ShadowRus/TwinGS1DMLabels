from sqlalchemy import Column, Integer, String
from api.deps import Base

from pydantic import BaseModel, HttpUrl, Field
from typing import Sequence, List, Optional

class Goods(Base):
    __tablename__="Goods"
    id = Column(Integer, primary_key=True, index=True)
    goods_name = Column(String)
    id_1 = Column(String,index=True)
    id_2 = Column(String,index=True)
    id_3 = Column(String)
    id_4 = Column(String)
    id_5 = Column(String)
    attr_1 = Column(String,index=True)
    attr_2= Column(String,index=True)
    attr_3 = Column(String)
    attr_4 = Column(String)
    attr_5 = Column(String)
    attr_6 = Column(String)
    is_deleted = Column(Integer)
    is_add_at = Column(String)
    is_manual = Column(Integer)
    source = Column(String)

class GoodsId(Base):
    __tablename__ = "GoodsID"
    id = Column(Integer, primary_key=True, index=True)
    goods_name = Column(String)
    id_1 = Column(String)
    id_2 = Column(String)
    id_3 = Column(String)
    id_4 = Column(String)
    id_5 = Column(String)
    attr_1 = Column(String)
    attr_2 = Column(String)
    attr_3 = Column(String)
    attr_4 = Column(String)
    attr_5 = Column(String)
    attr_6 = Column(String)
    is_add_at = Column(String)
    source = Column(String)



class AddGoodsRespone(BaseModel):
    goods_name: str=Field()
    id_1: str=Field()
    id_2:Optional[str]=None
    id_3:Optional[str]=None
    id_4:Optional[str]=None
    id_5:Optional[str]=None
    attr_1:Optional[str]=None
    attr_2:Optional[str]=None
    attr_3:Optional[str]=None
    attr_4:Optional[str]=None
    attr_5:Optional[str]=None
    attr_6:Optional[str]=None

