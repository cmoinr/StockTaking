# Script para poblar la base de datos con categorías y productos iniciales para la tienda de fútbol
from pymongo import MongoClient
from models import get_category_collection, get_product_collection, validate_category, validate_product
import requests
from bson.objectid import ObjectId

MONGO_URI = 'mongodb://localhost:27017/stock_db'

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.get_database()

# # Función para obtener la tasa de cambio actual desde el endpoint /tasa_cambio de app.py
# def obtener_tasa_cambio():
#     try:
#         resp = requests.get('http://127.0.0.1:5000/tasa_cambio', timeout=5)
#         data = resp.json()
#         return float(data.oficial.promedio)
#     except Exception as e:
#         print(f"No se pudo obtener la tasa de cambio automáticamente: {e}")
#         return 40.0  # Valor por defecto si falla

# # Obtener tasa de cambio actual
# TASA_CAMBIO = obtener_tasa_cambio()

# Categorías principales para tienda de fútbol
categorias = [
    {"nombre": "Calzado", "descripcion": "Botines, zapatillas de fútbol campo y futsal", "user_id": ObjectId("684df1c9049b0ea71d0178ce")},
    {"nombre": "Balones", "descripcion": "Balones de fútbol y futsal", "user_id": ObjectId("684df1c9049b0ea71d0178ce")},
    {"nombre": "Indumentaria", "descripcion": "Ropa deportiva: camisetas, shorts, medias", "user_id": ObjectId("684df1c9049b0ea71d0178ce")},
    {"nombre": "Protecciones", "descripcion": "Canilleras, tobilleras, protectores", "user_id": ObjectId("684df1c9049b0ea71d0178ce")},
    {"nombre": "Entrenamiento", "descripcion": "Conos, vallas, escaleras, mini arcos", "user_id": ObjectId("684df1c9049b0ea71d0178ce")},
    {"nombre": "Accesorios", "descripcion": "Guantes, infladores, silbatos, cintas, bolsos", "user_id": ObjectId("684df1c9049b0ea71d0178ce")}
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
    "stock": 10,
    "categoria": "Calzado",
    "precio": {
        "$": 80,
        "bs": 7832.25
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/2b0c665f160b49d5b0d4175739554cfa.jpg",
    "user_id": {
        "$oid": "684df1c9049b0ea71d0178ce"
    }
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
        "$": 95,
        "bs": 9704.91
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/a7bca452265c497492e381af5bc51b05.jpg",
    "user_id": {
        "$oid": "684df1c9049b0ea71d0178ce"
    }
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
        "$": 88,
        "bs": 8989.82
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/top-flex.png",
    "user_id": {
        "$oid": "684df1c9049b0ea71d0178ce"
    }
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
        "$": 77,
        "bs": 7866.09
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/sala.png",
    "user_id": {
        "$oid": "684df1c9049b0ea71d0178ce"
    }
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
        "$": 32,
        "bs": 3269.02
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/a645675d62a3465c9cebb2949acc6d65.jpg",
    "user_id": {
        "$oid": "684df1c9049b0ea71d0178ce"
    }
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
        "$": 21,
        "bs": 2145.3
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/5179fa9b07984d1792c1fbe3bc382430.jpg",
    "user_id": {
        "$oid": "684df1c9049b0ea71d0178ce"
    }
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
        "$": 30,
        "bs": 3064.71
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/penalty-balon.png",
    "user_id": {
        "$oid": "684df1c9049b0ea71d0178ce"
    }
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
        "$": 62.99,
        "bs": 6434.87
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/argentina-22.png",
    "user_id": {
        "$oid": "684df1c9049b0ea71d0178ce"
    }
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
        "$": 74,
        "bs": 7559.62
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/brasil-22.png",
    "user_id": {
        "$oid": "684df1c9049b0ea71d0178ce"
    }
    },
    {
    "nombre": "canilleras fut",
    "caracteristicas": {
        "color": "azul",
        "marca": "puma"
    },
    "stock": 5,
    "categoria": "Accesorios",
    "precio": {
        "$": 12.55,
        "bs": 1282.07
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/b9982775b8ef400fa3fd31f29b61af58.jpg",
    "user_id": {
        "$oid": "684df1c9049b0ea71d0178ce"
    }
    },
    {
    "nombre": "cinta capitan",
    "caracteristicas": {
        "color": "rojo",
        "marca": "nike"
    },
    "stock": 3,
    "categoria": "Accesorios",
    "precio": {
        "$": 8,
        "bs": 817.26
    },
    "user_id": {
        "$oid": "684e017a6ed1f852fc5b03ad"
    },
    "imagen": "https://storage.googleapis.com/stocktaking-bucket/uploads/161ab900745f4ec8a81db9df709a2f4b.jpg"
    }
]

# Convertir user_id de cada producto a ObjectId si es necesario
for prod in productos:
    if isinstance(prod.get('user_id'), dict) and '$oid' in prod['user_id']:
        prod['user_id'] = ObjectId(prod['user_id']['$oid'])

prod_col = get_product_collection(db)
for prod in productos:
    if not prod_col.find_one({"nombre": prod["nombre"]}):
        if validate_product(prod):
            prod_col.insert_one(prod)

print("Categorías y productos insertados correctamente.")