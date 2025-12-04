from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from database import Base, engine, SessionLocal
from routers import escuderias, pilotos, circuitos, tiempos, dashboard, teams

import base64

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Fórmula 1",
    version="3.0",
    description="F1 información de pilotos.",
)

# 🔎 Función utilitaria para convertir imágenes a base64
def convertir_imagen(imagen_binaria):
    if imagen_binaria:
        return base64.b64encode(imagen_binaria).decode("utf-8")
    return None

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Routers
app.include_router(escuderias.router)
app.include_router(pilotos.router)
app.include_router(circuitos.router)
app.include_router(tiempos.router)
app.include_router(dashboard.router)
app.include_router(teams.router)   # 👈 nuevo router para la vista de equipos/pilotos

# Archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🔎 Manejo de conexiones para evitar bloqueos
@app.on_event("startup")
def startup_event():
    # Aquí podrías inicializar recursos si lo necesitas
    pass

@app.on_event("shutdown")
def shutdown_event():
    # Cerrar conexiones activas al apagar la app
    db = SessionLocal()
    db.close()

@app.get("/")
def root():
    # Puedes redirigir al dashboard o a escuderías según tu preferencia
    return RedirectResponse(url="/teams/")
