from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Pharmacy, Mask, User

router = APIRouter()

@router.get("/")
def search_all(
    keyword: str = Query(..., description="搜尋關鍵字"),
    db: Session = Depends(get_db)
):
    results = {"pharmacies": [], "masks": [], "users": []}

    results["pharmacies"] = db.query(Pharmacy).filter(Pharmacy.name.ilike(f"%{keyword}%")).all()
    results["masks"] = db.query(Mask).filter(Mask.name.ilike(f"%{keyword}%")).all()
    results["users"] = db.query(User).filter(User.name.ilike(f"%{keyword}%")).all()

    return {
        "pharmacies": [{"id": p.id, "name": p.name} for p in results["pharmacies"]],
        "masks": [{"id": m.id, "name": m.name, "price": m.price} for m in results["masks"]],
        "users": [{"id": u.id, "name": u.name} for u in results["users"]],
    }
