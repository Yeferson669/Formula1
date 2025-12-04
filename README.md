# 🏎️ Proyecto Fórmula 1 - Gestión de Pilotos, Escuderías, Circuitos y Tiempos

Este proyecto es una aplicación web desarrollada con **FastAPI + SQLAlchemy + Jinja2** que permite gestionar información de **pilotos, escuderías, circuitos y tiempos de carrera**.  
Incluye funcionalidades de creación, edición, eliminación lógica (soft delete) y restauración de registros, además de formularios y vistas dinámicas.

---

## 📐 Diagrama de Clases

```mermaid
classDiagram
    Piloto --> Escuderia : pertenece
    Tiempo --> Piloto : registrado por
    Tiempo --> Circuito : realizado en
    Escuderia --> Piloto : tiene (máx 2)
    Circuito --> Tiempo : acumula


## 🔄 Diagrama de Actividades
flowchart TD
    A[Usuario] --> B[Formulario creación]
    B --> C[Validación datos]
    C -->|Correcto| D[Guardar en BD]
    C -->|Error| E[Mostrar mensaje]
    D --> F[Listado activo]
    F --> G[Eliminar registro]
    G --> H[Marcar activo=False]
    H --> I[Listado eliminados]
    I --> J[Restaurar registro]
    J --> F


## 🗂️ Modelos
Piloto: relación con Escudería (máx 2 pilotos activos por escudería).

Escudería: relación con Pilotos.

Circuito: relación con Tiempos.

Tiempo: relación con Piloto y Circuito, guarda tiempo en segundos pero se muestra en formato MM:SS.mmm.


## 🚀 Despliegue

Clonar repositorio: git clone https://github.com/usuario/proyecto-f1.git
cd proyecto-f1

Crear entorno virtual e instalar dependencias:python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt

Ejecutar servidor:uvicorn main:app --reload

##  🌐 Endpoints principales
    ##Pilotos
GET /pilotos/ → Listado + formulario + eliminados

POST /pilotos/crear/ → Crear piloto

POST /pilotos/editar/{id} → Editar piloto

GET /pilotos/eliminar/{id} → Eliminar (soft delete)

GET /pilotos/restaurar/{id} → Restaurar

Escuderías
GET /escuderias/ → Listado + formulario + eliminadas

POST /escuderias/crear/ → Crear escudería

POST /escuderias/editar/{id} → Editar escudería

GET /escuderias/eliminar/{id} → Eliminar

GET /escuderias/restaurar/{id} → Restaurar

Circuitos
GET /circuitos/ → Listado + formulario + eliminados

POST /circuitos/crear/ → Crear circuito

POST /circuitos/editar/{id} → Editar circuito

GET /circuitos/eliminar/{id} → Eliminar

GET /circuitos/restaurar/{id} → Restaurar

Tiempos
GET /tiempos/ → Listado + formulario + eliminados

POST /tiempos/crear/ → Crear tiempo

POST /tiempos/editar/{id} → Editar tiempo

GET /tiempos/eliminar/{id} → Eliminar

GET /tiempos/restaurar/{id} → Restaurar

Formato de tiempo: se guarda en segundos pero se muestra como MM:SS.mmm.

🛠️ Tecnologías usadas
Backend

FastAPI → Framework principal para construir la API y manejar rutas.

SQLAlchemy → ORM para manejar modelos y consultas a la base de datos.

PostgreSQL → Base de datos relacional usada para almacenar pilotos, escuderías, circuitos y tiempos.

Frontend

Jinja2 → Motor de plantillas para renderizar HTML dinámico.

TailwindCSS → Framework CSS para estilos modernos y responsivos.

Infraestructura

Uvicorn → Servidor ASGI para correr la aplicación FastAPI.

Python 3.10+ → Lenguaje de programación base del proyecto.

Extras

Soft delete + restauración → Implementado en todos los modelos para trazabilidad.

Conversión de imágenes a Base64 → Para mostrar logos y fotos en las vistas.

Formato de tiempos → Conversión de segundos a MM:SS.mmm para mostrar tiempos de vuelta.



#🎯 Conclusión#
Este proyecto demuestra cómo construir una aplicación web robusta, escalable y clara con FastAPI, aplicando buenas prácticas de:

Soft delete + restauración

Uniformidad de rutas y templates

Conversión de datos (tiempos formateados)

Frontend limpio con TailwindCSS

👨‍💻 Autor: Yeferson David Guaca Buitron
