import base64
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

from database import SessionLocal
from models import Escuderia, Piloto

router = APIRouter(prefix="/teams", tags=["Teams"])
templates = Jinja2Templates(directory="templates")

# -----------------------------
# Dependencia de sesión
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Utilidad: convertir binario a base64
# -----------------------------
def convertir_imagen(binario):
    return base64.b64encode(binario).decode("utf-8") if binario else None

# -----------------------------
# HOME: Listar escuderías
# -----------------------------
@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    escuderias = db.query(Escuderia).filter(Escuderia.activo == True).all()

    for e in escuderias:
        e.logo = convertir_imagen(e.logo)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "escuderias": escuderias}
    )

# -----------------------------
# DETALLE: Escudería por nombre
# -----------------------------
@router.get("/team/{team_name}", response_class=HTMLResponse)
def team_detail(request: Request, team_name: str, db: Session = Depends(get_db)):
    escuderia = db.query(Escuderia).filter(Escuderia.nombre == team_name).first()
    if not escuderia:
        return templates.TemplateResponse(
            "team.html",
            {"request": request, "team": None, "pilotos": [], "error": "Escudería no encontrada"}
        )

    escuderia.logo = convertir_imagen(escuderia.logo)

    pilotos = db.query(Piloto).filter(Piloto.escuderia_id == escuderia.id).all()
    for p in pilotos:
        p.imagen = convertir_imagen(p.imagen)

    return templates.TemplateResponse(
        "team.html",
        {"request": request, "team": escuderia, "pilotos": pilotos}
    )

# -----------------------------
# DETALLE: Piloto por ID
# -----------------------------
@router.get("/pilotos/{piloto_id}", response_class=HTMLResponse)
def piloto_detail(request: Request, piloto_id: int, db: Session = Depends(get_db)):
    piloto = (
        db.query(Piloto)
        .options(joinedload(Piloto.escuderia))  # 🔹 fuerza la carga de la relación escudería
        .filter(Piloto.id == piloto_id)
        .first()
    )
    if not piloto:
        return templates.TemplateResponse(
            "piloto_detail.html",
            {"request": request, "error": "Piloto no encontrado"}
        )

    piloto.imagen = convertir_imagen(piloto.imagen)
    if piloto.escuderia:
        piloto.escuderia.logo = convertir_imagen(piloto.escuderia.logo)

    return templates.TemplateResponse(
        "piloto_detail.html",
        {"request": request, "piloto": piloto}
    )
