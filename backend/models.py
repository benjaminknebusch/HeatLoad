from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Relationship with projects
    projects = relationship("Project", back_populates="owner")

    def set_password(self, password: str):
        """Set the password after hashing it."""
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str):
        """Verify a given password against the stored hashed password."""
        return pwd_context.verify(password, self.hashed_password)


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="projects")
    buildings = relationship("Building", back_populates="project")

class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    norm_outside_temp = Column(Float)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="buildings")
    floors = relationship("Floor", back_populates="building")

class Floor(Base):
    __tablename__ = "floors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    building = relationship("Building", back_populates="floors")
    rooms = relationship("Room", back_populates="floor")

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    floor_id = Column(Integer, ForeignKey("floors.id"))
    floor = relationship("Floor", back_populates="rooms")
    # Add fields for heat loss areas
    outer_wall_area = Column(Float)
    roof_area = Column(Float)
    roof_window_area = Column(Float)
    outer_window_area = Column(Float)
    outer_door_area = Column(Float)
    ceiling_to_unheated_area = Column(Float)
    floor_to_unheated_area = Column(Float)
    wall_to_unheated_area = Column(Float)