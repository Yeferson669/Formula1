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
🔄 Diagrama de Actividades
mermaid
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
🗂️ Modelos
Modelo	Relación / Descripción
Piloto	Relación con Escudería (máx 2 pilotos activos por escudería). Incluye imagen y datos.
Escudería	Relación con Pilotos. Tiene nombre, país y logo.
Circuito	Relación con Tiempos. Incluye longitud, país, descripción e imagen.
Tiempo	Relación con Piloto y Circuito. Guarda tiempo en segundos pero se muestra como MM:SS.mmm.
🚀 Despliegue
bash
# Clonar repositorio
git clone https://github.com/usuario/proyecto-f1.git
cd proyecto-f1

# Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt

# Ejecutar servidor
uvicorn main:app --reload
Acceder en navegador: 👉 http://127.0.0.1:8000

🌐 Endpoints principales
Pilotos
Método	Endpoint	Descripción
GET	/pilotos/	Listado + formulario + eliminados
POST	/pilotos/crear/	Crear piloto
POST	/pilotos/editar/{id}	Editar piloto
GET	/pilotos/eliminar/{id}	Eliminar (soft delete)
GET	/pilotos/restaurar/{id}	Restaurar
Escuderías
Método	Endpoint	Descripción
GET	/escuderias/	Listado + formulario + eliminadas
POST	/escuderias/crear/	Crear escudería
POST	/escuderias/editar/{id}	Editar escudería
GET	/escuderias/eliminar/{id}	Eliminar
GET	/escuderias/restaurar/{id}	Restaurar
Circuitos
Método	Endpoint	Descripción
GET	/circuitos/	Listado + formulario + eliminados
POST	/circuitos/crear/	Crear circuito
POST	/circuitos/editar/{id}	Editar circuito
GET	/circuitos/eliminar/{id}	Eliminar
GET	/circuitos/restaurar/{id}	Restaurar
Tiempos
Método	Endpoint	Descripción
GET	/tiempos/	Listado + formulario + eliminados
POST	/tiempos/crear/	Crear tiempo
POST	/tiempos/editar/{id}	Editar tiempo
GET	/tiempos/eliminar/{id}	Eliminar
GET	/tiempos/restaurar/{id}	Restaurar
Nota	-	El tiempo se guarda en segundos pero se muestra como MM:SS.mmm.
🛠️ Tecnologías usadas
Categoría	Tecnologías
Backend	FastAPI, SQLAlchemy, PostgreSQL
Frontend	Jinja2, TailwindCSS
Infraestructura	Uvicorn, Python 3.10+
Extras	Soft delete + restauración, Conversión de imágenes a Base64, Formato de tiempos MM:SS.mmm
🎯 Conclusión
Este proyecto demuestra cómo construir una aplicación web robusta, escalable y clara con FastAPI, aplicando buenas prácticas de:

Soft delete + restauración

Uniformidad de rutas y templates

Conversión de datos (tiempos formateados)

Frontend limpio con TailwindCSS

👨‍💻 Autor: Yeferson David Guaca Buitron
👨‍💻 Autor: Yeferson David Guaca Buitron

