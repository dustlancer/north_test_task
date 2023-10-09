from ast import Return
from sqlalchemy import Null
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import func
from db.models import Coil
from schemas import CoilBase, StatsReq, CoilsRequest
from fastapi import HTTPException, status
from datetime import date


# Создать рулон
def create_coil(db: Session, request: CoilBase):
    new_coil = Coil(
        length = request.length,
        weight = request.weight,
        added = date.today(),
        deleted = request.deleted
    )
    
    db.add(new_coil)
    db.commit()
    db.refresh(new_coil)
    return new_coil.id


# Получить рулоны(все, либо фильтрация по комбинации диапазонов)
# Диапазон id вида [2,4] выведет рулоны с id 2,3,4
def get_coils(db: Session, request: CoilsRequest = None):
    coils = db.query(Coil)
    if not coils:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail = f"no coils found")
    
    if request!=None:
        if request.id_range:
            coils = coils.filter(Coil.id.between(request.id_range[0], request.id_range[1]))
        if request.length_range:
            coils = coils.filter(Coil.length.between(request.length_range[0], request.length_range[1]))
        if request.weight_range:
            coils = coils.filter(Coil.weight.between(request.weight_range[0], request.weight_range[1]))
        if request.added_range:
            coils = coils.filter(Coil.added.between(request.added_range[0], request.added_range[1]))
        if request.deleted_range:
            coils = coils.filter(Coil.deleted.between(request.deleted_range[0], request.deleted_range[1]))

    return(coils.all())



# Удалить рулон
def delete_coil(db: Session, id: int):
    coil = db.query(Coil).filter(Coil.id == id).first()
    if not coil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail = f"coil with id {id} not found.")
    coil.deleted=date.today()
    db.commit()
    db.refresh(coil)

    return {"ok": True}


# Получить конкретный рулон по id
def get_coil(db: Session, id: int):
    coil = db.query(Coil).filter(Coil.id == id).first()
    if not coil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail = f"coil with id {id} not found.")
    
    return coil


# Получить статистику за определённый период
def get_stats(db: Session, request: StatsReq):
    if request == None:
        return({"Error": "input json is missing"})
    start_date = request.start_date
    end_date = request.end_date
    total_coils = db.query(Coil).filter(Coil.added.between(start_date, end_date)).count()
    total_deleted_coils = db.query(Coil).filter(Coil.added.between(start_date, end_date)).filter(Coil.deleted != None).count()
    avg_length = db.query(func.avg(Coil.length)).filter(Coil.added.between(start_date, end_date)).scalar()
    avg_weight = db.query(func.avg(Coil.weight)).filter(Coil.added.between(start_date, end_date)).scalar()
    max_length = db.query(func.max(Coil.length)).filter(Coil.added.between(start_date, end_date)).scalar()
    max_weight = db.query(func.max(Coil.weight)).filter(Coil.added.between(start_date, end_date)).scalar()
    total_weight = db.query(func.sum(Coil.weight).filter(Coil.added.between(start_date, end_date))).scalar()

    return {
            "total_coils": total_coils,
            "total_deleted_coils": total_deleted_coils,
            "avg_length": avg_length,
            "avg_weight": avg_weight,
            "max_length": max_length,
            "max_weight": max_weight,
            "total_weight": total_weight
        }