# Modelos de datos para productos en MongoDB

def get_product_collection(db):
    return db['products']

def get_product_schema():
    return {
        "nombre": str,
        "caracteristicas": dict,
        "stock": int,
        "precio": dict
    }

def validate_product(data):
    schema = get_product_schema()
    for key, typ in schema.items():
        if key not in data or not isinstance(data[key], typ):
            return False
    return True