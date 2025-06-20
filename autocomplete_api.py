from flask import Blueprint, jsonify, request, current_app, session
from models import get_product_collection
from bson.objectid import ObjectId

autocomplete_api = Blueprint('autocomplete_api', __name__)

@autocomplete_api.route('/api/autocomplete/nombres')
def autocomplete_nombres():
    db = current_app.db
    q = request.args.get('q', '').strip()
    collection = get_product_collection(db)
    filtro = {'user_id': ObjectId(session['user_id'])}
    if q:
        filtro['nombre'] = {'$regex': q, '$options': 'i'}
    nombres = collection.find(filtro, {'nombre': 1, '_id': 0}).limit(10)
    return jsonify([n['nombre'] for n in nombres if 'nombre' in n])

@autocomplete_api.route('/api/autocomplete/caracteristicas')
def autocomplete_caracteristicas():
    db = current_app.db
    q = request.args.get('q', '').strip()
    collection = get_product_collection(db)
    pipeline = [
        {"$match": {"user_id": ObjectId(session['user_id'])}},
        {"$project": {"caracteristicas": {"$objectToArray": "$caracteristicas"}}},
        {"$unwind": "$caracteristicas"},
    ]
    if q:
        pipeline.append({"$match": {"$or": [
            {"caracteristicas.k": {"$regex": q, "$options": "i"}},
            {"caracteristicas.v": {"$regex": q, "$options": "i"}}
        ]}})
    pipeline.append({"$group": {"_id": {"k": "$caracteristicas.k", "v": "$caracteristicas.v"}}})
    pipeline.append({"$limit": 10})
    results = collection.aggregate(pipeline)
    return jsonify([f"{r['_id']['k']}: {r['_id']['v']}" for r in results])
