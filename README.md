# Stocktaking Web-App

Este proyecto es una web-app en Python (Flask) para el control de inventario de un comercio pequeño, integrando MongoDB. Permite gestionar productos, sus características y el stock disponible, con una interfaz web moderna y búsquedas avanzadas.

## Estructura del proyecto

- `app.py` — Aplicación principal Flask
- `/models` — Modelos de datos (productos, categorías, movimientos de stock)
- `/static` — Archivos estáticos (CSS, JS, imágenes)
- `/templates` — Plantillas HTML para la web-app
- `requirements.txt` — Dependencias del proyecto
- `README.md` — Este archivo
- `ER-diagram.png` — Diagrama de la base de datos (MongoDB)

## Estado del proyecto

- [x] Alta, edición y eliminación de productos
- [x] Búsqueda por nombre y búsquedas avanzadas (por característica y por rango de stock)
- [x] Interfaz web elegante y responsiva
- [x] Integración con MongoDB local (creación automática de la base de datos y colecciones)
- [x] Diagrama de base de datos incluido

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

## Pruebas
- Puedes ejecutar `test_mongo_connection.py` para verificar la conexión a MongoDB antes de iniciar la app.

## Diagrama de la base de datos
- Consulta el archivo `ER-diagram.png` para ver la estructura de las colecciones y relaciones principales.

## Notas
- La base de datos `stock_db` y las colecciones se crean automáticamente al agregar el primer producto.
- Todos los estilos están centralizados en `static/style.css`.

---

> **Requisitos:** Python 3.8+, MongoDB Community Edition, entorno virtual recomendado.