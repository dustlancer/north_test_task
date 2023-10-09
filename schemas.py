import datetime
from tokenize import Double
from pydantic import BaseModel
from typing import Optional, List

class CoilBase(BaseModel):
    length : float 
    weight : float
    added : Optional[datetime.date] = None
    deleted : Optional[datetime.date] = None


class CoilDisp(BaseModel):
    id: int
    length : float 
    weight : float
    added : datetime.date
    deleted : datetime.date

class CoilsRequest(BaseModel):
    id_range: Optional[List[int]] = None
    length_range: Optional[List[float]] = None
    weight_range: Optional[List[float]] = None
    added_range: Optional[List[datetime.date]] = None
    deleted_range: Optional[List[datetime.date]] = None


class StatsReq(BaseModel):
    start_date : datetime.date
    end_date : datetime.date


