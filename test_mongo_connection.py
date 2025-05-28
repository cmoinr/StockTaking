from pymongo import MongoClient

# Cambia la URI si tu MongoDB no está en localhost o usa otro puerto
MONGO_URI = 'mongodb://localhost:27017/'

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    # Intenta obtener información del servidor
    info = client.server_info()
    print('Conexión exitosa a MongoDB!')
    print('Versión del servidor:', info['version'])
except Exception as e:
    print('No se pudo conectar a MongoDB:')
    print(e)
