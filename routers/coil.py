from tkinter import N
from urllib import request
from click import Option
from fastapi import APIRouter, Depends
from typing import List
from schemas import CoilBase, CoilDisp, StatsReq, CoilsRequest
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_coil
from typing import Optional


router = APIRouter( 
    prefix='/coil',
    tags = ['coil']
)

# Добавить рулон
@router.post('/')
def create_coil(request: CoilBase, db: Session = Depends(get_db)):
    return db_coil.create_coil(db, request)

# Получить рулоны
@router.get('/')
def get_coils(request: Optional[CoilsRequest]=None, db: Session = Depends(get_db)):
    return db_coil.get_coils(db, request)

# Получить статистику
@router.get('/stats')
def get_stats(request: Optional[StatsReq]=None, db: Session=Depends(get_db)):
    return db_coil.get_stats(db, request)

# Удалить рулон
@router.delete('/{coil_id}')
def delete_coil(coil_id: int, db:Session = Depends(get_db)):
    return db_coil.delete_coil(db, coil_id)

# Получить конкретный рулон по id
@router.get('/{coil_id}', response_model=CoilDisp)
def get_article(coil_id: int, db: Session = Depends(get_db)):
    return db_coil.get_coil(db, coil_id)


