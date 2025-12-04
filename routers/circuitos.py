import base64
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
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


# Listado de circuitos + formulario
@router.get("/", response_class=HTMLResponse)
def listar_circuitos(request: Request, db: Session = Depends(get_db)):
    circuitos = db.query(Circuito).filter(Circuito.activo == True).all()
    for c in circuitos:
        c.imagen = convertir_imagen(c.imagen)
    return templates.TemplateResponse(
        "circuitos.html",   # 👈 listado + formulario
        {"request": request, "circuitos": circuitos}
    )


# Detalle de circuito
@router.get("/{circuito_id}", response_class=HTMLResponse)
def detalle_circuito(request: Request, circuito_id: int, db: Session = Depends(get_db)):
    circuito = db.query(Circuito).filter(Circuito.id == circuito_id, Circuito.activo == True).first()
    if not circuito:
        return templates.TemplateResponse(
            "circuito_detail.html",
            {"request": request, "circuito": None, "error": "Circuito no encontrado"}
        )
    circuito.imagen = convertir_imagen(circuito.imagen)
    return templates.TemplateResponse(
        "circuito_detail.html",
        {"request": request, "circuito": circuito}
    )


# Crear circuito
@router.post("/crear/", response_class=HTMLResponse)
async def crear_circuito(
    nombre: str = Form(...),
    pais: str = Form(...),
    longitud_km: float = Form(None),
    descripcion: str = Form(None),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    existente = db.query(Circuito).filter(Circuito.nombre == nombre, Circuito.activo == True).first()
    if existente:
        return templates.TemplateResponse("error.html", {"request": {}, "error": "Ya existe un circuito con ese nombre"})

    imagen_binaria = await imagen.read() if imagen else None

    nuevo = Circuito(
        nombre=nombre,
        pais=pais,
        longitud_km=longitud_km,
        descripcion=descripcion,
        imagen=imagen_binaria,
        activo=True
    )
    db.add(nuevo)
    db.commit()
    return RedirectResponse(url="/circuitos/", status_code=303)


# Editar circuito
@router.post("/editar/{circuito_id}", response_class=HTMLResponse)
async def editar_circuito(
    circuito_id: int,
    nombre: str = Form(...),
    pais: str = Form(...),
    longitud_km: float = Form(None),
    descripcion: str = Form(None),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    circuito = db.query(Circuito).filter(Circuito.id == circuito_id, Circuito.activo == True).first()
    if not circuito:
        return templates.TemplateResponse("error.html", {"request": {}, "error": "Circuito no encontrado"})

    circuito.nombre = nombre
    circuito.pais = pais
    circuito.longitud_km = longitud_km
    circuito.descripcion = descripcion
    if imagen:
        circuito.imagen = await imagen.read()

    db.commit()
    return RedirectResponse(url=f"/circuitos/{circuito_id}", status_code=303)


# Eliminar circuito
@router.get("/eliminar/{circuito_id}", response_class=HTMLResponse)
def eliminar_circuito(circuito_id: int, db: Session = Depends(get_db)):
    circuito = db.query(Circuito).filter(Circuito.id == circuito_id).first()
    if circuito:
        circuito.activo = False
        db.commit()
    return RedirectResponse(url="/circuitos/", status_code=303)


# Listar circuitos eliminados
@router.get("/eliminados/", response_class=HTMLResponse)
def listar_eliminados(request: Request, db: Session = Depends(get_db)):
    circuitos = db.query(Circuito).filter(Circuito.activo == False).all()
    for c in circuitos:
        c.imagen = convertir_imagen(c.imagen)
    return templates.TemplateResponse(
        "circuitos.html",   # 👈 listado + formulario
        {"request": request, "circuitos": circuitos, "mensaje": "Listado de circuitos eliminados"}
    )
