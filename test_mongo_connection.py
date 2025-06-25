from pymongo import MongoClient
import os

# Cambia la URI si tu MongoDB no está en localhost o usa otro puerto
MONGO_URI = os.environ.get('MONGO_URI')

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    # Intenta obtener información del servidor
    info = client.server_info()
    print('Conexión exitosa a MongoDB!')
    print('Versión del servidor:', info['version'])
except Exception as e:
    print('No se pudo conectar a MongoDB:')
    print(e)
