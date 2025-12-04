from __future__ import annotations
from pydantic import BaseModel, confloat, conint, constr
from typing import List, Optional
from datetime import date


class CircuitoBase(BaseModel):
    nombre: constr(min_length=3, max_length=50)
    pais: Optional[constr(min_length=2, max_length=50)] = None
    longitud_km: Optional[conint(gt=0, lt=10_000)] = None  
    activo: bool = True
    imagen_url: Optional[str] = None

class Circuito(CircuitoBase):
    id: int

    class Config:
        orm_mode = True


class PilotoBase(BaseModel):
    nombre: constr(min_length=3, max_length=50)
    nacionalidad: constr(min_length=2, max_length=50)
    numero: conint(ge=1, le=99)  
    activo: bool = True
    escuderia_id: Optional[int] = None

    
    fecha_nacimiento: Optional[date] = None
    biografia: Optional[constr(min_length=10, max_length=500)] = None
    twitter: Optional[constr(min_length=3, max_length=50)] = None
    imagen_url: Optional[str] = None

class Piloto(PilotoBase):
    id: int
    circuitos: List[Circuito] = []

    class Config:
        orm_mode = True


class EscuderiaBase(BaseModel):
    nombre: constr(min_length=3, max_length=50)
    pais: constr(min_length=2, max_length=50)
    activo: bool = True
    logo_url: Optional[str] = None

class Escuderia(EscuderiaBase):
    id: int
    pilotos: List[Piloto] = []

    class Config:
        orm_mode = True


class TiempoBase(BaseModel):
    piloto_id: int
    circuito_id: int
    tiempo_vuelta: confloat(gt=0)  
    posicion: Optional[conint(ge=1)] = None
    fecha: Optional[date] = None

class Tiempo(TiempoBase):
    id: int
    piloto: Optional[Piloto] = None
    circuito: Optional[Circuito] = None

    class Config:
        orm_mode = True