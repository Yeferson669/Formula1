from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Float, Table, LargeBinary
from sqlalchemy.orm import relationship
from database import Base


piloto_circuito = Table(
    "piloto_circuito",
    Base.metadata,
    Column("piloto_id", ForeignKey("pilotos.id"), primary_key=True),
    Column("circuito_id", ForeignKey("circuitos.id"), primary_key=True),
)


class Escuderia(Base):
    __tablename__ = "escuderias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, index=True, nullable=False)
    pais = Column(String(50), nullable=False)
    activo = Column(Boolean, default=True)

    
    logo_url = Column(String(255), nullable=True)
    
    logo = Column(LargeBinary, nullable=True)

    pilotos = relationship("Piloto", back_populates="escuderia")


class Piloto(Base):
    __tablename__ = "pilotos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), index=True, nullable=False)
    nacionalidad = Column(String(50), nullable=False)
    numero = Column(Integer, nullable=False)
    activo = Column(Boolean, default=True)
    escuderia_id = Column(Integer, ForeignKey("escuderias.id"))

    
    fecha_nacimiento = Column(Date, nullable=True)
    biografia = Column(String(500), nullable=True)
    twitter = Column(String(50), nullable=True)

    
    imagen_url = Column(String(255), nullable=True)
    
    imagen = Column(LargeBinary, nullable=True)

    escuderia = relationship("Escuderia", back_populates="pilotos")
    circuitos = relationship("Circuito", secondary=piloto_circuito, back_populates="pilotos")
    tiempos = relationship("Tiempo", back_populates="piloto")


class Circuito(Base):
    __tablename__ = "circuitos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, index=True, nullable=False)
    pais = Column(String(50), nullable=False)
    longitud_km = Column(Float, nullable=True)  
    activo = Column(Boolean, default=True)

    
    imagen_url = Column(String(255), nullable=True)
    
    imagen = Column(LargeBinary, nullable=True)

    descripcion = Column(String, nullable=True)

    pilotos = relationship("Piloto", secondary=piloto_circuito, back_populates="circuitos")
    tiempos = relationship("Tiempo", back_populates="circuito")
   

class Tiempo(Base):
    __tablename__ = "tiempos"

    id = Column(Integer, primary_key=True, index=True)
    piloto_id = Column(Integer, ForeignKey("pilotos.id"))
    circuito_id = Column(Integer, ForeignKey("circuitos.id"))
    tiempo_vuelta = Column(Float, nullable=False)
    posicion = Column(Integer, nullable=True)
    fecha = Column(Date, nullable=True)
    activo = Column(Boolean, default=True)

    
    piloto = relationship("Piloto", back_populates="tiempos")
    circuito = relationship("Circuito", back_populates="tiempos")

    def __repr__(self):
        return f"<Tiempo id={self.id} piloto_id={self.piloto_id} circuito_id={self.circuito_id} tiempo_vuelta={self.tiempo_vuelta}>"
