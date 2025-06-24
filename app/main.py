# app/main.py
from fastapi import FastAPI
from app.database import engine
from app.models import Base

from app.init__db import init_db
from app.routes import pharmacy, mask, user, purchase, search

init_db()

app = FastAPI(title="Phantom Mask API")

app.include_router(pharmacy.router, prefix="/pharmacies", tags=["Pharmacies"])
app.include_router(mask.router, prefix="/masks", tags=["Masks"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(purchase.router, prefix="/purchase", tags=["Purchase"])
app.include_router(search.router, prefix="/search", tags=["Search"])