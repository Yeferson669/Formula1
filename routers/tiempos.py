import base64
import datetime
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from models import Tiempo, Piloto, Circuito

router = APIRouter(prefix="/tiempos", tags=["Tiempos"])
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def convertir_relaciones(tiempos):
    for t in tiempos:
        if t.piloto and t.piloto.imagen and isinstance(t.piloto.imagen, bytes):
            t.piloto.imagen = base64.b64encode(t.piloto.imagen).decode("utf-8")
        if t.circuito and t.circuito.imagen and isinstance(t.circuito.imagen, bytes):
            t.circuito.imagen = base64.b64encode(t.circuito.imagen).decode("utf-8")
    return tiempos


# Listado de tiempos + formulario
@router.get("/", response_class=HTMLResponse)
def listar_tiempos(request: Request, db: Session = Depends(get_db)):
    tiempos = (
        db.query(Tiempo)
        .options(joinedload(Tiempo.piloto), joinedload(Tiempo.circuito))
        .filter(Tiempo.activo == True)
        .all()
    )
    tiempos = convertir_relaciones(tiempos)
    pilotos = db.query(Piloto).filter(Piloto.activo == True).all()
    circuitos = db.query(Circuito).filter(Circuito.activo == True).all()
    return templates.TemplateResponse(
        "tiempos_list.html",   # 👈 listado + formulario
        {"request": request, "tiempos": tiempos, "pilotos": pilotos, "circuitos": circuitos}
    )


# Detalle de un tiempo
@router.get("/{tiempo_id}", response_class=HTMLResponse)
def detalle_tiempo(request: Request, tiempo_id: int, db: Session = Depends(get_db)):
    tiempo = (
        db.query(Tiempo)
        .options(joinedload(Tiempo.piloto), joinedload(Tiempo.circuito))
        .filter(Tiempo.id == tiempo_id, Tiempo.activo == True)
        .first()
    )
    if not tiempo:
        return templates.TemplateResponse("tiempo_detail.html", {"request": request, "error": "Tiempo no encontrado"})

    convertir_relaciones([tiempo])
    return templates.TemplateResponse("tiempo_detail.html", {"request": request, "tiempo": tiempo})


# Crear tiempo
@router.post("/crear/", response_class=HTMLResponse)
async def crear_tiempo(
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
        return templates.TemplateResponse("error.html", {"request": {}, "error": "Piloto no existe o está inactivo"})
    if not circuito:
        return templates.TemplateResponse("error.html", {"request": {}, "error": "Circuito no existe o está inactivo"})

    if tiempo_vuelta <= 0:
        return templates.TemplateResponse("error.html", {"request": {}, "error": "El tiempo de vuelta debe ser mayor a 0"})
    if posicion is not None and posicion < 1:
        return templates.TemplateResponse("error.html", {"request": {}, "error": "La posición debe ser mayor o igual a 1"})

    fecha_obj = None
    if fecha:
        try:
            fecha_obj = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            return templates.TemplateResponse("error.html", {"request": {}, "error": "Formato de fecha inválido (usar YYYY-MM-DD)"})

        existente = db.query(Tiempo).filter(
            Tiempo.piloto_id == piloto_id,
            Tiempo.circuito_id == circuito_id,
            Tiempo.fecha == fecha_obj,
            Tiempo.activo == True
        ).first()
        if existente:
            return templates.TemplateResponse("error.html", {"request": {}, "error": "Ya existe un tiempo registrado para este piloto en este circuito en esa fecha"})

    nuevo = Tiempo(
        piloto_id=piloto_id,
        circuito_id=circuito_id,
        tiempo_vuelta=tiempo_vuelta,
        posicion=posicion,
        fecha=fecha_obj,
        activo=True
    )
    db.add(nuevo)
    db.commit()
    return RedirectResponse(url="/tiempos/", status_code=303)


# Editar tiempo
@router.post("/editar/{tiempo_id}", response_class=HTMLResponse)
def editar_tiempo(
    tiempo_id: int,
    tiempo_vuelta: float = Form(...),
    posicion: int = Form(None),
    fecha: str = Form(None),
    db: Session = Depends(get_db)
):
    tiempo = db.query(Tiempo).filter(Tiempo.id == tiempo_id, Tiempo.activo == True).first()
    if not tiempo:
        return templates.TemplateResponse("error.html", {"request": {}, "error": "Tiempo no encontrado"})

    tiempo.tiempo_vuelta = tiempo_vuelta
    tiempo.posicion = posicion

    if fecha:
        try:
            tiempo.fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            return templates.TemplateResponse("error.html", {"request": {}, "error": "Formato de fecha inválido (usar YYYY-MM-DD)"})
    else:
        tiempo.fecha = None

    db.commit()
    return RedirectResponse(url=f"/tiempos/{tiempo_id}", status_code=303)


# Eliminar tiempo
@router.get("/eliminar/{tiempo_id}", response_class=HTMLResponse)
def eliminar_tiempo(tiempo_id: int, db: Session = Depends(get_db)):
    tiempo = db.query(Tiempo).filter(Tiempo.id == tiempo_id).first()
    if tiempo:
        tiempo.activo = False
        db.commit()
    return RedirectResponse(url="/tiempos/", status_code=303)


# Listar tiempos eliminados
@router.get("/eliminados/", response_class=HTMLResponse)
def tiempos_eliminados(request: Request, db: Session = Depends(get_db)):
    tiempos = (
        db.query(Tiempo)
        .options(joinedload(Tiempo.piloto), joinedload(Tiempo.circuito))
        .filter(Tiempo.activo == False)
        .all()
    )
    tiempos = convertir_relaciones(tiempos)
    pilotos = db.query(Piloto).filter(Piloto.activo == True).all()
    circuitos = db.query(Circuito).filter(Circuito.activo == True).all()
    return templates.TemplateResponse(
        "tiempos_list.html",   # 👈 listado + formulario
        {"request": request, "tiempos": tiempos, "pilotos": pilotos, "circuitos": circuitos, "mensaje": "Listado de tiempos eliminados"}
    )
