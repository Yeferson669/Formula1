# Formula1 🏎️

## Descripción  
Formula1 es una aplicación web desarrollada con **FastAPI** para gestionar información sobre escuderías, circuitos y tiempos de carrera de Fórmula 1. Ofrece un backend robusto junto a un frontend basado en plantillas HTML/Jinja2, con una estructura escalable, portable y segura.  

## Tecnologías utilizadas  
- **Python 3.10+**  
- Backend: **FastAPI**  
- ORM: **SQLAlchemy**  
- Base de datos: **PostgreSQL** (ej. via Clever Cloud)  
- Servidor ASGI: **Uvicorn**  
- Frontend: **Jinja2 Templates + HTML / CSS**  
- Despliegue: **Render**, con variables de entorno para configuración  


## Instalación (local)  

1. Clona este repositorio:  
   ```bash
   git clone https://github.com/Yeferson669/Formula1.git
   cd Formula1

2. Crea y activa un entorno virtual:
      python -m venv venv  
      source venv/bin/activate
      en Windows: venv\Scripts\activate

4. Instala las dependencias:
    pip install -r requirements.txt

5. Configura las variables de entorno (por ejemplo en un archivo .env):

   DATABASE_URL: cadena de conexión a PostgreSQL
   SECRET_KEY: clave para seguridad (si aplica)
   DEBUG: modo debug (True/False)

## Despliegue

Para desplegar en producción (por ejemplo usando Render):

Comando build: pip install -r requirements.txt

Comando start: uvicorn main:app --host 0.0.0.0 --port 10000

Asegúrate de configurar las variables de entorno de producción (cadena a PostgreSQL, clave secreta, modo debug, etc.).
## Tecnologías utilizadas

Python 3.10+

FastAPI

SQLAlchemy ORM

PostgreSQL

Uvicorn

Jinja2 Templates

HTML / CSS

Render (Deployment)

## Endpoints disponibles

 # Escuderia
 
| Método | Ruta               | Descripción       |
| ------ | ------------------ | ----------------- |
| GET    | `/escuderias/`     | Listar escuderías |
| GET    | `/escuderias/{id}` | Obtener detalle   |
| POST   | `/escuderias/`     | Crear             |


## Circuitos

| Método | Ruta              | Descripción      |
| ------ | ----------------- | ---------------- |
| GET    | `/circuitos/`     | Listar circuitos |
| GET    | `/circuitos/{id}` | Detalle          |
| POST   | `/circuitos/`     | Crear            |


## Tiempos

| Método | Ruta            | Descripción      |
| ------ | --------------- | ---------------- |
| GET    | `/tiempos/`     | Listar registros |
| GET    | `/tiempos/{id}` | Detalle          |
| POST   | `/tiempos/`     | Registrar tiempo |


## Buenas prácticas implementadas

Arquitectura MVC/MVT

Variables de entorno seguras

Conexiones PostgreSQL con pool

Rutas separadas por módulos

Templates reutilizables

Código limpio y estructurado

## Autor

Yeferson Guaca


