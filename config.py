from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Заміни ці значення на свої
DATABASE_URL = "postgresql://postgres:dariismyname@localhost:5432/weatherdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
