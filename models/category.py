# Definición de esquemas y utilidades para la colección de categorías

def get_category_schema():
    return {
        "nombre": str,  # Nombre de la categoría
        "descripcion": str  # Descripción opcional
    }

def validate_category(data):
    schema = get_category_schema()
    for key, typ in schema.items():
        if key not in data or not isinstance(data[key], typ):
            return False
    return True

def get_category_collection(db):
    return db['categories']
