import json
from sqlalchemy.orm import Session
from model.models import City, Street, Location
from decimal import Decimal
from database.db import SessionLocal  # ← твой engine

with open("address.json", "r", encoding="utf-8") as f:
    data = json.load(f)

session = SessionLocal()

# Город Караганда
city_name = "Караганда"
city = session.query(City).filter_by(city_name=city_name).first()
if not city:
    city = City(city_name=city_name)
    session.add(city)
    session.commit()

for element in data.get("elements", []):
    tags = element.get("tags", {})
    if not tags:
        continue

    street_name = tags.get("addr:street")
    house_number = tags.get("addr:housenumber")

    # Пропустить, если нет адреса
    if not (street_name and house_number):
        continue

    # Координаты
    lat = element.get("lat") or element.get("center", {}).get("lat")
    lon = element.get("lon") or element.get("center", {}).get("lon")

    if not (lat and lon):
        continue  # если нет координат — пропускаем

    # Создаём или получаем улицу
    street = session.query(Street).filter_by(street_name=street_name, city_id=city.id).first()
    if not street:
        street = Street(street_name=street_name, city=city)
        session.add(street)
        session.commit()

    # Проверка на дубликат
    exists = session.query(Location).filter_by(
        street_id=street.id,
        number=house_number,
        latitude=Decimal(str(lat)),
        longitude=Decimal(str(lon))
    ).first()

    if not exists:
        location = Location(
            number=house_number,
            latitude=Decimal(str(lat)),
            longitude=Decimal(str(lon)),
            street=street
        )
        session.add(location)

session.commit()
session.close()
print("✅ Импорт завершён.")
