# app/routes/pharmacy.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal, engine
from app.models import Pharmacy, Mask, OpeningHour
from datetime import datetime, timedelta, timezone
from typing import Optional

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

@router.get("/mask-count")
def get_pharmacies_by_mask_count(
    min_price: float,
    max_price: float,
    threshold: int = Query(..., description="比較的口罩數量閾值"),
    more_than: bool = Query(True, description="True: 多於 threshold；False: 少於 threshold"),
    db: Session = Depends(get_db)
):
    pharmacies = db.query(Pharmacy).all()
    result = []

    for pharmacy in pharmacies:
        mask_count = db.query(Mask).filter(
            Mask.pharmacy_id == pharmacy.id,
            Mask.price >= min_price,
            Mask.price <= max_price
        ).count()

        if (more_than and mask_count > threshold) or (not more_than and mask_count < threshold):
            result.append({
                "pharmacy_id": pharmacy.id,
                "pharmacy_name": pharmacy.name,
                "mask_count": mask_count
            })

    return result