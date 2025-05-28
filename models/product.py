# Este archivo define los modelos de datos para productos en MongoDB

def get_product_collection(db):
    return db['products']

def get_product_schema():
    return {
        "nombre": str,  # Nombre del producto
        "caracteristicas": dict,  # Características como color, peso, etc.
        "stock": int  # Cantidad existente
    }

def validate_product(data):
    schema = get_product_schema()
    for key, typ in schema.items():
        if key not in data or not isinstance(data[key], typ):
            return False
    return True

# Ejemplo de documento de producto:
# {
#   "nombre": "Producto X",
#   "caracteristicas": {"color": "rojo", "peso": "1kg"},
#   "stock": 10
# }
