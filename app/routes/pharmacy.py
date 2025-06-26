# app/routes/pharmacy.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal, engine
from app.models import Pharmacy, Mask, OpeningHour
from datetime import datetime, timedelta, timezone
import operator

router = APIRouter()

# Dependency：取得資料庫 session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_pharmacies(
    db: Session = Depends(get_db)
):
    return db.query(Pharmacy).all()

@router.get("/opening")
def get_open_pharmacies(
    weekday: str = Query(None),
    time: str = Query(None),
    db: Session = Depends(get_db)
):
    # 若都未提供，則預設為目前台灣時間
    if weekday is None and time is None:
        now = datetime.now(timezone(timedelta(hours=8)))  # 台灣時區 UTC+8
        weekday = now.strftime("%A")
        time = now.strftime("%H:%M")
        opening_hours = db.query(OpeningHour).filter(
            OpeningHour.weekday == weekday,
            OpeningHour.open_time <= time,
            OpeningHour.close_time >= time
        ).all()
    elif weekday is None:
        opening_hours = db.query(OpeningHour).filter(
        OpeningHour.open_time <= time,
        OpeningHour.close_time >= time
        ).all()
    elif time is None:
        opening_hours = db.query(OpeningHour).filter(
        OpeningHour.weekday == weekday
        ).all()
    else :
        opening_hours = db.query(OpeningHour).filter(
            OpeningHour.weekday == weekday,
            OpeningHour.open_time <= time,
            OpeningHour.close_time >= time
        ).all()

    if not opening_hours:
        raise HTTPException(status_code=404, detail="No pharmacies open at this time.")

    # 取得對應的藥局
    pharmacy_ids = [oh.pharmacy_id for oh in opening_hours]
    pharmacies = db.query(Pharmacy).filter(Pharmacy.id.in_(pharmacy_ids)).all()

    return pharmacies

@router.get("/{pharmacy_id}/masks")
def get_pharmacy_masks(
    pharmacy_id: int,
    sort_by: str = Query("name", enum=["name", "price"]),
    order: str = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db)
):
    pharmacy = db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()
    if not pharmacy:
        raise HTTPException(status_code=404, detail="Pharmacy not found")

    query = db.query(Mask).filter(Mask.pharmacy_id == pharmacy_id)

    # 套用排序
    if sort_by == "name":
        query = query.order_by(Mask.name.asc() if order == "asc" else Mask.name.desc())
    else:
        query = query.order_by(Mask.price.asc() if order == "asc" else Mask.price.desc())

    masks = query.all()

    return {
        "pharmacy": pharmacy.name,
        "masks": [
            {
                "name": m.name,
                "price": m.price
            } for m in masks
        ]
    }

comparison_ops = {
    "gt": operator.gt,
    "lt": operator.lt,
    "ge": operator.ge,
    "le": operator.le,
    "eq": operator.eq,
}

@router.get("/pharmacies/mask_count")
def get_pharmacies_by_mask_count(
    min_price: float = Query(..., description="價格下限"),
    max_price: float = Query(..., description="價格上限"),
    count: int = Query(..., description="要比較的口罩數量"),
    op: str = Query(..., description="運算子：gt, lt, ge, le, eq"),
    db: Session = Depends(get_db)
):
    if op not in comparison_ops:
        raise HTTPException(status_code=400, detail="無效的運算子，必須是：gt, lt, ge, le, eq")

    compare_fn = comparison_ops[op]

    result = []
    pharmacies = db.query(Pharmacy).all()

    for pharmacy in pharmacies:
        mask_count = db.query(Mask).filter(
            Mask.pharmacy_id == pharmacy.id,
            Mask.price >= min_price,
            Mask.price <= max_price
        ).count()

        if compare_fn(mask_count, count):
            result.append({
                "id": pharmacy.id,
                "name": pharmacy.name,
                "cash_balance": pharmacy.cash_balance,
                "mask_count": mask_count
            })

    return result