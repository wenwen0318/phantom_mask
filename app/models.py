# app/models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cash_balance = Column(Float, default=0.0)

    purchases = relationship("PurchaseHistory", back_populates="user")

class Pharmacy(Base):
    __tablename__ = "pharmacies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cash_balance = Column(Float, default=0.0)

    masks = relationship("Mask", back_populates="pharmacy")
    opening_hours = relationship("OpeningHour", back_populates="pharmacy")
    purchases = relationship("PurchaseHistory", back_populates="pharmacy")

class Mask(Base):
    __tablename__ = "masks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id"))
    pharmacy = relationship("Pharmacy", back_populates="masks")
    purchases = relationship("PurchaseHistory", back_populates="mask")

class OpeningHour(Base):
    __tablename__ = "opening_hours"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id"))
    weekday = Column(String, nullable=False)
    open_time = Column(String, nullable=False)
    close_time = Column(String, nullable=False)

    pharmacy = relationship("Pharmacy", back_populates="opening_hours")

class PurchaseHistory(Base):
    __tablename__ = "purchase_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id"))
    mask_id = Column(Integer, ForeignKey("masks.id"))
    amount = Column(Float)
    date = Column(String, nullable=False)

    user = relationship("User", back_populates="purchases")
    pharmacy = relationship("Pharmacy", back_populates="purchases")
    mask = relationship("Mask", back_populates="purchases")
