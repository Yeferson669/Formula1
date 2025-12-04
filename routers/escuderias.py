import base64
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Escuderia, Piloto

router = APIRouter(prefix="/escuderias", tags=["Escuderías"])
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def convertir_imagen(binario):
    return base64.b64encode(binario).decode("utf-8") if binario else None


@router.get("/buscar", response_class=HTMLResponse)
def buscar_escuderias(request: Request, nombre: str = "", db: Session = Depends(get_db)):
    if nombre:
        escuderias = db.query(Escuderia).filter(Escuderia.nombre.ilike(f"%{nombre}%"), Escuderia.activo == True).all()
    else:
        escuderias = db.query(Escuderia).filter(Escuderia.activo == True).all()

    for e in escuderias:
        e.logo = convertir_imagen(e.logo)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "escuderias": escuderias, "busqueda": nombre}
    )


@router.get("/", response_class=HTMLResponse)
def get_escuderias(request: Request, db: Session = Depends(get_db)):
    escuderias = db.query(Escuderia).filter(Escuderia.activo == True).all()

    for e in escuderias:
        e.logo = convertir_imagen(e.logo)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "escuderias": escuderias}
    )


@router.get("/{escuderia_id}", response_class=HTMLResponse)
def get_escuderia_by_id(request: Request, escuderia_id: int, db: Session = Depends(get_db)):
    esc = db.query(Escuderia).filter(Escuderia.id == escuderia_id, Escuderia.activo == True).first()
    if not esc:
        return templates.TemplateResponse(
            "team.html",
            {"request": request, "team": None, "pilotos": [], "error": "Escudería no encontrada"}
        )

    esc.logo = convertir_imagen(esc.logo)

    pilotos = db.query(Piloto).filter(Piloto.escuderia_id == esc.id).all()
    for p in pilotos:
        p.imagen = convertir_imagen(p.imagen)

    return templates.TemplateResponse(
        "team.html",
        {"request": request, "team": esc, "pilotos": pilotos}
    )


@router.post("/", response_class=HTMLResponse)
async def create_escuderia(
    request: Request,
    nombre: str = Form(...),
    pais: str = Form(...),
    logo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    existente = db.query(Escuderia).filter(Escuderia.nombre == nombre, Escuderia.activo == True).first()
    if existente:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": "Ya existe una escudería con ese nombre"}
        )

    logo_binario = None
    if logo:
        logo_binario = await logo.read()

    db_esc = Escuderia(
        nombre=nombre,
        pais=pais,
        logo=logo_binario,
        activo=True
    )
    db.add(db_esc)
    db.commit()
    db.refresh(db_esc)

    escuderias = db.query(Escuderia).filter(Escuderia.activo == True).all()
    for e in escuderias:
        e.logo = convertir_imagen(e.logo)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "escuderias": escuderias}
    )


@router.post("/editar/{escuderia_id}", response_class=HTMLResponse)
async def update_escuderia(
    request: Request,
    escuderia_id: int,
    nombre: str = Form(...),
    pais: str = Form(...),
    logo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_esc = db.query(Escuderia).filter(Escuderia.id == escuderia_id, Escuderia.activo == True).first()
    if not db_esc:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": "Escudería no encontrada"}
        )

    db_esc.nombre = nombre
    db_esc.pais = pais

    if logo:
        db_esc.logo = await logo.read()

    db.commit()
    db.refresh(db_esc)

    db_esc.logo = convertir_imagen(db_esc.logo)

    pilotos = db.query(Piloto).filter(Piloto.escuderia_id == db_esc.id).all()
    for p in pilotos:
        p.imagen = convertir_imagen(p.imagen)

    return templates.TemplateResponse(
        "team.html",
        {"request": request, "team": db_esc, "pilotos": pilotos}
    )


@router.get("/eliminar/{escuderia_id}", response_class=HTMLResponse)
def eliminar_escuderia(request: Request, escuderia_id: int, db: Session = Depends(get_db)):
    esc = db.query(Escuderia).filter(Escuderia.id == escuderia_id).first()
    if not esc:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": "Escudería no encontrada"}
        )
    esc.activo = False
    db.commit()

    escuderias = db.query(Escuderia).filter(Escuderia.activo == True).all()
    for e in escuderias:
        e.logo = convertir_imagen(e.logo)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "escuderias": escuderias, "mensaje": f"Escudería {esc.nombre} fue eliminada"}
    )


@router.get("/eliminados/", response_class=HTMLResponse)
def get_eliminadas(request: Request, db: Session = Depends(get_db)):
    escuderias = db.query(Escuderia).filter(Escuderia.activo == False).all()

    for e in escuderias:
        e.logo = convertir_imagen(e.logo)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "escuderias": escuderias}
    )
