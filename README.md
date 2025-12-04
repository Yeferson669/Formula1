📘 Proyecto FórmulaZ – Aplicación Web con FastAPI
🚀 Descripción General
FórmulaZ es una aplicación web desarrollada con FastAPI y SQLAlchemy, diseñada para gestionar información relacionada con escuderías, circuitos y tiempos de carrera de Fórmula 1. El proyecto combina un backend robusto con un frontend moderno y visualmente atractivo, desplegado en Render y conectado a una base de datos PostgreSQL alojada en Clever Cloud.

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

📂 Estructura del Proyecto
Código
Formulaz/
│── main.py              # Punto de entrada FastAPI
│── models.py            # Definición de modelos SQLAlchemy
│── routers/             # Endpoints organizados por módulo
│   ├── escuderias.py
│   ├── circuitos.py
│   └── tiempos.py
│── templates/           # Vistas HTML con Jinja2
│   ├── base.html
│   ├── index.html
│   ├── circuito_detail.html
│   ├── tiempo_detail.html
│   └── error.html
│── static/              # Archivos CSS, JS, imágenes
│── requirements.txt     # Dependencias del proyecto
│── .gitignore           # Exclusiones para Git
│── README.md            # Documentación
⚙️ Instalación Local
Clonar el repositorio

bash
git clone https://github.com/Yeferson669/Formulaz.git
cd Formulaz
Crear entorno virtual

bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Instalar dependencias

bash
pip install -r requirements.txt
Configurar variables de entorno Crear un archivo .env en la raíz del proyecto:

env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_db
SECRET_KEY=tu_clave_secreta
DEBUG=True
Ejecutar la aplicación

bash
uvicorn main:app --reload
🌐 Despliegue en Render
Build Command:

bash
pip install -r requirements.txt
Start Command:

bash
uvicorn main:app --host=0.0.0.0 --port=10000
Environment Group:

DATABASE_URL → cadena de conexión de Clever Cloud.

SECRET_KEY → clave secreta para seguridad.

DEBUG → modo de depuración.

🧪 Ejemplo de Endpoints
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

.gitignore configurado para excluir venv/, __pycache__/ y archivos innecesarios.

Commits limpios y descriptivos para mantener un historial ordenado.

Variables de entorno seguras en Render (sin credenciales en el código).

👨‍💻 Autor
Yeferson Guaca Desarrollador backend/frontend con experiencia en FastAPI, SQLAlchemy y despliegue en la nube. 📧 Contacto: ydguaca49@ucatolica.edu.co


