import base64
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse
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


@router.get("/", response_class=HTMLResponse)
def get_pilotos(request: Request, db: Session = Depends(get_db)):
    pilotos = db.query(Piloto).filter(Piloto.activo == True).all()

    for p in pilotos:
        p.imagen = convertir_imagen(p.imagen)

    return templates.TemplateResponse(
        "pilotos_list.html",
        {"request": request, "pilotos": pilotos}
    )


@router.get("/{piloto_id}", response_class=HTMLResponse)
def get_piloto_by_id(request: Request, piloto_id: int, db: Session = Depends(get_db)):
    piloto = (
        db.query(Piloto)
        .options(joinedload(Piloto.escuderia))
        .filter(Piloto.id == piloto_id, Piloto.activo == True)
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


@router.get("/buscar/", response_class=HTMLResponse)
def buscar_pilotos(request: Request, nombre: str = None, db: Session = Depends(get_db)):
    if not nombre:
        resultados = db.query(Piloto).filter(Piloto.activo == True).all()
    else:
        resultados = db.query(Piloto).filter(Piloto.nombre.ilike(f"%{nombre}%"), Piloto.activo == True).all()

    for p in resultados:
        p.imagen = convertir_imagen(p.imagen)

    return templates.TemplateResponse(
        "pilotos_list.html",
        {"request": request, "pilotos": resultados, "busqueda": nombre}
    )


@router.post("/", response_class=HTMLResponse)
async def create_piloto(
    request: Request,
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

    piloto_existente = db.query(Piloto).filter(Piloto.nombre == nombre, Piloto.activo == True).first()
    if piloto_existente and piloto_existente.escuderia_id != escuderia_id:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Este piloto ya pertenece a otra escudería activa"})

    existente = db.query(Piloto).filter(Piloto.numero == numero, Piloto.activo == True).first()
    if existente:
        return templates.TemplateResponse("error.html", {"request": request, "error": "El número de piloto ya está en uso"})

    imagen_binaria = None
    if imagen:
        imagen_binaria = await imagen.read()

    db_piloto = Piloto(
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
    db.add(db_piloto)
    db.commit()
    db.refresh(db_piloto)

    pilotos = db.query(Piloto).filter(Piloto.activo == True).all()
    for p in pilotos:
        p.imagen = convertir_imagen(p.imagen)

    return templates.TemplateResponse(
        "pilotos_list.html",
        {"request": request, "pilotos": pilotos, "mensaje": f"Piloto {db_piloto.nombre} creado exitosamente"}
    )


@router.post("/editar/{piloto_id}", response_class=HTMLResponse)
async def update_piloto(
    request: Request,
    piloto_id: int,
    nombre: str = Form(...),
    nacionalidad: str = Form(...),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_piloto = db.query(Piloto).filter(Piloto.id == piloto_id, Piloto.activo == True).first()
    if not db_piloto:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Piloto no encontrado"})

    db_piloto.nombre = nombre
    db_piloto.nacionalidad = nacionalidad

    if imagen:
        db_piloto.imagen = await imagen.read()

    db.commit()
    db.refresh(db_piloto)

    db_piloto.imagen = convertir_imagen(db_piloto.imagen)

    return templates.TemplateResponse("piloto_detail.html", {"request": request, "piloto": db_piloto})


@router.get("/eliminar/{piloto_id}", response_class=HTMLResponse)
def eliminar_piloto(request: Request, piloto_id: int, db: Session = Depends(get_db)):
    piloto = db.query(Piloto).filter(Piloto.id == piloto_id).first()
    if not piloto:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Piloto no encontrado"})
    piloto.activo = False
    db.commit()

    pilotos = db.query(Piloto).filter(Piloto.activo == True).all()
    for p in pilotos:
        p.imagen = convertir_imagen(p.imagen)

    return templates.TemplateResponse(
        "pilotos_list.html",
        {"request": request, "pilotos": pilotos, "mensaje": f"Piloto {piloto.nombre} fue eliminado"}
    )


@router.get("/eliminados/", response_class=HTMLResponse)
def get_pilotos_eliminados(request: Request, db: Session = Depends(get_db)):
    pilotos = db.query(Piloto).filter(Piloto.activo == False).all()

    for p in pilotos:
        p.imagen = convertir_imagen(p.imagen)

    return templates.TemplateResponse(
        "pilotos_list.html",
        {"request": request, "pilotos": pilotos, "mensaje": "Listado de pilotos eliminados"}
    )
