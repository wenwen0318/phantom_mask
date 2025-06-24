from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models import Pharmacy, Mask

router = APIRouter()
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
    return db.query(Mask).all()


@router.get("/by-pharmacy/{pharmacy_id}")
def get_masks_by_pharmacy(
    pharmacy_id: int,
    sort_by: str = Query("name", enum=["name", "price"]),
    db: Session = Depends(get_db)
):
    order = Mask.name.asc() if sort_by == "name" else Mask.price.asc()
    masks = db.query(Mask).filter(Mask.pharmacy_id == pharmacy_id).order_by(order).all()

    return [{"id": m.id, "name": m.name, "price": m.price} for m in masks]
