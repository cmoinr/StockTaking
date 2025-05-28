from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from models import get_product_collection, validate_product
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para flash messages y sesiones
app.config['MONGO_URI'] = 'mongodb://localhost:27017/stock_db'

mongo_client = MongoClient(app.config['MONGO_URI'])
db = mongo_client.get_database()

@app.route('/')
def index():
    products = list(get_product_collection(db).find())
    return render_template('index.html', products=products)

@app.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'caracteristicas': {},
            'stock': int(request.form['stock'])
        }
        for key in request.form:
            if key.startswith('car_'):
                data['caracteristicas'][key[4:]] = request.form[key]
        if validate_product(data):
            get_product_collection(db).insert_one(data)
            flash('Producto agregado exitosamente.')
            return redirect(url_for('index'))
        else:
            flash('Datos inválidos.')
    return render_template('nuevo_producto.html')

@app.route('/producto/<id>/editar', methods=['GET', 'POST'])
def editar_producto(id):
    collection = get_product_collection(db)
    producto = collection.find_one({'_id': ObjectId(id)})
    if not producto:
        flash('Producto no encontrado.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        update = {
            'nombre': request.form['nombre'],
            'caracteristicas': {},
            'stock': int(request.form['stock'])
        }
        for key in request.form:
            if key.startswith('car_'):
                update['caracteristicas'][key[4:]] = request.form[key]
        if validate_product(update):
            collection.update_one({'_id': ObjectId(id)}, {'$set': update})
            flash('Producto actualizado.')
            return redirect(url_for('index'))
        else:
            flash('Datos inválidos.')
    return render_template('editar_producto.html', producto=producto)

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
    productos = list(collection.find({'nombre': {'$regex': query, '$options': 'i'}}))
    return render_template('buscar_producto.html', productos=productos, query=query)

@app.route('/producto/busqueda_avanzada1')
def busqueda_avanzada1():
    caracteristica = request.args.get('caracteristica')
    valor = request.args.get('valor')
    collection = get_product_collection(db)
    productos = list(collection.find({f'caracteristicas.{caracteristica}': valor}))
    return render_template('busqueda_avanzada1.html', productos=productos, caracteristica=caracteristica, valor=valor)

@app.route('/producto/busqueda_avanzada2')
def busqueda_avanzada2():
    min_stock = int(request.args.get('min', 0))
    max_stock = int(request.args.get('max', 999999))
    collection = get_product_collection(db)
    productos = list(collection.find({'stock': {'$gte': min_stock, '$lte': max_stock}}))
    return render_template('busqueda_avanzada2.html', productos=productos, min_stock=min_stock, max_stock=max_stock)

if __name__ == '__main__':
    app.run(debug=True)
