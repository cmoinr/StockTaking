from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from models import get_product_collection, validate_product, get_category_collection
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para flash messages y sesiones
# Usar variable de entorno para la URI de MongoDB
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/stock_db')

mongo_client = MongoClient(app.config['MONGO_URI'], server_api=ServerApi('1'))
db = mongo_client.get_database('stock_db')

@app.route('/')
def index():
    products = list(get_product_collection(db).find())
    return render_template('index.html', products=products)


@app.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    categorias = list(get_category_collection(db).find())
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'caracteristicas': {},
            'stock': int(request.form['stock']),
            'categoria': request.form.get('car_categoria')
        }
        # Procesar características dinámicas
        for key in request.form:
            if key.startswith('car_nombre_'):
                idx = key.split('_')[-1]
                nombre = request.form.get(f'car_nombre_{idx}', '').strip()
                valor = request.form.get(f'car_valor_{idx}', '').strip()
                if nombre and valor:
                    data['caracteristicas'][nombre] = valor
        if validate_product(data):
            get_product_collection(db).insert_one(data)
            flash('Producto agregado exitosamente.')
            return redirect(url_for('index'))
        else:
            flash('Datos inválidos.')
    return render_template('nuevo_producto.html', categorias=categorias)


@app.route('/producto/<id>/editar', methods=['GET', 'POST'])
def editar_producto(id):
    collection = get_product_collection(db)
    producto = collection.find_one({'_id': ObjectId(id)})
    categorias = list(get_category_collection(db).find())
    if not producto:
        flash('Producto no encontrado.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        update = {
            'nombre': request.form['nombre'],
            'caracteristicas': {},
            'stock': int(request.form['stock']),
            'categoria': request.form.get('car_categoria')
        }
        # Procesar características dinámicas correctamente (tantas como existan)
        car_nombres = [k for k in request.form if k.startswith('car_nombre_')]
        for key in car_nombres:
            idx = key.split('_')[-1]
            nombre = request.form.get(f'car_nombre_{idx}', '').strip()
            valor = request.form.get(f'car_valor_{idx}', '').strip()
            if nombre and valor:
                update['caracteristicas'][nombre] = valor
                print(f"Agregando característica: {nombre} = {valor}")
        if validate_product(update):
            collection.update_one({'_id': ObjectId(id)}, {'$set': update})
            flash('Producto actualizado.')
            return redirect(url_for('index'))
        else:
            flash('Datos inválidos.')
    return render_template('editar_producto.html', producto=producto, categorias=categorias)


@app.route('/producto/<id>/eliminar', methods=['POST'])
def eliminar_producto(id):
    collection = get_product_collection(db)
    collection.delete_one({'_id': ObjectId(id)})
    flash('Producto eliminado.')
    return redirect(url_for('index'))


@app.route('/producto/buscar')
def buscar_producto():
    query = request.args.get('q', '')
    collection = get_product_collection(db)
    products = list(collection.find({'nombre': {'$regex': query, '$options': 'i'}}))
    return render_template('buscar_producto.html', products=products, query=query)


@app.route('/producto/busqueda_avanzada1')
def busqueda_avanzada1():
    caracteristica = request.args.get('caracteristica')
    valor = request.args.get('valor')
    collection = get_product_collection(db)
    products = list(collection.find({f'caracteristicas.{caracteristica}': valor}))
    return render_template('busqueda_avanzada1.html', products=products, caracteristica=caracteristica, valor=valor)


@app.route('/producto/busqueda_avanzada2')
def busqueda_avanzada2():
    min_stock = int(request.args.get('min', 0))
    max_stock = int(request.args.get('max', 1000))
    collection = get_product_collection(db)
    products = list(collection.find({'stock': {'$gte': min_stock, '$lte': max_stock}}))
    return render_template('busqueda_avanzada2.html', products=products, min_stock=min_stock, max_stock=max_stock)


@app.route('/caracteristicas_unicas')
def caracteristicas_unicas():
    collection = get_product_collection(db)
    # Obtener todas las claves de caracteristicas de todos los productos
    all_caracs = collection.find({}, {"caracteristicas": 1})
    car_set = set()
    for prod in all_caracs:
        caracs = prod.get("caracteristicas", {})
        for k in caracs.keys():
            car_set.add(k)
    return jsonify(sorted(list(car_set)))


@app.route('/valores_caracteristica')
def valores_caracteristica():
    caracteristica = request.args.get('caracteristica')
    if not caracteristica:
        return jsonify([])
    collection = get_product_collection(db)
    # Buscar todos los valores únicos para la característica seleccionada
    all_vals = collection.find({f"caracteristicas.{caracteristica}": {"$exists": True}}, {f"caracteristicas.{caracteristica}": 1})
    val_set = set()
    for prod in all_vals:
        caracs = prod.get("caracteristicas", {})
        val = caracs.get(caracteristica)
        if val:
            val_set.add(val)
    return jsonify(sorted(list(val_set)))


if __name__ == '__main__':
    app.run(debug=True)
