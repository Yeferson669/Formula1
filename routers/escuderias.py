import base64
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
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
        escuderias = db.query(Escuderia).filter(
            Escuderia.nombre.ilike(f"%{nombre}%"), Escuderia.activo == True
        ).all()
    else:
        escuderias = db.query(Escuderia).filter(Escuderia.activo == True).all()

    for e in escuderias:
        e.logo = convertir_imagen(e.logo)

    eliminadas = db.query(Escuderia).filter(Escuderia.activo == False).all()
    for e in eliminadas:
        e.logo = convertir_imagen(e.logo)

    return templates.TemplateResponse(
        "escuderias.html",
        {
            "request": request,
            "escuderias": escuderias,
            "eliminadas": eliminadas,
            "busqueda": nombre
        }
    )


@router.get("/", response_class=HTMLResponse)
def listar_escuderias(request: Request, db: Session = Depends(get_db)):
    escuderias = db.query(Escuderia).filter(Escuderia.activo == True).all()
    for e in escuderias:
        e.logo = convertir_imagen(e.logo)

    eliminadas = db.query(Escuderia).filter(Escuderia.activo == False).all()
    for e in eliminadas:
        e.logo = convertir_imagen(e.logo)

    return templates.TemplateResponse(
        "escuderias.html",
        {
            "request": request,
            "escuderias": escuderias,
            "eliminadas": eliminadas
        }
    )


@router.get("/{escuderia_id}", response_class=HTMLResponse)
def detalle_escuderia(request: Request, escuderia_id: int, db: Session = Depends(get_db)):
    esc = db.query(Escuderia).filter(
        Escuderia.id == escuderia_id, Escuderia.activo == True
    ).first()
    if not esc:
        return templates.TemplateResponse(
            "escuderia.html",
            {"request": request, "escuderia": None, "pilotos": [], "error": "Escudería no encontrada"}
        )

    esc.logo = convertir_imagen(esc.logo)
    pilotos = db.query(Piloto).filter(Piloto.escuderia_id == esc.id).all()
    for p in pilotos:
        p.imagen = convertir_imagen(p.imagen)

    return templates.TemplateResponse(
        "escuderia.html",
        {"request": request, "escuderia": esc, "pilotos": pilotos}
    )


@router.post("/crear/", response_class=HTMLResponse)
async def crear_escuderia(
    nombre: str = Form(...),
    pais: str = Form(...),
    logo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    existente = db.query(Escuderia).filter(
        Escuderia.nombre == nombre, Escuderia.activo == True
    ).first()
    if existente:
        return RedirectResponse(url="/escuderias/", status_code=303)

    logo_binario = await logo.read() if logo else None

    nueva = Escuderia(nombre=nombre, pais=pais, logo=logo_binario, activo=True)
    db.add(nueva)
    db.commit()
    return RedirectResponse(url="/escuderias/", status_code=303)


@router.post("/editar/{escuderia_id}", response_class=HTMLResponse)
async def editar_escuderia(
    escuderia_id: int,
    nombre: str = Form(...),
    pais: str = Form(...),
    logo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    esc = db.query(Escuderia).filter(
        Escuderia.id == escuderia_id, Escuderia.activo == True
    ).first()
    if not esc:
        return RedirectResponse(url="/escuderias/", status_code=303)

    esc.nombre = nombre
    esc.pais = pais
    if logo:
        esc.logo = await logo.read()

    db.commit()
    return RedirectResponse(url=f"/escuderias/{escuderia_id}", status_code=303)


@router.get("/eliminar/{escuderia_id}", response_class=HTMLResponse)
def eliminar_escuderia(escuderia_id: int, db: Session = Depends(get_db)):
    esc = db.query(Escuderia).filter(Escuderia.id == escuderia_id).first()
    if esc:
        esc.activo = False
        db.commit()
    return RedirectResponse(url="/escuderias/", status_code=303)


# Restaurar escudería
@router.get("/restaurar/{escuderia_id}", response_class=HTMLResponse)
def restaurar_escuderia(escuderia_id: int, db: Session = Depends(get_db)):
    esc = db.query(Escuderia).filter(Escuderia.id == escuderia_id, Escuderia.activo == False).first()
    if esc:
        esc.activo = True
        db.commit()
    return RedirectResponse(url="/escuderias/", status_code=303)


@router.get("/eliminados/", response_class=HTMLResponse)
def listar_eliminadas(request: Request, db: Session = Depends(get_db)):
    eliminadas = db.query(Escuderia).filter(Escuderia.activo == False).all()
    for e in eliminadas:
        e.logo = convertir_imagen(e.logo)
    return templates.TemplateResponse(
        "escuderias.html",
        {"request": request, "escuderias": [], "eliminadas": eliminadas, "mensaje": "Listado de escuderías eliminadas"}
    )
