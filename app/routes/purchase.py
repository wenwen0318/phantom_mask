# app/routes/purchase.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Mask, Pharmacy, PurchaseHistory
from app.schemas import PurchaseRequest
from datetime import datetime

router = APIRouter()

@router.post("/purchase")
def make_purchase(purchase: PurchaseRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == purchase.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_cost = 0
    mask_objs = []

    # 檢查庫存與金額
    for item in purchase.items:
        mask = db.query(Mask).filter(Mask.id == item.mask_id).first()
        if not mask:
            raise HTTPException(status_code=404, detail=f"Mask ID {item.mask_id} not found")

        cost = mask.price * item.quantity
        total_cost += cost
        mask_objs.append((mask, item.quantity, cost))

    if user.cash_balance < total_cost:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # 扣款、加到藥局、寫交易紀錄
    user.cash_balance -= total_cost
    db.add(user)

    for mask, qty, cost in mask_objs:
        pharmacy = db.query(Pharmacy).filter(Pharmacy.id == mask.pharmacy_id).first()
        pharmacy.cash_balance += cost
        db.add(pharmacy)

        history = PurchaseHistory(
            user_id=user.id,
            pharmacy_id=pharmacy.id,
            mask_id=mask.id,
            amount=cost,
            date=datetime.utcnow().isoformat()
        )
        db.add(history)

    db.commit()
    return { "message": "Purchase successful", "total_spent": total_cost }
