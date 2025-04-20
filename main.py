import csv
from datetime import datetime
from sqlalchemy.orm import Session
from config import SessionLocal
from models.weather import Weather, Wind, WindDirectionEnum

def should_go_outside_formula(wind_kph, wind_degree):
    if wind_kph and wind_kph > 30:
        return False
    if wind_degree and 0 <= wind_degree <= 20:
        return False
    return True

def load_weather_data(csv_file_path: str):
    db: Session = SessionLocal()
    with open(csv_file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                weather = Weather(
                    country=row['country'],
                    last_updated=datetime.strptime(row['last_updated'], "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M"),
                    sunrise=datetime.strptime(row['sunrise'], "%I:%M %p").time() if row['sunrise'] else None
                )
                db.add(weather)
                db.flush()  # Отримаємо weather.id

                wind = Wind(
                    weather_id=weather.id,
                    wind_degree=int(row['wind_degree']) if row['wind_degree'] else None,
                    wind_kph = float(row.get('wind_kph', 0)) if row.get('wind_kph') else None,
                    wind_direction=WindDirectionEnum(row['wind_direction']) if row['wind_direction'] in WindDirectionEnum.__members__ else None,
                    should_go_outside=should_go_outside_formula(
                        float(row['wind_kph']) if row['wind_kph'] else None,
                        int(row['wind_degree']) if row['wind_degree'] else None
                    )
                )
                db.add(wind)
                print(f"✅ Added weather and wind: {weather.country}, {wind.wind_kph}")
            except Exception as e:
                print(f"❌ Error processing row: {row}\n{e}")

        db.commit()
    db.close()

if __name__ == "__main__":
    csv_path = "data/weather.csv"  # заміни на фактичний шлях
    load_weather_data(csv_path)
