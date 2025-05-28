# Stocktaking Web-App

Este proyecto es una web-app en Python (Flask) para el control de inventario de un comercio pequeño, integrando MongoDB. Permite gestionar productos, sus características y el stock disponible, con una interfaz web moderna y búsquedas avanzadas.

## Estructura del proyecto

- `app.py` — Aplicación principal Flask
- `/models` — Modelos de datos (productos, categorías, movimientos de stock)
- `/static` — Archivos estáticos (CSS, JS, imágenes)
- `/templates` — Plantillas HTML para la web-app
- `requirements.txt` — Dependencias del proyecto
- `README.md` — Este archivo

## Funcionalidades principales

- Alta, edición y eliminación de productos
- Búsqueda por nombre y búsquedas avanzadas (por característica y por rango de stock)
- Interfaz web elegante y responsiva
- Integración con MongoDB local (creación automática de la base de datos y colecciones)

## Instalación y uso

1. **Clona el repositorio y entra a la carpeta del proyecto.**
2. **Crea y activa un entorno virtual:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
3. **Instala las dependencias:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Asegúrate de tener MongoDB instalado y corriendo en tu máquina.**
5. **Inicia la aplicación:**
   ```powershell
   $env:FLASK_APP="app"
   $env:FLASK_ENV="development"
   flask run
   ```
6. **Abre tu navegador en** [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Notas
- La base de datos `stock_db` y las colecciones se crean automáticamente al agregar el primer producto.
- Todos los estilos están centralizados en `static/style.css`.
- Puedes personalizar los modelos en `/models` según tus necesidades.

---

> **Requisitos:** Python 3.8+, MongoDB Community Edition, entorno virtual recomendado.