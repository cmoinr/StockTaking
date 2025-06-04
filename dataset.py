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
        return float(data['tasa'])
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
        "caracteristicas": {"color": "Negro/Rojo", "talla": "42"},
        "stock": 8,
        "categoria": "Calzado",
        "precio": {"$": 120.00, "bs": round(120.00 * TASA_CAMBIO, 2)},
        "imagen": "predator.png"
    },
    {
        "nombre": "Botines Nike Mercurial",
        "caracteristicas": {"color": "Azul", "talla": "41"},
        "stock": 10,
        "categoria": "Calzado",
        "precio": {"$": 135.00, "bs": round(135.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Zapatillas Futsal Joma Top Flex",
        "caracteristicas": {"color": "Blanco/Azul", "talla": "43"},
        "stock": 7,
        "categoria": "Calzado",
        "precio": {"$": 95.00, "bs": round(95.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Zapatillas Futsal Adidas Sala",
        "caracteristicas": {"color": "Negro", "talla": "40"},
        "stock": 5,
        "categoria": "Calzado",
        "precio": {"$": 110.00, "bs": round(110.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Balón Nike Futsal Pro",
        "caracteristicas": {"tamaño": "4", "color": "Blanco/Azul"},
        "stock": 15,
        "categoria": "Balones",
        "precio": {"$": 60.00, "bs": round(60.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Balón Adidas Tango",
        "caracteristicas": {"tamaño": "5", "color": "Blanco/Negro"},
        "stock": 12,
        "categoria": "Balones",
        "precio": {"$": 55.00, "bs": round(55.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Balón Penalty Campo",
        "caracteristicas": {"tamaño": "5", "color": "Amarillo"},
        "stock": 9,
        "categoria": "Balones",
        "precio": {"$": 50.00, "bs": round(50.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Camiseta Oficial Argentina 2022",
        "caracteristicas": {"talla": "M"},
        "stock": 5,
        "categoria": "Indumentaria",
        "precio": {"$": 45.00, "bs": round(45.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Camiseta Oficial Brasil 2022",
        "caracteristicas": {"talla": "L"},
        "stock": 4,
        "categoria": "Indumentaria",
        "precio": {"$": 45.00, "bs": round(45.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Short Deportivo Puma",
        "caracteristicas": {"talla": "S", "color": "Negro"},
        "stock": 11,
        "categoria": "Indumentaria",
        "precio": {"$": 30.00, "bs": round(30.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Medias Nike Performance",
        "caracteristicas": {"talla": "M", "color": "Blanco"},
        "stock": 20,
        "categoria": "Indumentaria",
        "precio": {"$": 15.00, "bs": round(15.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Canilleras Puma Ultra",
        "caracteristicas": {"talla": "L", "color": "Negro"},
        "stock": 12,
        "categoria": "Protecciones",
        "precio": {"$": 25.00, "bs": round(25.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Canilleras Adidas X",
        "caracteristicas": {"talla": "M", "color": "Rojo"},
        "stock": 8,
        "categoria": "Protecciones",
        "precio": {"$": 28.00, "bs": round(28.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Tobilleras Reforzadas",
        "caracteristicas": {"talla": "Única", "color": "Negro"},
        "stock": 10,
        "categoria": "Protecciones",
        "precio": {"$": 18.00, "bs": round(18.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Set de Conos Entrenamiento (20u)",
        "caracteristicas": {"color": "Naranja"},
        "stock": 3,
        "categoria": "Entrenamiento",
        "precio": {"$": 40.00, "bs": round(40.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Escalera de Agilidad 4m",
        "caracteristicas": {"color": "Amarillo"},
        "stock": 2,
        "categoria": "Entrenamiento",
        "precio": {"$": 55.00, "bs": round(55.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Vallas de Salto (4u)",
        "caracteristicas": {"altura": "30cm", "color": "Rojo"},
        "stock": 4,
        "categoria": "Entrenamiento",
        "precio": {"$": 70.00, "bs": round(70.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Mini Arcos Portátiles",
        "caracteristicas": {"ancho": "1.2m"},
        "stock": 2,
        "categoria": "Entrenamiento",
        "precio": {"$": 90.00, "bs": round(90.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Guantes de Arquero Reusch",
        "caracteristicas": {"talla": "9", "color": "Blanco/Verde"},
        "stock": 6,
        "categoria": "Accesorios",
        "precio": {"$": 50.00, "bs": round(50.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Guantes de Arquero Uhlsport",
        "caracteristicas": {"talla": "10", "color": "Negro/Amarillo"},
        "stock": 5,
        "categoria": "Accesorios",
        "precio": {"$": 55.00, "bs": round(55.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Bolsos Deportivos Nike",
        "caracteristicas": {"color": "Negro", "capacidad": "40L"},
        "stock": 7,
        "categoria": "Accesorios",
        "precio": {"$": 40.00, "bs": round(40.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Cintas de Capitán",
        "caracteristicas": {"color": "Azul"},
        "stock": 10,
        "categoria": "Accesorios",
        "precio": {"$": 10.00, "bs": round(10.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Silbatos Fox 40",
        "caracteristicas": {"color": "Negro"},
        "stock": 15,
        "categoria": "Accesorios",
        "precio": {"$": 12.00, "bs": round(12.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Inflador de Balones Manual",
        "caracteristicas": {"color": "Rojo"},
        "stock": 8,
        "categoria": "Accesorios",
        "precio": {"$": 8.00, "bs": round(8.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Red para Arco 7x2m",
        "caracteristicas": {"color": "Blanco"},
        "stock": 3,
        "categoria": "Accesorios",
        "precio": {"$": 25.00, "bs": round(25.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Chalecos de Entrenamiento (10u)",
        "caracteristicas": {"color": "Verde"},
        "stock": 5,
        "categoria": "Entrenamiento",
        "precio": {"$": 35.00, "bs": round(35.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Cinta Marcadora de Campo",
        "caracteristicas": {"color": "Blanco"},
        "stock": 2,
        "categoria": "Accesorios",
        "precio": {"$": 5.00, "bs": round(5.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Bebederos Deportivos (Pack 6u)",
        "caracteristicas": {"color": "Transparente"},
        "stock": 4,
        "categoria": "Accesorios",
        "precio": {"$": 20.00, "bs": round(20.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Muñequeras Adidas",
        "caracteristicas": {"color": "Negro"},
        "stock": 12,
        "categoria": "Accesorios",
        "precio": {"$": 15.00, "bs": round(15.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Gorras Nike Running",
        "caracteristicas": {"color": "Blanco"},
        "stock": 6,
        "categoria": "Accesorios",
        "precio": {"$": 20.00, "bs": round(20.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Protectores Bucales Sencillos",
        "caracteristicas": {"color": "Transparente"},
        "stock": 10,
        "categoria": "Protecciones",
        "precio": {"$": 10.00, "bs": round(10.00 * TASA_CAMBIO, 2)}
    },
    {
        "nombre": "Vendajes Elásticos Deportivos",
        "caracteristicas": {"color": "Beige"},
        "stock": 14,
        "categoria": "Accesorios",
        "precio": {"$": 12.00, "bs": round(12.00 * TASA_CAMBIO, 2)}
    }
]

prod_col = get_product_collection(db)
for prod in productos:
    if not prod_col.find_one({"nombre": prod["nombre"]}):
        if validate_product(prod):
            prod_col.insert_one(prod)

print("Categorías y productos insertados correctamente.")
