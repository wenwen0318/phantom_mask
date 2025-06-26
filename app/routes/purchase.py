# app/routes/purchase.py

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.models import User, Mask, Pharmacy, PurchaseHistory
from app.schemas import PurchaseRequest

router = APIRouter()

@router.get("/purchase/summary")
def get_purchase_summary(
    start_date: str = Query(..., description="起始日期，格式 YYYY-MM-DD"),
    end_date: str = Query(..., description="結束日期，格式 YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    # 轉換為 datetime
    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date) + timedelta(days=1)
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式錯誤，請使用 YYYY-MM-DD")

    # 查詢指定區間的所有交易紀錄
    histories = db.query(PurchaseHistory).filter(
        PurchaseHistory.date >= start_dt,
        PurchaseHistory.date < end_dt
    ).all()

    total_quantity = len(histories)
    total_transaction = round(sum(h.amount for h in histories), 2)

    return {
        "total_quantity": total_quantity,
        "total_transaction": total_transaction
    }

@router.post("/")
def make_purchase(purchase: PurchaseRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == purchase.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_cost = 0
    purchase_records = []

    for item in purchase.items:
        mask = db.query(Mask).filter(Mask.id == item.mask_id).first()
        if not mask:
            raise HTTPException(status_code=404, detail=f"Mask not found")

        pharmacy = db.query(Pharmacy).filter(Pharmacy.id == mask.pharmacy_id).first()
        if not pharmacy:
            raise HTTPException(status_code=404, detail=f"Pharmacy not found for mask {item.mask_id}")

        cost = mask.price * item.quantity
        total_cost += cost

        # 建立購買紀錄
        purchase_records.append({
            "mask": mask,
            "pharmacy": pharmacy,
            "quantity": item.quantity,
            "amount": cost
        })

    total_cost = round(total_cost, 2)

    if user.cash_balance < total_cost:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # 開始扣款、寫入紀錄
    user.cash_balance = round(user.cash_balance - total_cost, 2)
    db.add(user)

    for record in purchase_records:
        record["pharmacy"].cash_balance = round(record["pharmacy"].cash_balance + record["amount"], 2)
        db.add(record["pharmacy"])

        db.add(PurchaseHistory(
            user_id=user.id,
            pharmacy_id=record["pharmacy"].id,
            mask_id=record["mask"].id,
            amount=record["amount"],
            date=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None)
        ))

    db.commit()

    return {"message": "Purchase completed", "total_spent": total_cost}
