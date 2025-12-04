import base64
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from models import Piloto, Escuderia

router = APIRouter(prefix="/pilotos", tags=["Pilotos"])
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def convertir_imagen(binario):
    return base64.b64encode(binario).decode("utf-8") if binario else None


# Listado de pilotos + formulario + eliminados
@router.get("/", response_class=HTMLResponse)
def listar_pilotos(request: Request, db: Session = Depends(get_db)):
    pilotos = db.query(Piloto).filter(Piloto.activo == True).all()
    for p in pilotos:
        p.imagen = convertir_imagen(p.imagen)

    eliminados = db.query(Piloto).filter(Piloto.activo == False).all()
    for e in eliminados:
        e.imagen = convertir_imagen(e.imagen)

    escuderias = db.query(Escuderia).filter(Escuderia.activo == True).all()
    return templates.TemplateResponse(
        "piloto.html",
        {
            "request": request,
            "pilotos": pilotos,
            "eliminados": eliminados,   # 👈 ahora también pasamos los eliminados
            "escuderias": escuderias
        }
    )


# Detalle de piloto
@router.get("/{piloto_id}", response_class=HTMLResponse)
def detalle_piloto(request: Request, piloto_id: int, db: Session = Depends(get_db)):
    piloto = (
        db.query(Piloto)
        .options(joinedload(Piloto.escuderia))
        .filter(Piloto.id == piloto_id, Piloto.activo == True)
        .first()
    )
    if not piloto:
        return templates.TemplateResponse(
            "piloto_detail.html",
            {"request": request, "piloto": None, "error": "Piloto no encontrado"}
        )

    piloto.imagen = convertir_imagen(piloto.imagen)
    if piloto.escuderia:
        piloto.escuderia.logo = convertir_imagen(piloto.escuderia.logo)

    return templates.TemplateResponse("piloto_detail.html", {"request": request, "piloto": piloto})


# Buscar pilotos
@router.get("/buscar/", response_class=HTMLResponse)
def buscar_pilotos(request: Request, nombre: str = None, db: Session = Depends(get_db)):
    if not nombre:
        resultados = db.query(Piloto).filter(Piloto.activo == True).all()
    else:
        resultados = db.query(Piloto).filter(Piloto.nombre.ilike(f"%{nombre}%"), Piloto.activo == True).all()

    for p in resultados:
        p.imagen = convertir_imagen(p.imagen)

    escuderias = db.query(Escuderia).filter(Escuderia.activo == True).all()
    eliminados = db.query(Piloto).filter(Piloto.activo == False).all()
    for e in eliminados:
        e.imagen = convertir_imagen(e.imagen)

    return templates.TemplateResponse(
        "piloto.html",
        {
            "request": request,
            "pilotos": resultados,
            "eliminados": eliminados,
            "escuderias": escuderias,
            "busqueda": nombre
        }
    )


# Crear piloto
@router.post("/crear/", response_class=HTMLResponse)
async def crear_piloto(
    nombre: str = Form(...),
    numero: int = Form(...),
    nacionalidad: str = Form(...),
    escuderia_id: int = Form(...),
    fecha_nacimiento: str = Form(None),
    biografia: str = Form(None),
    twitter: str = Form(None),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    esc = db.query(Escuderia).filter(Escuderia.id == escuderia_id, Escuderia.activo == True).first()
    if not esc:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Escudería no existe o está inactiva"})

    count_pilotos = db.query(Piloto).filter(Piloto.escuderia_id == escuderia_id, Piloto.activo == True).count()
    if count_pilotos >= 2:
        return templates.TemplateResponse("error.html", {"request": request, "error": "La escudería ya tiene el máximo de 2 pilotos activos"})

    existente = db.query(Piloto).filter(Piloto.numero == numero, Piloto.activo == True).first()
    if existente:
        return templates.TemplateResponse("error.html", {"request": request, "error": "El número de piloto ya está en uso"})

    imagen_binaria = await imagen.read() if imagen else None

    nuevo = Piloto(
        nombre=nombre,
        numero=numero,
        nacionalidad=nacionalidad,
        escuderia_id=escuderia_id,
        fecha_nacimiento=fecha_nacimiento,
        biografia=biografia,
        twitter=twitter,
        imagen=imagen_binaria,
        activo=True
    )
    db.add(nuevo)
    db.commit()
    return RedirectResponse(url="/pilotos/", status_code=303)


# Editar piloto
@router.post("/editar/{piloto_id}", response_class=HTMLResponse)
async def editar_piloto(
    piloto_id: int,
    nombre: str = Form(...),
    nacionalidad: str = Form(...),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    piloto = db.query(Piloto).filter(Piloto.id == piloto_id, Piloto.activo == True).first()
    if not piloto:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Piloto no encontrado"})

    piloto.nombre = nombre
    piloto.nacionalidad = nacionalidad
    if imagen:
        piloto.imagen = await imagen.read()

    db.commit()
    return RedirectResponse(url=f"/pilotos/{piloto_id}", status_code=303)


# Eliminar piloto
@router.get("/eliminar/{piloto_id}", response_class=HTMLResponse)
def eliminar_piloto(piloto_id: int, db: Session = Depends(get_db)):
    piloto = db.query(Piloto).filter(Piloto.id == piloto_id).first()
    if piloto:
        piloto.activo = False
        db.commit()
    return RedirectResponse(url="/pilotos/", status_code=303)


# Restaurar piloto
@router.get("/restaurar/{piloto_id}", response_class=HTMLResponse)
def restaurar_piloto(piloto_id: int, db: Session = Depends(get_db)):
    piloto = db.query(Piloto).filter(Piloto.id == piloto_id, Piloto.activo == False).first()
    if piloto:
        piloto.activo = True
        db.commit()
    return RedirectResponse(url="/pilotos/", status_code=303)


# Listar pilotos eliminados (opcional, ya que ahora se muestran en el mismo template)
@router.get("/eliminados/", response_class=HTMLResponse)
def listar_eliminados(request: Request, db: Session = Depends(get_db)):
    eliminados = db.query(Piloto).filter(Piloto.activo == False).all()
    for e in eliminados:
        e.imagen = convertir_imagen(e.imagen)
    escuderias = db.query(Escuderia).filter(Escuderia.activo == True).all()
    return templates.TemplateResponse(
        "piloto.html",
        {"request": request, "pilotos": [], "eliminados": eliminados, "escuderias": escuderias, "mensaje": "Listado de pilotos eliminados"}
    )
