from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models import User, PurchaseHistory
from datetime import datetime

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
    return db.query(User).all()

@router.get("/top-spenders")
def get_top_spenders(
    start: str,
    end: str,
    top_n: int = 5,
    db: Session = Depends(get_db)
):
    histories = db.query(PurchaseHistory).all()
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    spending = {}

    for h in histories:
        h_date = datetime.fromisoformat(h.date)
        if start_dt <= h_date <= end_dt:
            spending[h.user_id] = spending.get(h.user_id, 0) + h.amount

    users = db.query(User).filter(User.id.in_(spending.keys())).all()
    ranked = sorted(users, key=lambda u: spending[u.id], reverse=True)

    return [
        {"user_id": u.id, "name": u.name, "total_spent": spending[u.id]}
        for u in ranked[:top_n]
    ]
