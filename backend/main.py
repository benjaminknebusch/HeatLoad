from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend import models, crud, auth
from backend.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="frontend/templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Startseite
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# Projekte verwalten
@app.get("/projects", response_class=HTMLResponse)
async def read_projects(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    projects = crud.get_user_projects(db, current_user.id)
    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})

@app.post("/projects", response_class=RedirectResponse)
async def create_project(request: Request, name: str = Form(...), db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    crud.create_project(db, name, current_user.id)
    return RedirectResponse(url="/projects", status_code=303)

# Gebäude verwalten
@app.get("/buildings/{project_id}", response_class=HTMLResponse)
async def read_buildings(request: Request, project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    buildings = crud.get_project_buildings(db, project_id)
    return templates.TemplateResponse("buildings.html", {"request": request, "buildings": buildings, "project_id": project_id})

@app.post("/buildings/{project_id}", response_class=RedirectResponse)
async def create_building(request: Request, project_id: int, name: str = Form(...), location: str = Form(...), norm_outside_temp: float = Form(...), db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    crud.create_building(db, name, location, norm_outside_temp, project_id)
    return RedirectResponse(url=f"/buildings/{project_id}", status_code=303)

# Etagen verwalten
@app.get("/floors/{building_id}", response_class=HTMLResponse)
async def read_floors(request: Request, building_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    floors = crud.get_building_floors(db, building_id)
    return templates.TemplateResponse("floors.html", {"request": request, "floors": floors, "building_id": building_id})

@app.post("/floors/{building_id}", response_class=RedirectResponse)
async def create_floor(request: Request, building_id: int, name: str = Form(...), db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    crud.create_floor(db, name, building_id)
    return RedirectResponse(url=f"/floors/{building_id}", status_code=303)

# Räume verwalten
@app.get("/rooms/{floor_id}", response_class=HTMLResponse)
async def read_rooms(request: Request, floor_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    rooms = crud.get_floor_rooms(db, floor_id)
    return templates.TemplateResponse("rooms.html", {"request": request, "rooms": rooms, "floor_id": floor_id})

@app.post("/rooms/{floor_id}", response_class=RedirectResponse)
async def create_room(request: Request, floor_id: int, name: str = Form(...), outer_wall_area: float = Form(...), roof_area: float = Form(...), roof_window_area: float = Form(...), outer_window_area: float = Form(...), outer_door_area: float = Form(...), ceiling_to_unheated_area: float = Form(...), floor_to_unheated_area: float = Form(...), wall_to_unheated_area: float = Form(...), db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    crud.create_room(db, name, outer_wall_area, roof_area, roof_window_area, outer_window_area, outer_door_area, ceiling_to_unheated_area, floor_to_unheated_area, wall_to_unheated_area, floor_id)
    return RedirectResponse(url=f"/rooms/{floor_id}", status_code=303)

# Heizlastberechnung
def calculate_heat_loss(room: models.Room, norm_outside_temp: float):
    # Beispielberechnung (vereinfacht)
    heat_loss = (
        room.outer_wall_area * 0.3 +
        room.roof_area * 0.2 +
        (room.roof_window_area + room.outer_window_area) * 0.5 +
        room.outer_door_area * 0.4 +
        room.ceiling_to_unheated_area * 0.1 +
        room.floor_to_unheated_area * 0.1 +
        room.wall_to_unheated_area * 0.1
    ) * (20 - norm_outside_temp)  # Annahme: Raumtemperatur = 20°C
    return heat_loss

# Gesamtergebnisseite
@app.get("/results/{project_id}", response_class=HTMLResponse)
async def read_results(request: Request, project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    buildings = crud.get_project_buildings(db, project_id)
    results = []
    for building in buildings:
        floors = crud.get_building_floors(db, building.id)
        for floor in floors:
            rooms = crud.get_floor_rooms(db, floor.id)
            for room in rooms:
                heat_loss = calculate_heat_loss(room, building.norm_outside_temp)
                results.append({
                    "building": building.name,
                    "floor": floor.name,
                    "room": room.name,
                    "heat_loss": heat_loss
                })
    total_heat_loss = sum(result["heat_loss"] for result in results)
    return templates.TemplateResponse("results.html", {"request": request, "results": results, "total_heat_loss": total_heat_loss})

def main():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9090)

if __name__ == '__main__':
    main()