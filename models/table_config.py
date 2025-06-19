from bson.objectid import ObjectId

def get_table_config_collection(db):
    return db['user_table_config']

def get_default_column_order():
    return ["nombre", "categoria", "caracteristicas", "stock", "precio", "imagen"]

def get_table_config_for_user(db, user_id):
    col = get_table_config_collection(db)
    config = col.find_one({"user_id": ObjectId(user_id)})
    if not config:
        # Si no existe, crear config por defecto
        config = {
            "user_id": ObjectId(user_id),
            "column_order": get_default_column_order(),
            "custom_columns": []
        }
        col.insert_one(config)
    return config

def update_table_config_for_user(db, user_id, column_order, custom_columns):
    col = get_table_config_collection(db)
    col.update_one(
        {"user_id": ObjectId(user_id)},
        {"$set": {"column_order": column_order, "custom_columns": custom_columns}},
        upsert=True
    )
