# Script para poblar la base de datos con categorías y productos iniciales para la tienda de fútbol
from pymongo import MongoClient
from models import get_category_collection, get_product_collection, validate_category, validate_product

MONGO_URI = 'mongodb://localhost:27017/stock_db'

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.get_database()

# # Categorías principales para tienda de fútbol
# categorias = [
#     {"nombre": "Calzado", "descripcion": "Botines, zapatillas de fútbol campo y futsal"},
#     {"nombre": "Balones", "descripcion": "Balones de fútbol y futsal"},
#     {"nombre": "Indumentaria", "descripcion": "Ropa deportiva: camisetas, shorts, medias"},
#     {"nombre": "Protecciones", "descripcion": "Canilleras, tobilleras, protectores"},
#     {"nombre": "Entrenamiento", "descripcion": "Conos, vallas, escaleras, mini arcos"},
#     {"nombre": "Accesorios", "descripcion": "Guantes, infladores, silbatos, cintas, bolsos"}
# ]

# # Insertar categorías si no existen
# cat_col = get_category_collection(db)
# for cat in categorias:
#     if not cat_col.find_one({"nombre": cat["nombre"]}):
#         if validate_category(cat):
#             cat_col.insert_one(cat)

# Productos de ejemplo
productos = [
    {
        "nombre": "Botines Adidas Predator",
        "caracteristicas": {"color": "Negro/Rojo", "talla": "42"},
        "stock": 8,
        "categoria": "Calzado"
    },
    {
        "nombre": "Botines Nike Mercurial",
        "caracteristicas": {"color": "Azul", "talla": "41"},
        "stock": 10,
        "categoria": "Calzado"
    },
    {
        "nombre": "Zapatillas Futsal Joma Top Flex",
        "caracteristicas": {"color": "Blanco/Azul", "talla": "43"},
        "stock": 7,
        "categoria": "Calzado"
    },
    {
        "nombre": "Zapatillas Futsal Adidas Sala",
        "caracteristicas": {"color": "Negro", "talla": "40"},
        "stock": 5,
        "categoria": "Calzado"
    },
    {
        "nombre": "Balón Nike Futsal Pro",
        "caracteristicas": {"tamaño": "4", "color": "Blanco/Azul"},
        "stock": 15,
        "categoria": "Balones"
    },
    {
        "nombre": "Balón Adidas Tango",
        "caracteristicas": {"tamaño": "5", "color": "Blanco/Negro"},
        "stock": 12,
        "categoria": "Balones"
    },
    {
        "nombre": "Balón Penalty Campo",
        "caracteristicas": {"tamaño": "5", "color": "Amarillo"},
        "stock": 9,
        "categoria": "Balones"
    },
    {
        "nombre": "Camiseta Oficial Argentina 2022",
        "caracteristicas": {"talla": "M"},
        "stock": 5,
        "categoria": "Indumentaria"
    },
    {
        "nombre": "Camiseta Oficial Brasil 2022",
        "caracteristicas": {"talla": "L"},
        "stock": 4,
        "categoria": "Indumentaria"
    },
    {
        "nombre": "Short Deportivo Puma",
        "caracteristicas": {"talla": "S", "color": "Negro"},
        "stock": 11,
        "categoria": "Indumentaria"
    },
    {
        "nombre": "Medias Nike Performance",
        "caracteristicas": {"talla": "M", "color": "Blanco"},
        "stock": 20,
        "categoria": "Indumentaria"
    },
    {
        "nombre": "Canilleras Puma Ultra",
        "caracteristicas": {"talla": "L", "color": "Negro"},
        "stock": 12,
        "categoria": "Protecciones"
    },
    {
        "nombre": "Canilleras Adidas X",
        "caracteristicas": {"talla": "M", "color": "Rojo"},
        "stock": 8,
        "categoria": "Protecciones"
    },
    {
        "nombre": "Tobilleras Reforzadas",
        "caracteristicas": {"talla": "Única", "color": "Negro"},
        "stock": 10,
        "categoria": "Protecciones"
    },
    {
        "nombre": "Set de Conos Entrenamiento (20u)",
        "caracteristicas": {"color": "Naranja"},
        "stock": 3,
        "categoria": "Entrenamiento"
    },
    {
        "nombre": "Escalera de Agilidad 4m",
        "caracteristicas": {"color": "Amarillo"},
        "stock": 2,
        "categoria": "Entrenamiento"
    },
    {
        "nombre": "Vallas de Salto (4u)",
        "caracteristicas": {"altura": "30cm", "color": "Rojo"},
        "stock": 4,
        "categoria": "Entrenamiento"
    },
    {
        "nombre": "Mini Arcos Portátiles",
        "caracteristicas": {"ancho": "1.2m"},
        "stock": 2,
        "categoria": "Entrenamiento"
    },
    {
        "nombre": "Guantes de Arquero Reusch",
        "caracteristicas": {"talla": "9", "color": "Blanco/Verde"},
        "stock": 6,
        "categoria": "Accesorios"
    },
    {
        "nombre": "Guantes de Arquero Uhlsport",
        "caracteristicas": {"talla": "10", "color": "Negro/Amarillo"},
        "stock": 5,
        "categoria": "Accesorios"
    },
    {
        "nombre": "Bolsos Deportivos Nike",
        "caracteristicas": {"color": "Negro", "capacidad": "40L"},
        "stock": 7,
        "categoria": "Accesorios"
    },
    {
        "nombre": "Cintas de Capitán",
        "caracteristicas": {"color": "Azul"},
        "stock": 10,
        "categoria": "Accesorios"
    },
    {
        "nombre": "Silbatos Fox 40",
        "caracteristicas": {"color": "Negro"},
        "stock": 15,
        "categoria": "Accesorios"
    },
    {
        "nombre": "Inflador de Balones Manual",
        "caracteristicas": {"color": "Rojo"},
        "stock": 8,
        "categoria": "Accesorios"
    },
    {
        "nombre": "Red para Arco 7x2m",
        "caracteristicas": {"color": "Blanco"},
        "stock": 3,
        "categoria": "Accesorios"
    },
    {
        "nombre": "Chalecos de Entrenamiento (10u)",
        "caracteristicas": {"color": "Verde"},
        "stock": 5,
        "categoria": "Entrenamiento"
    },
    {
        "nombre": "Cinta Marcadora de Campo",
        "caracteristicas": {"color": "Blanco"},
        "stock": 2,
        "categoria": "Accesorios"
    },
    {
        "nombre": "Bebederos Deportivos (Pack 6u)",
        "caracteristicas": {"color": "Transparente"},
        "stock": 4,
        "categoria": "Accesorios"
    },
    {
        "nombre": "Muñequeras Adidas",
        "caracteristicas": {"color": "Negro"},
        "stock": 12,
        "categoria": "Accesorios"
    },
    {
        "nombre": "Gorras Nike Running",
        "caracteristicas": {"color": "Blanco"},
        "stock": 6,
        "categoria": "Accesorios"
    },
    {
        "nombre": "Protectores Bucales Sencillos",
        "caracteristicas": {"color": "Transparente"},
        "stock": 10,
        "categoria": "Protecciones"
    },
    {
        "nombre": "Vendajes Elásticos Deportivos",
        "caracteristicas": {"color": "Beige"},
        "stock": 14,
        "categoria": "Accesorios"
    }
]

prod_col = get_product_collection(db)
for prod in productos:
    if not prod_col.find_one({"nombre": prod["nombre"]}):
        if validate_product(prod):
            prod_col.insert_one(prod)

print("Categorías y productos iniciales insertados correctamente.")
