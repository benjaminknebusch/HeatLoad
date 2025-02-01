from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

# Benutzer
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Projekte
def get_user_projects(db: Session, user_id: int):
    return db.query(models.Project).filter(models.Project.user_id == user_id).all()

def create_project(db: Session, name: str, user_id: int):
    db_project = models.Project(name=name, user_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# Gebäude
def get_project_buildings(db: Session, project_id: int):
    return db.query(models.Building).filter(models.Building.project_id == project_id).all()

def create_building(db: Session, name: str, location: str, norm_outside_temp: float, project_id: int):
    db_building = models.Building(name=name, location=location, norm_outside_temp=norm_outside_temp, project_id=project_id)
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building

# Etagen
def get_building_floors(db: Session, building_id: int):
    return db.query(models.Floor).filter(models.Floor.building_id == building_id).all()

def create_floor(db: Session, name: str, building_id: int):
    db_floor = models.Floor(name=name, building_id=building_id)
    db.add(db_floor)
    db.commit()
    db.refresh(db_floor)
    return db_floor

# Räume
def get_floor_rooms(db: Session, floor_id: int):
    return db.query(models.Room).filter(models.Room.floor_id == floor_id).all()

def create_room(db: Session, name: str, outer_wall_area: float, roof_area: float, roof_window_area: float, outer_window_area: float, outer_door_area: float, ceiling_to_unheated_area: float, floor_to_unheated_area: float, wall_to_unheated_area: float, floor_id: int):
    db_room = models.Room(
        name=name,
        outer_wall_area=outer_wall_area,
        roof_area=roof_area,
        roof_window_area=roof_window_area,
        outer_window_area=outer_window_area,
        outer_door_area=outer_door_area,
        ceiling_to_unheated_area=ceiling_to_unheated_area,
        floor_to_unheated_area=floor_to_unheated_area,
        wall_to_unheated_area=wall_to_unheated_area,
        floor_id=floor_id
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room