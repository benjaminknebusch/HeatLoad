from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite-Datenbank-URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./heatload.db"

# Datenbank-Engine erstellen
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal für Datenbankoperationen
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basisklasse für Modelle
Base = declarative_base()

# Dependency für Datenbank-Sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()