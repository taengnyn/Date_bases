from sqlalchemy import Column, Integer, String, Float, Date, Time, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

# Enum для напрямку вітру
class WindDirectionEnum(str, enum.Enum):
    N = "N"
    NE = "NE"
    E = "E"
    SE = "SE"
    S = "S"
    SW = "SW"
    W = "W"
    NW = "NW"
    Variable = "Variable"

# Основна таблиця — Погода
class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    last_updated = Column(Date, nullable=False)
    sunrise = Column(Time, nullable=True)

    # Зв'язок з таблицею Wind
    wind = relationship("Wind", back_populates="weather", uselist=False)

# Таблиця з параметрами вітру
class Wind(Base):
    __tablename__ = "wind"

    id = Column(Integer, primary_key=True, index=True)
    weather_id = Column(Integer, ForeignKey("weather.id"), nullable=False, unique=True)
    
    wind_degree = Column(Integer)
    wind_kph = Column(Float)
    wind_direction = Column(Enum(WindDirectionEnum))
    
    should_go_outside = Column(Boolean)  # "Чи варто виходити?"

    weather = relationship("Weather", back_populates="wind")
