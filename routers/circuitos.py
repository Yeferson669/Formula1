from fastapi import APIRouter, Request, Depends, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Circuito
import shutil, os

router = APIRouter(prefix="/circuitos", tags=["Circuitos"])
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
# READ: Listar todos los circuitos activos
# -----------------------------
@router.get("/", response_class=HTMLResponse)
def get_circuitos(request: Request, db: Session = Depends(get_db)):
    circuitos = db.query(Circuito).filter(Circuito.activo == True).all()
    return templates.TemplateResponse(
        "circuitos_list.html",
        {"request": request, "circuitos": circuitos}
    )

# -----------------------------
# READ: Detalle de circuito por ID
# -----------------------------
@router.get("/{circuito_id}", response_class=HTMLResponse)
def get_circuito_by_id(request: Request, circuito_id: int, db: Session = Depends(get_db)):
    circuito = db.query(Circuito).filter(Circuito.id == circuito_id, Circuito.activo == True).first()
    if not circuito:
        return templates.TemplateResponse(
            "circuito_detail.html",
            {"request": request, "error": "Circuito no encontrado"}
        )
    return templates.TemplateResponse(
        "circuito_detail.html",
        {"request": request, "circuito": circuito}
    )

# -----------------------------
# READ: Buscar circuitos por nombre
# -----------------------------
@router.get("/buscar/", response_class=HTMLResponse)
def buscar_circuitos(request: Request, nombre: str | None = None, db: Session = Depends(get_db)):
    if not nombre:
        resultados = db.query(Circuito).filter(Circuito.activo == True).all()
    else:
        resultados = db.query(Circuito).filter(Circuito.nombre.ilike(f"%{nombre}%"), Circuito.activo == True).all()
    return templates.TemplateResponse(
        "circuitos_list.html",
        {"request": request, "circuitos": resultados, "busqueda": nombre}
    )

# -----------------------------
# CREATE: Crear circuito (formulario con imagen)
# -----------------------------
@router.post("/", response_class=HTMLResponse)
async def create_circuito(
    request: Request,
    nombre: str = Form(...),
    pais: str = Form(...),
    longitud_km: float = Form(None),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    existente = db.query(Circuito).filter(Circuito.nombre == nombre, Circuito.activo == True).first()
    if existente:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Ya existe un circuito con ese nombre"})

    imagen_url = None
    if imagen:
        upload_dir = "static/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_location = os.path.join(upload_dir, imagen.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(imagen.file, buffer)
        imagen_url = file_location

    db_circuito = Circuito(
        nombre=nombre,
        pais=pais,
        longitud_km=longitud_km,
        imagen_url=imagen_url,
        activo=True
    )
    db.add(db_circuito)
    db.commit()
    db.refresh(db_circuito)

    circuitos = db.query(Circuito).filter(Circuito.activo == True).all()
    return templates.TemplateResponse(
        "circuitos_list.html",
        {"request": request, "circuitos": circuitos, "mensaje": f"Circuito {db_circuito.nombre} creado exitosamente"}
    )

# -----------------------------
# UPDATE: Editar circuito
# -----------------------------
@router.post("/editar/{circuito_id}", response_class=HTMLResponse)
def update_circuito(request: Request, circuito_id: int, nombre: str = Form(...), pais: str = Form(...), longitud_km: float = Form(None), db: Session = Depends(get_db)):
    db_circuito = db.query(Circuito).filter(Circuito.id == circuito_id, Circuito.activo == True).first()
    if not db_circuito:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Circuito no encontrado"})

    db_circuito.nombre = nombre
    db_circuito.pais = pais
    db_circuito.longitud_km = longitud_km
    db.commit()
    db.refresh(db_circuito)

    return templates.TemplateResponse("circuito_detail.html", {"request": request, "circuito": db_circuito})

# -----------------------------
# DELETE: Marcar circuito como inactivo
# -----------------------------
@router.get("/eliminar/{circuito_id}", response_class=HTMLResponse)
def eliminar_circuito(request: Request, circuito_id: int, db: Session = Depends(get_db)):
    circuito = db.query(Circuito).filter(Circuito.id == circuito_id).first()
    if not circuito:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Circuito no encontrado"})
    circuito.activo = False
    db.commit()

    circuitos = db.query(Circuito).filter(Circuito.activo == True).all()
    return templates.TemplateResponse(
        "circuitos_list.html",
        {"request": request, "circuitos": circuitos, "mensaje": f"Circuito {circuito.nombre} fue eliminado"}
    )

# -----------------------------
# READ: Listar circuitos eliminados
# -----------------------------
@router.get("/eliminados/", response_class=HTMLResponse)
def get_eliminados(request: Request, db: Session = Depends(get_db)):
    circuitos = db.query(Circuito).filter(Circuito.activo == False).all()
    return templates.TemplateResponse(
        "circuitos_list.html",
        {"request": request, "circuitos": circuitos}
    )