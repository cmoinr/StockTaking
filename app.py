from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from models import get_product_collection, validate_product, get_category_collection
from bson.objectid import ObjectId
import os
import requests
from gcs_utils import upload_file_to_gcs, delete_file_from_gcs

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para flash messages y sesiones
# Usar variable de entorno para la URI de MongoDB
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/stock_db')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB máximo
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

mongo_client = MongoClient(app.config['MONGO_URI'], server_api=ServerApi('1'))
db = mongo_client.get_database('stock_db')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            'categoria': request.form.get('car_categoria'),
            'precio': {
                '$': float(request.form.get('precio_$', 0)),
                'bs': float(request.form.get('precio_bs', 0))
            }
        }
        # Procesar características dinámicas
        for key in request.form:
            if key.startswith('car_nombre_'):
                idx = key.split('_')[-1]
                nombre = request.form.get(f'car_nombre_{idx}', '').strip()
                valor = request.form.get(f'car_valor_{idx}', '').strip()
                if nombre and valor:
                    data['caracteristicas'][nombre] = valor
        # Procesar imagen
        imagen = request.files.get('imagen')
        if imagen and allowed_file(imagen.filename):
            # Subir a GCS y guardar la URL pública
            public_url = upload_file_to_gcs(imagen)
            data['imagen'] = public_url
        else:
            data['imagen'] = None
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
            'categoria': request.form.get('car_categoria'),
            'precio': {
                '$': float(request.form.get('precio_$', 0)),
                'bs': float(request.form.get('precio_bs', 0))
            }
        }
        # Procesar características dinámicas correctamente (tantas como existan)
        car_nombres = [k for k in request.form if k.startswith('car_nombre_')]
        for key in car_nombres:
            idx = key.split('_')[-1]
            nombre = request.form.get(f'car_nombre_{idx}', '').strip()
            valor = request.form.get(f'car_valor_{idx}', '').strip()
            if nombre and valor:
                update['caracteristicas'][nombre] = valor
        # Procesar imagen (opcional)
        imagen = request.files.get('imagen')
        eliminar_imagen = request.form.get('eliminar_imagen') == '1'
        imagen_anterior = producto.get('imagen')
        if eliminar_imagen and imagen_anterior:
            # Eliminar archivo en GCS si existe
            if imagen_anterior:
                # Extraer filename del URL
                from urllib.parse import urlparse
                parsed = urlparse(imagen_anterior)
                filename = os.path.basename(parsed.path)
                delete_file_from_gcs(filename)
            update['imagen'] = None
        elif imagen and allowed_file(imagen.filename):
            # Subir nueva imagen a GCS
            public_url = upload_file_to_gcs(imagen)
            update['imagen'] = public_url
            # Si sube nueva imagen y había una anterior, eliminar la anterior
            if imagen_anterior:
                from urllib.parse import urlparse
                parsed = urlparse(imagen_anterior)
                filename = os.path.basename(parsed.path)
                delete_file_from_gcs(filename)
        else:
            # Si no se sube nueva imagen ni se elimina, mantener la anterior
            update['imagen'] = None if eliminar_imagen else producto.get('imagen')
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


@app.route('/tasa_cambio')
def tasa_cambio():
    # Nueva implementación usando la API https://ve.dolarapi.com/v1/dolares/oficial
    try:
        resp = requests.get("https://ve.dolarapi.com/v1/dolares/oficial", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            tasa = data.get('promedio')
            if tasa:
                print(f"Tasa de cambio obtenida de dolarapi.com: {tasa}")
                return jsonify({"tasa": tasa, "fuente": "dolarapi.com"})
            else:
                print("No se encontró el campo 'precio' en la respuesta de la API")
                return jsonify({"error": "No se encontró el campo 'precio' en la respuesta de la API"}), 500
        else:
            print(f"Error en la respuesta de la API: status {resp.status_code}")
            return jsonify({"error": f"Error en la respuesta de la API: status {resp.status_code}"}), 500
    except Exception as e:
        print(f"Error al obtener la tasa de dolarapi.com: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)