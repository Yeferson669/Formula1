from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from database import Base, engine
from routers import escuderias, pilotos, circuitos, tiempos, dashboard, teams

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Fórmula 1",
    version="3.0",
    description="F1 información de pilotos.",
)

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

@app.get("/")
def root():
    return RedirectResponse(url="/teams/")
