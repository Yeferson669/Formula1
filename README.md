🏁 Fórmula! – Aplicación Web con FastAPI

Descripción General

Fórmula1 es una aplicación web desarrollada con FastAPI, diseñada para gestionar información sobre escuderías, circuitos y tiempos de carrera de Fórmula 1. El proyecto combina un backend robusto con un frontend moderno y visualmente atractivo, desplegado en Render y conectado a una base de datos PostgreSQL alojada en Clever Cloud.

El objetivo principal es ofrecer una plataforma portable, escalable y segura, con un diseño visual impactante y una infraestructura backend confiable.

🛠️ Tecnologías Utilizadas
Lenguaje: Python 3.10+

Framework Backend: FastAPI

ORM: SQLAlchemy

Base de Datos: PostgreSQL (Clever Cloud)

Servidor ASGI: Uvicorn

Frontend: Jinja2 Templates + HTML/CSS

Despliegue: Render

Control de Versiones: Git + GitHub

📁 Estructura del Proyecto
Archivos principales:

main.py: Punto de entrada de la aplicación FastAPI.

models.py: Definición de modelos SQLAlchemy.

requirements.txt: Lista de dependencias del proyecto.

.gitignore: Exclusiones para Git (venv, pycache, etc.).

README.md: Documentación del proyecto.

Carpetas clave:

routers/: Contiene los endpoints organizados por módulo.

escuderias.py: CRUD para escuderías.

circuitos.py: CRUD para circuitos.

tiempos.py: CRUD para tiempos de carrera.

templates/: Vistas HTML renderizadas con Jinja2.

base.html: Template base con navbar y estilos globales.

index.html: Página principal.

circuito_detail.html: Detalle de circuito.

tiempo_detail.html: Detalle de tiempo.

error.html: Página de error personalizada.

static/: Archivos estáticos como CSS, JS e imágenes.

⚙️ Instalación Local
Clonar el repositorio desde GitHub.

Crear y activar un entorno virtual.

Instalar las dependencias listadas en requirements.txt..

Configurar las variables de entorno en un archivo .env con la cadena de conexión a PostgreSQL, clave secreta y modo debug.

Ejecutar la aplicación con Uvicorn en modo desarrollo.

🌐 Despliegue en Render
Build Command: pip install -r requirements.txt

Start Command: uvicorn main:app --host=0.0.0.0 --port=10000

Variables de entorno configuradas en Render:

DATABASE_URL → cadena de conexión de Clever Cloud.

SECRET_KEY → clave secreta para seguridad.

DEBUG → modo de depuración.

🧪 Endpoints Disponibles
Escuderías

GET /escuderias/ → Lista todas las escuderías.

GET /escuderias/{id} → Detalle de una escudería.

POST /escuderias/ → Crear nueva escudería.

Circuitos

GET /circuitos/ → Lista todos los circuitos.

GET /circuitos/{id} → Detalle de un circuito.

POST /circuitos/ → Crear nuevo circuito.

Tiempos

GET /tiempos/ → Lista todos los tiempos registrados.

GET /tiempos/{id} → Detalle de un tiempo.

POST /tiempos/ → Registrar nuevo tiempo.

🎨 Diseño Frontend
Header y Navbar: colores oscuros con contraste sobre fondo rojo, animaciones claras y modernas.

Templates uniformes: vistas con fondos blancos y recuadros compactos para destacar logos e imágenes.

Animaciones: efectos visuales dinámicos pero profesionales, priorizando la experiencia del usuario.

🔒 Buenas Prácticas Implementadas
Uso de pools de conexión en SQLAlchemy para evitar fugas.

Separación clara de routers, templates y static.

.gitignore configurado para excluir venv, pycache y archivos innecesarios.

Commits limpios y descriptivos para mantener un historial ordenado.

Variables de entorno seguras en Render (sin credenciales en el código).

👨‍💻 Autor
Yeferson Guaca

