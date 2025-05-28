# Definición de esquemas y utilidades para la colección de movimientos de stock

def get_stock_movement_schema():
    return {
        "producto_id": str,  # ID del producto
        "tipo": str,        # 'entrada' o 'salida'
        "cantidad": int,    # Cantidad movida
        "fecha": str,       # Fecha del movimiento (ISO 8601)
        "descripcion": str  # Descripción opcional
    }

def validate_stock_movement(data):
    schema = get_stock_movement_schema()
    for key, typ in schema.items():
        if key not in data or not isinstance(data[key], typ):
            return False
    return True

def get_stock_movement_collection(db):
    return db['stock_movements']
