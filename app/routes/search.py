from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Pharmacy, Mask

router = APIRouter()

def compute_relevance(name: str, keyword: str) -> int:
    """計算關鍵字出現在名稱的位置，越前面越相關"""
    name_lower = name.lower()
    keyword_lower = keyword.lower()
    index = name_lower.find(keyword_lower)
    return index if index != -1 else float('inf')

@router.get("/")
def search_all(
    type: str = Query("mask", enum=["mask", "pharmacy"], description="搜尋類型：mask 或 pharmacy"),
    keyword: str = Query(..., min_length=1, description="搜尋關鍵字"),
    db: Session = Depends(get_db)
):
    keyword_pattern = f"%{keyword}%"

    if type == "mask":
        masks = db.query(Mask).filter(Mask.name.ilike(keyword_pattern)).all()
        if not masks:
            raise HTTPException(status_code=404, detail="沒有找到符合的口罩。")
        
        masks_sorted = sorted(masks, key=lambda m: compute_relevance(m.name, keyword))
        return [{"id": m.id, "name": m.name, "price": m.price}for m in masks_sorted]

    else:
        pharmacies = db.query(Pharmacy).filter(Pharmacy.name.ilike(keyword_pattern)).all()
        if not pharmacies:
            raise HTTPException(status_code=404, detail="沒有找到符合的藥局。")
        
        pharmacies_sorted = sorted(pharmacies, key=lambda p: compute_relevance(p.name, keyword))
        return [{"id": p.id, "name": p.name}for p in pharmacies_sorted]
