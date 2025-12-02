from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import datetime, json
from collections import Counter

from database import SessionLocal
from models import Piloto, Escuderia, Circuito, Tiempo

router = APIRouter(tags=["Dashboard"])
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard", include_in_schema=False)
def dashboard(request: Request, db: Session = Depends(get_db)):
    # Pilotos por escudería
    escuderias = db.query(Escuderia).all()
    esc_labels = [e.nombre for e in escuderias if e.activo]
    pilotos_count = [db.query(Piloto).filter(Piloto.escuderia_id == e.id, Piloto.activo == True).count() for e in escuderias if e.activo]

    # Tiempos promedio por circuito
    circuitos = db.query(Circuito).all()
    circ_labels = [c.nombre for c in circuitos if c.activo]
    tiempos_promedio = []
    for c in circuitos:
        tiempos = db.query(Tiempo).filter(Tiempo.circuito_id == c.id, Tiempo.activo == True).all()
        tiempos_promedio.append(round(sum([t.tiempo_vuelta for t in tiempos]) / len(tiempos), 2) if tiempos else 0)

    # Pilotos por nacionalidad
    nacionalidades = [p.nacionalidad for p in db.query(Piloto).filter(Piloto.activo == True).all()]
    nacionalidades_count = Counter(nacionalidades)

    # Escuderías activas vs eliminadas
    escuderias_activas = db.query(Escuderia).filter(Escuderia.activo == True).count()
    escuderias_inactivas = db.query(Escuderia).filter(Escuderia.activo == False).count()

    # Longitud de circuitos
    longitudes = [c.longitud_km for c in db.query(Circuito).filter(Circuito.activo == True, Circuito.longitud_km != None).all()]

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "escuderias": json.dumps(esc_labels),
        "pilotos_count": json.dumps(pilotos_count),
        "circuitos": json.dumps(circ_labels),
        "tiempos_promedio": json.dumps(tiempos_promedio),
        "nacionalidades_labels": json.dumps(list(nacionalidades_count.keys())),
        "nacionalidades_data": json.dumps(list(nacionalidades_count.values())),
        "escuderias_status_labels": json.dumps(["Activas", "Eliminadas"]),
        "escuderias_status_data": json.dumps([escuderias_activas, escuderias_inactivas]),
        "longitudes": json.dumps(longitudes),
        "current_year": datetime.datetime.now().year
    })