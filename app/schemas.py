from fastapi import FastAPI, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Pharmacy
from app.schemas import Pharmacy as PharmacySchema

from pydantic import BaseModel
from typing import List

app = FastAPI()

# 取得資料庫 session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PurchaseItem(BaseModel):
    mask_id: int
    quantity: int

class PurchaseRequest(BaseModel):
    user_id: int
    items: List[PurchaseItem]