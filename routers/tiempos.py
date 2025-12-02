from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from models import Tiempo, Piloto, Circuito
import datetime

router = APIRouter(prefix="/tiempos", tags=["Tiempos"])
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
# READ: Listar todos los tiempos activos
# -----------------------------
@router.get("/", response_class=HTMLResponse)
def get_tiempos(request: Request, db: Session = Depends(get_db)):
    tiempos = (
        db.query(Tiempo)
        .options(joinedload(Tiempo.piloto), joinedload(Tiempo.circuito))
        .filter(Tiempo.activo == True)
        .all()
    )
    return templates.TemplateResponse(
        "tiempos_list.html",
        {"request": request, "tiempos": tiempos}
    )

# -----------------------------
# READ: Detalle de tiempo por ID
# -----------------------------
@router.get("/{tiempo_id}", response_class=HTMLResponse)
def get_tiempo_by_id(request: Request, tiempo_id: int, db: Session = Depends(get_db)):
    tiempo = (
        db.query(Tiempo)
        .options(joinedload(Tiempo.piloto), joinedload(Tiempo.circuito))
        .filter(Tiempo.id == tiempo_id, Tiempo.activo == True)
        .first()
    )
    if not tiempo:
        return templates.TemplateResponse(
            "tiempo_detail.html",
            {"request": request, "error": "Tiempo no encontrado"}
        )
    return templates.TemplateResponse(
        "tiempo_detail.html",
        {"request": request, "tiempo": tiempo}
    )

# -----------------------------
# CREATE: Crear tiempo (formulario)
# -----------------------------
@router.post("/", response_class=HTMLResponse)
async def create_tiempo(
    request: Request,
    piloto_id: int = Form(...),
    circuito_id: int = Form(...),
    tiempo_vuelta: float = Form(...),
    posicion: int = Form(None),
    fecha: str = Form(None),
    db: Session = Depends(get_db)
):
    piloto = db.query(Piloto).filter(Piloto.id == piloto_id, Piloto.activo == True).first()
    circuito = db.query(Circuito).filter(Circuito.id == circuito_id, Circuito.activo == True).first()
    if not piloto:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Piloto no existe o está inactivo"})
    if not circuito:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Circuito no existe o está inactivo"})

    if tiempo_vuelta <= 0:
        return templates.TemplateResponse("error.html", {"request": request, "error": "El tiempo de vuelta debe ser mayor a 0"})
    if posicion is not None and posicion < 1:
        return templates.TemplateResponse("error.html", {"request": request, "error": "La posición debe ser mayor o igual a 1"})

    if fecha:
        existente = db.query(Tiempo).filter(
            Tiempo.piloto_id == piloto_id,
            Tiempo.circuito_id == circuito_id,
            Tiempo.fecha == fecha,
            Tiempo.activo == True
        ).first()
        if existente:
            return templates.TemplateResponse("error.html", {"request": request, "error": "Ya existe un tiempo registrado para este piloto en este circuito en esa fecha"})

    db_tiempo = Tiempo(
        piloto_id=piloto_id,
        circuito_id=circuito_id,
        tiempo_vuelta=tiempo_vuelta,
        posicion=posicion,
        fecha=fecha,
        activo=True
    )
    db.add(db_tiempo)
    db.commit()
    db.refresh(db_tiempo)

    tiempos = db.query(Tiempo).filter(Tiempo.activo == True).all()
    return templates.TemplateResponse(
        "tiempos_list.html",
        {"request": request, "tiempos": tiempos, "mensaje": "Tiempo registrado correctamente"}
    )

# -----------------------------
# UPDATE: Editar tiempo
# -----------------------------
@router.post("/editar/{tiempo_id}", response_class=HTMLResponse)
def update_tiempo(request: Request, tiempo_id: int, tiempo_vuelta: float = Form(...), posicion: int = Form(None), fecha: str = Form(None), db: Session = Depends(get_db)):
    db_tiempo = db.query(Tiempo).filter(Tiempo.id == tiempo_id, Tiempo.activo == True).first()
    if not db_tiempo:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Tiempo no encontrado"})

    db_tiempo.tiempo_vuelta = tiempo_vuelta
    db_tiempo.posicion = posicion
    db_tiempo.fecha = fecha
    db.commit()
    db.refresh(db_tiempo)

    return templates.TemplateResponse("tiempo_detail.html", {"request": request, "tiempo": db_tiempo})

# -----------------------------
# DELETE: Marcar tiempo como inactivo
# -----------------------------
@router.get("/eliminar/{tiempo_id}", response_class=HTMLResponse)
def eliminar_tiempo(request: Request, tiempo_id: int, db: Session = Depends(get_db)):
    tiempo = db.query(Tiempo).filter(Tiempo.id == tiempo_id).first()
    if not tiempo:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Tiempo no encontrado"})
    tiempo.activo = False
    db.commit()

    tiempos = db.query(Tiempo).filter(Tiempo.activo == True).all()
    return templates.TemplateResponse(
        "tiempos_list.html",
        {"request": request, "tiempos": tiempos, "mensaje": f"Tiempo con ID {tiempo_id} eliminado"}
    )

# -----------------------------
# READ: Listar tiempos eliminados
# -----------------------------
@router.get("/eliminados/", response_class=HTMLResponse)
def get_tiempos_eliminados(request: Request, db: Session = Depends(get_db)):
    tiempos = db.query(Tiempo).filter(Tiempo.activo == False).all()
    return templates.TemplateResponse(
        "tiempos_list.html",
        {"request": request, "tiempos": tiempos}
    )