from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from database import Base, engine, SessionLocal
from routers import escuderias, pilotos, circuitos, tiempos, dashboard, teams

import base64


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Fórmula 1",
    version="3.0",
    description="F1 información de pilotos.",
)


def convertir_imagen(imagen_binaria):
    if imagen_binaria:
        return base64.b64encode(imagen_binaria).decode("utf-8")
    return None


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.include_router(escuderias.router)
app.include_router(pilotos.router)
app.include_router(circuitos.router)
app.include_router(tiempos.router)
app.include_router(dashboard.router)
app.include_router(teams.router)   


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def startup_event():
    
    pass

@app.on_event("shutdown")
def shutdown_event():
    
    db = SessionLocal()
    db.close()

@app.get("/")
def root():
    
    return RedirectResponse(url="/teams/")
