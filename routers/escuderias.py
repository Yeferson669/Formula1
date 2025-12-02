from fastapi import APIRouter, Request, Depends, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Escuderia, Piloto
import shutil, os

router = APIRouter(prefix="/escuderias", tags=["Escuderías"])
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
# READ: Buscar escuderías por nombre (debe ir antes de /{id})
# -----------------------------
@router.get("/buscar", response_class=HTMLResponse)
def buscar_escuderias(request: Request, nombre: str = "", db: Session = Depends(get_db)):
    if nombre:
        escuderias = db.query(Escuderia).filter(Escuderia.nombre.ilike(f"%{nombre}%"), Escuderia.activo == True).all()
    else:
        escuderias = db.query(Escuderia).filter(Escuderia.activo == True).all()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "escuderias": escuderias, "busqueda": nombre}
    )

# -----------------------------
# READ: Listar todas las escuderías activas
# -----------------------------
@router.get("/", response_class=HTMLResponse)
def get_escuderias(request: Request, db: Session = Depends(get_db)):
    escuderias = db.query(Escuderia).filter(Escuderia.activo == True).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "escuderias": escuderias}
    )

# -----------------------------
# READ: Detalle de escudería por ID
# -----------------------------
@router.get("/{escuderia_id}", response_class=HTMLResponse)
def get_escuderia_by_id(request: Request, escuderia_id: int, db: Session = Depends(get_db)):
    esc = db.query(Escuderia).filter(Escuderia.id == escuderia_id, Escuderia.activo == True).first()
    if not esc:
        return templates.TemplateResponse(
            "team.html",
            {"request": request, "team": None, "pilotos": [], "error": "Escudería no encontrada"}
        )
    pilotos = db.query(Piloto).filter(Piloto.escuderia_id == esc.id).all()
    return templates.TemplateResponse(
        "team.html",
        {"request": request, "team": esc, "pilotos": pilotos}
    )

# -----------------------------
# CREATE: Crear escudería (formulario con logo)
# -----------------------------
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

    logo_url = None
    if logo:
        upload_dir = "static/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_location = os.path.join(upload_dir, logo.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(logo.file, buffer)
        logo_url = file_location

    db_esc = Escuderia(
        nombre=nombre,
        pais=pais,
        logo_url=logo_url,
        activo=True
    )
    db.add(db_esc)
    db.commit()
    db.refresh(db_esc)

    escuderias = db.query(Escuderia).filter(Escuderia.activo == True).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "escuderias": escuderias}
    )

# -----------------------------
# UPDATE: Editar escudería
# -----------------------------
@router.post("/editar/{escuderia_id}", response_class=HTMLResponse)
def update_escuderia(request: Request, escuderia_id: int, nombre: str = Form(...), pais: str = Form(...), db: Session = Depends(get_db)):
    db_esc = db.query(Escuderia).filter(Escuderia.id == escuderia_id, Escuderia.activo == True).first()
    if not db_esc:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": "Escudería no encontrada"}
        )

    db_esc.nombre = nombre
    db_esc.pais = pais
    db.commit()
    db.refresh(db_esc)

    pilotos = db.query(Piloto).filter(Piloto.escuderia_id == db_esc.id).all()
    return templates.TemplateResponse(
        "team.html",
        {"request": request, "team": db_esc, "pilotos": pilotos}
    )

# -----------------------------
# DELETE: Marcar escudería como inactiva
# -----------------------------
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
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "escuderias": escuderias, "mensaje": f"Escudería {esc.nombre} fue eliminada"}
    )

# -----------------------------
# READ: Listar escuderías eliminadas
# -----------------------------
@router.get("/eliminados/", response_class=HTMLResponse)
def get_eliminadas(request: Request, db: Session = Depends(get_db)):
    escuderias = db.query(Escuderia).filter(Escuderia.activo == False).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "escuderias": escuderias}
    )