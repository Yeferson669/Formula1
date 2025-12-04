import base64
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Circuito

router = APIRouter(prefix="/circuitos", tags=["Circuitos"])
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def convertir_imagen(binario):
    return base64.b64encode(binario).decode("utf-8") if binario else None


@router.get("/", response_class=HTMLResponse)
def get_circuitos(request: Request, db: Session = Depends(get_db)):
    circuitos = db.query(Circuito).filter(Circuito.activo == True).all()

    for c in circuitos:
        c.imagen = convertir_imagen(c.imagen)

    return templates.TemplateResponse(
        "circuitos_list.html",
        {"request": request, "circuitos": circuitos}
    )


@router.get("/{circuito_id}", response_class=HTMLResponse)
def get_circuito_by_id(request: Request, circuito_id: int, db: Session = Depends(get_db)):
    circuito = db.query(Circuito).filter(Circuito.id == circuito_id, Circuito.activo == True).first()
    if not circuito:
        return templates.TemplateResponse(
            "circuito_detail.html",
            {"request": request, "error": "Circuito no encontrado"}
        )

    circuito.imagen = convertir_imagen(circuito.imagen)

    return templates.TemplateResponse(
        "circuito_detail.html",
        {"request": request, "circuito": circuito}
    )


@router.post("/", response_class=HTMLResponse)
async def create_circuito(
    request: Request,
    nombre: str = Form(...),
    pais: str = Form(...),
    longitud_km: float = Form(None),
    descripcion: str = Form(None),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    existente = db.query(Circuito).filter(Circuito.nombre == nombre, Circuito.activo == True).first()
    if existente:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Ya existe un circuito con ese nombre"})

    imagen_binaria = None
    if imagen:
        imagen_binaria = await imagen.read()

    db_circuito = Circuito(
        nombre=nombre,
        pais=pais,
        longitud_km=longitud_km,
        descripcion=descripcion,
        imagen=imagen_binaria,
        activo=True
    )
    db.add(db_circuito)
    db.commit()
    db.refresh(db_circuito)

    circuitos = db.query(Circuito).filter(Circuito.activo == True).all()
    for c in circuitos:
        c.imagen = convertir_imagen(c.imagen)

    return templates.TemplateResponse(
        "circuitos_list.html",
        {"request": request, "circuitos": circuitos, "mensaje": f"Circuito {db_circuito.nombre} creado exitosamente"}
    )


@router.post("/editar/{circuito_id}", response_class=HTMLResponse)
async def update_circuito(
    request: Request,
    circuito_id: int,
    nombre: str = Form(...),
    pais: str = Form(...),
    longitud_km: float = Form(None),
    descripcion: str = Form(None),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_circuito = db.query(Circuito).filter(Circuito.id == circuito_id, Circuito.activo == True).first()
    if not db_circuito:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Circuito no encontrado"})

    db_circuito.nombre = nombre
    db_circuito.pais = pais
    db_circuito.longitud_km = longitud_km
    db_circuito.descripcion = descripcion

    if imagen:
        db_circuito.imagen = await imagen.read()

    db.commit()
    db.refresh(db_circuito)

    db_circuito.imagen = convertir_imagen(db_circuito.imagen)

    return templates.TemplateResponse("circuito_detail.html", {"request": request, "circuito": db_circuito})
