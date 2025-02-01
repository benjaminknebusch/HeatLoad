from pydantic import BaseModel
from typing import List, Optional

# Benutzer
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# Projekte
class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# Gebäude
class BuildingBase(BaseModel):
    name: str
    location: str
    norm_outside_temp: float

class BuildingCreate(BuildingBase):
    pass

class Building(BuildingBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True

# Etagen
class FloorBase(BaseModel):
    name: str

class FloorCreate(FloorBase):
    pass

class Floor(FloorBase):
    id: int
    building_id: int

    class Config:
        from_attributes = True

# Räume
class RoomBase(BaseModel):
    name: str
    outer_wall_area: float
    roof_area: float
    roof_window_area: float
    outer_window_area: float
    outer_door_area: float
    ceiling_to_unheated_area: float
    floor_to_unheated_area: float
    wall_to_unheated_area: float

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    floor_id: int

    class Config:
        from_attributes = True