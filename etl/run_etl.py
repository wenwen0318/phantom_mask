import json
import re
from datetime import datetime
from app.database import SessionLocal
from app.models import Pharmacy, Mask, User, PurchaseHistory, OpeningHour

WEEKDAY_ALIASES = {
    "Mon": "Monday",
    "Tue": "Tuesday",
    "Wed": "Wednesday",
    "Thu": "Thursday",
    "Thur": "Thursday",
    "Fri": "Friday",
    "Sat": "Saturday",
    "Sun": "Sunday"
}

def get_day_range(start, end):
    days_order = ["Mon", "Tue", "Wed", "Thu", "Thur", "Fri", "Sat", "Sun"]
    start_idx = days_order.index(start)
    end_idx = days_order.index(end)
    return days_order[start_idx:end_idx + 1]

def parse_opening_hours(opening_str):
    result = []
    sections = opening_str.split('/')
    for section in sections:
        section = section.strip()
        match = re.search(r'(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})', section)
        if not match:
            print(f"⚠️ 無法解析時間段：{section}")
            continue
        open_time, close_time = match.group(1), match.group(2)
        day_part = section[:match.start()].strip()
        if '-' in day_part:
            start_day, end_day = [d.strip() for d in day_part.split('-', 1)]
            days = get_day_range(start_day, end_day)
        else:
            days = [d.strip() for d in day_part.split(',')]
        for d in days:
            full_day = WEEKDAY_ALIASES.get(d, d)
            result.append((full_day, open_time, close_time))
    return result

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def insert_pharmacies(data, db):
    for p in data:
        pharmacy = Pharmacy(name=p['name'], cash_balance=p['cashBalance'])
        db.add(pharmacy)
        db.commit()

        for mask in p['masks']:
            db.add(Mask(name=mask['name'], price=mask['price'], pharmacy_id=pharmacy.id))

        for weekday, open_time, close_time in parse_opening_hours(p['openingHours']):
            db.add(OpeningHour(pharmacy_id=pharmacy.id, weekday=weekday, open_time=open_time, close_time=close_time))

        db.commit()

def insert_users(data, db):
    for u in data:
        user = User(name=u['name'], cash_balance=u['cashBalance'])
        db.add(user)
        db.commit()

        for p in u['purchaseHistories']:
            pharmacy = db.query(Pharmacy).filter_by(name=p['pharmacyName']).first()
            mask = db.query(Mask).filter_by(name=p['maskName']).first()
            db.add(PurchaseHistory(
                user_id=user.id,
                pharmacy_id=pharmacy.id if pharmacy else None,
                mask_id=mask.id if mask else None,
                amount=p['transactionAmount'],
                date=p['transactionDate']
            ))
        db.commit()

def run():
    db = SessionLocal()
    try:
        insert_pharmacies(load_json("./data/pharmacies.json"), db)
        insert_users(load_json("./data/users.json"), db)
        print("ETL 完成，資料已成功導入資料庫！")
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run()
