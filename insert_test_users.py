from pymongo import MongoClient
from bson.objectid import ObjectId

# Conexión a la base de datos local
client = MongoClient('mongodb://localhost:27017/')
db = client['stock_db']
users_col = db['users']

# Usuarios de prueba
usuarios = [
    {
        '_id': ObjectId('684df1c9049b0ea71d0178ce'),
        'username': 'cmoinr',
        'email': 'cmoinr@hotmail.com',
        'password_hash': 'scrypt:32768:8:1$FR0tmHeViFtn2Tjc$947786857fb10dcb33f7f0d3d38f0bb2005a52a3ed4e84d2e7e6444d8436cceefbd760c0f38c65e62c0596a49ac7c562ac97d281770022c2cd4a89ab48ffeeaa'
    },
    {
        '_id': ObjectId('684e017a6ed1f852fc5b03ad'),
        'username': 'aneki',
        'email': 'aneki@gmail.com',
        'password_hash': 'scrypt:32768:8:1$afArewrKmxK9CRXu$b7d2030b3d8ca72ec1b9329d57a45e4d8b4ca7fafa62449bd4c61eb71426ebb5a511fd40d5538aed7b51cc647253c1458fa827c29666f8e40331c8b6119cd5ca'
    }
]

for user in usuarios:
    if not users_col.find_one({'_id': user['_id']}):
        users_col.insert_one(user)
        print(f"Usuario {user['username']} insertado.")
    else:
        print(f"Usuario {user['username']} ya existe.")
