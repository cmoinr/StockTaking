from bson.objectid import ObjectId
from datetime import datetime
import pytz

# Zona horaria de Venezuela (Caracas)
CARACAS_TZ = pytz.timezone('America/Caracas')

def create_venta(user_id, items, total, cliente=None, metodo_pago=None):
    return {
        'user_id': ObjectId(user_id),
        'fecha': datetime.now(CARACAS_TZ),
        'items': items,  # lista de dicts: [{producto_id, nombre, cantidad, precio_unitario, subtotal}]
        'total': total,
        'cliente': cliente,  # dict opcional: {'nombre':..., 'telefono':..., 'email':...}
        'metodo_pago': metodo_pago  # string opcional
    }

# Ejemplo de item:
# {
#   'producto_id': ObjectId(...),
#   'nombre': 'Zapato',
#   'cantidad': 2,
#   'precio_unitario': 10.0,
#   'subtotal': 20.0
# }
