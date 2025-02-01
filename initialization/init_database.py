from backend.database import engine, Base
from backend.models import User, Project, Building, Floor, Room

# Tabellen erstellen
Base.metadata.create_all(bind=engine)