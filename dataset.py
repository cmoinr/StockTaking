# Script para poblar la base de datos con categorías y productos iniciales para la tienda de fútbol
from pymongo import MongoClient
from models import get_category_collection, get_product_collection, validate_category, validate_product
import requests

MONGO_URI = 'mongodb://localhost:27017/stock_db'

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.get_database()

# Función para obtener la tasa de cambio actual desde el endpoint /tasa_cambio de app.py
def obtener_tasa_cambio():
    try:
        resp = requests.get('http://127.0.0.1:5000/tasa_cambio', timeout=5)
        data = resp.json()
        return float(data.oficial.promedio)
    except Exception as e:
        print(f"No se pudo obtener la tasa de cambio automáticamente: {e}")
        return 40.0  # Valor por defecto si falla

# Obtener tasa de cambio actual
TASA_CAMBIO = obtener_tasa_cambio()

# Categorías principales para tienda de fútbol
categorias = [
    {"nombre": "Calzado", "descripcion": "Botines, zapatillas de fútbol campo y futsal"},
    {"nombre": "Balones", "descripcion": "Balones de fútbol y futsal"},
    {"nombre": "Indumentaria", "descripcion": "Ropa deportiva: camisetas, shorts, medias"},
    {"nombre": "Protecciones", "descripcion": "Canilleras, tobilleras, protectores"},
    {"nombre": "Entrenamiento", "descripcion": "Conos, vallas, escaleras, mini arcos"},
    {"nombre": "Accesorios", "descripcion": "Guantes, infladores, silbatos, cintas, bolsos"}
]

# Insertar categorías si no existen
cat_col = get_category_collection(db)
for cat in categorias:
    if not cat_col.find_one({"nombre": cat["nombre"]}):
        if validate_category(cat):
            cat_col.insert_one(cat)

# Productos de ejemplo
productos = [
    {
    "nombre": "Botines Adidas Predator",
    "caracteristicas": {
        "color": "Negro/Rojo",
        "talla": "42",
        "deporte": "futbol campo"
    },
    "stock": 12,
    "categoria": "Calzado",
    "precio": {
        "$": 80,
        "bs": 7832.25
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/predator.png"
    },
    {
    "nombre": "Botines Nike Mercurial AIR",
    "caracteristicas": {
        "color": "Azul",
        "talla": "41"
    },
    "stock": 10,
    "categoria": "Calzado",
    "precio": {
        "$": 90,
        "bs": 8811.28
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/mercurial.png"
    },
    {
    "nombre": "Zapatillas Futsal Joma Top Flex",
    "caracteristicas": {
        "color": "Blanco/Azul",
        "talla": "43",
        "tecnologia": "reactive-ball"
    },
    "stock": 7,
    "categoria": "Calzado",
    "precio": {
        "$": 90,
        "bs": 8811.28
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/top-flex.png"
    },
    {
    "nombre": "Zapatillas Futsal Adidas Sala",
    "caracteristicas": {
        "color": "Negro",
        "talla": "40",
        "suela": "non-marking",
        "suelo": "futsal"
    },
    "stock": 10,
    "categoria": "Calzado",
    "precio": {
        "$": 75,
        "bs": 7342.73
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/sala.png"
    },
    {
    "nombre": "Balón Nike Futsal Pro",
    "caracteristicas": {
        "tamaño": "4",
        "color": "naranja",
        "clase": "termosellado"
    },
    "stock": 15,
    "categoria": "Balones",
    "precio": {
        "$": 35,
        "bs": 3426.61
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/nike-pro.png"
    },
    {
    "nombre": "Balón Adidas Tango",
    "caracteristicas": {
        "tamaño": "5",
        "color": "Blanco/Negro"
    },
    "stock": 10,
    "categoria": "Balones",
    "precio": {
        "$": 28,
        "bs": 2741.29
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/adidas-tango.png"
    },
    {
    "nombre": "Balón Penalty Campo",
    "caracteristicas": {
        "tamaño": "5",
        "color": "amarillo/azul",
        "clase": "termosellado"
    },
    "stock": 7,
    "categoria": "Balones",
    "precio": {
        "$": 32,
        "bs": 3132.9
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/penalty-balon.png"
    },
    {
    "nombre": "Camiseta Oficial Argentina 2022",
    "caracteristicas": {
        "talla": "M",
        "escudo": "termosellado",
        "tecnologia": "AeroReady"
    },
    "stock": 7,
    "categoria": "Indumentaria",
    "precio": {
        "$": 64,
        "bs": 6265.8
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/argentina-22.png"
    },
    {
    "nombre": "Camiseta Oficial Brasil 2022",
    "caracteristicas": {
        "talla": "S-XL",
        "escudo": "termosellado",
        "marca": "nike",
        "tecnologia": "Dry-Fit ADV"
    },
    "stock": 4,
    "categoria": "Indumentaria",
    "precio": {
        "$": 75,
        "bs": 7342.73
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/brasil-22.png"
    }
]

prod_col = get_product_collection(db)
for prod in productos:
    if not prod_col.find_one({"nombre": prod["nombre"]}):
        if validate_product(prod):
            prod_col.insert_one(prod)

print("Categorías y productos insertados correctamente.")
