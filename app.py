from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mail import Mail, Message
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from models import get_product_collection, validate_product
from models.category import get_category_collection, validate_category
from models.user import User
from models.table_config import get_table_config_for_user, update_table_config_for_user
from bson.objectid import ObjectId
from gcs_utils import upload_file_to_gcs, delete_file_from_gcs
from compress_utils import compress_image
from PIL import UnidentifiedImageError
from uuid import uuid4
from autocomplete_api import autocomplete_api
from auth import auth_bp
from login_required import login_required
import requests
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para flash messages y sesiones
# Usar variable de entorno para la URI de MongoDB
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/stock_db')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB máximo
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])
mail = Mail(app)

mongo_client = MongoClient(app.config['MONGO_URI'], server_api=ServerApi('1'))
db = mongo_client.get_database('stock_db')
app.register_blueprint(autocomplete_api)
app.register_blueprint(auth_bp)
app.db = db


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@login_required
def index():
    user_id = session['user_id']
    products = list(get_product_collection(db).find({'user_id': ObjectId(user_id)}))
    config = get_table_config_for_user(db, user_id)
    return render_template(
        'index.html',
        products=products,
        column_config=config,
        show_categorias=True,
        show_nuevo_producto=True,
        show_buscar_producto=True
    )


@app.route('/producto/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    categorias = list(get_category_collection(db).find({'user_id': ObjectId(session['user_id'])}))
    config = get_table_config_for_user(db, session['user_id'])
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'caracteristicas': {},
            'stock': int(request.form['stock']),
            'categoria': request.form.get('car_categoria'),
            'precio': {
                '$': float(request.form.get('precio_$', 0)),
                'bs': float(request.form.get('precio_bs', 0))
            },
            'user_id': ObjectId(session['user_id'])
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
            try:
                # Generar un nombre único para la imagen usando uuid4 y mantener la extensión original
                ext = imagen.filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid4().hex}.{ext}"
                comprimida = compress_image(imagen)
                comprimida.filename = unique_filename
                public_url = upload_file_to_gcs(comprimida, force_jpeg=True)
                data['imagen'] = public_url
            except UnidentifiedImageError:
                flash('La imagen subida no es válida o está corrupta.')
                return render_template('nuevo_producto.html', categorias=categorias, show_categorias=True, show_nuevo_producto=True, show_buscar_producto=True)
            except Exception as e:
                flash(f'Error al procesar la imagen: {str(e)}')
                return render_template('nuevo_producto.html', categorias=categorias, show_categorias=True, show_nuevo_producto=True, show_buscar_producto=True)
        else:
            data['imagen'] = None

        for col in config['custom_columns']:
            field = f"custom_{col['name']}"
            value = request.form.get(field)
            if col['type'] == 'number' and value:
                try:
                    value = float(value)
                except ValueError:
                    value = None
            data[col['name']] = value

        if validate_product(data):
            get_product_collection(db).insert_one(data)
            flash('Producto agregado exitosamente.')
            return redirect(url_for('index'))
        else:
            flash('Datos inválidos.')
    return render_template('nuevo_producto.html', categorias=categorias, column_config=config, show_categorias=True, show_nuevo_producto=True, show_buscar_producto=True)


@app.route('/producto/<id>/editar', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    from urllib.parse import urlparse
    collection = get_product_collection(db)
    producto = collection.find_one({'_id': ObjectId(id)})
    categorias = list(get_category_collection(db).find({'user_id': ObjectId(session['user_id'])}))
    config = get_table_config_for_user(db, session['user_id'])
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
            },
            'user_id': ObjectId(session['user_id'])
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
        if imagen and allowed_file(imagen.filename):            
            # Eliminar la imagen anterior si existe
            if imagen_anterior:                    
                try:
                    parsed = urlparse(imagen_anterior)
                    filename = os.path.basename(parsed.path)
                    delete_file_from_gcs(filename)            
                except Exception as e:
                    update['imagen'] = None
                    print(f'Eliminacion forzada de la imagen: {str(e)}')
            try:        
                # Generar un nombre único para la imagen usando uuid4 y mantener la extensión original
                ext = imagen.filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid4().hex}.{ext}"
                comprimida = compress_image(imagen)
                comprimida.filename = unique_filename
                public_url = upload_file_to_gcs(comprimida, force_jpeg=True)
                update['imagen'] = public_url
            except UnidentifiedImageError:
                flash('La imagen subida no es válida o está corrupta.')
                return render_template('editar_producto.html', producto=producto, categorias=categorias, show_categorias=True, show_nuevo_producto=True, show_buscar_producto=True)
            except Exception as e:
                flash(f'Error al procesar la imagen: {str(e)}')
                return render_template('editar_producto.html', producto=producto, categorias=categorias, show_categorias=True, show_nuevo_producto=True, show_buscar_producto=True)
        elif eliminar_imagen and imagen_anterior:
            try:
                parsed = urlparse(imagen_anterior)
                filename = os.path.basename(parsed.path)
                delete_file_from_gcs(filename)            
            except Exception as e:
                update['imagen'] = None
                print(f'Eliminacion forzada de la imagen: {str(e)}')            
        else:
            update['imagen'] = producto.get('imagen')

        for col in config['custom_columns']:
            field = f"custom_{col['name']}"
            value = request.form.get(field)
            if col['type'] == 'number' and value:
                try:
                    value = float(value)
                except ValueError:
                    value = None
            update[col['name']] = value

        if validate_product(update):
            collection.update_one({'_id': ObjectId(id)}, {'$set': update})
            flash('Producto actualizado.')
            return redirect(url_for('index'))
        else:
            flash('Datos inválidos.')
    return render_template('editar_producto.html', producto=producto, categorias=categorias, column_config=config, show_categorias=True, show_nuevo_producto=True, show_buscar_producto=True)


@app.route('/producto/<id>/eliminar', methods=['POST'])
@login_required
def eliminar_producto(id):
    collection = get_product_collection(db)
    collection.delete_one({'_id': ObjectId(id)})
    flash('Producto eliminado.')
    return redirect(url_for('index'))


@app.route('/categorias', methods=['GET', 'POST'])
@login_required
def categorias():
    collection = get_category_collection(db)
    if request.method == 'POST':
        categorias = collection.find({'user_id': ObjectId(session['user_id'])})
        for c in categorias:
            cid = str(c['_id'])
            nombre = request.form.get(f'nombre_{cid}')
            descripcion = request.form.get(f'descripcion_{cid}')
            eliminar = request.form.get(f'eliminar_{cid}')
            if eliminar == '1':
                collection.delete_one({'_id': ObjectId(cid), 'user_id': ObjectId(session['user_id'])})
            else:
                if nombre is not None:
                    collection.update_one(
                        {'_id': ObjectId(cid), 'user_id': ObjectId(session['user_id'])},
                        {'$set': {'nombre': nombre, 'descripcion': descripcion}}
                    )
        # Nueva categoría
        nombre_nueva = request.form.get('nombre_nueva')
        descripcion_nueva = request.form.get('descripcion_nueva')
        if nombre_nueva:
            data = {'nombre': nombre_nueva, 'descripcion': descripcion_nueva or '', 'user_id': ObjectId(session['user_id'])}
            if validate_category(data):
                collection.insert_one(data)
        return redirect(url_for('categorias'))
    # GET: mostrar categorías
    categorias = list(collection.find({'user_id': ObjectId(session['user_id'])}))
    return render_template('categorias.html', categorias=categorias, show_categorias=True, show_nuevo_producto=True, show_buscar_producto=True)


@app.route('/tasa_dolar', methods=['GET'])
@login_required
def tasa_dolar():
    return render_template('tasa_dolar.html', show_categorias=True, show_nuevo_producto=True, show_buscar_producto=True)


@app.route('/api/productos')
@login_required
def api_productos():
    productos = list(get_product_collection(db).find({'user_id': ObjectId(session['user_id'])}))
    # Solo enviar nombre y precio en la respuesta
    return jsonify([
        {
            'nombre': p.get('nombre'),
            'precio': p.get('precio', {})
        } for p in productos
    ])


@app.route('/actualizar_precios', methods=['POST'])
@login_required
def actualizar_precios():
    data = request.get_json()
    tasa = data.get('tasa')
    resp = requests.get("https://ve.dolarapi.com/v1/dolares", timeout=5)
    if resp.status_code != 200:
        flash('No se pudo obtener la tasa de cambio.', 'error')
        return jsonify({'success': False, 'error': 'No se pudo obtener la tasa'}), 500
    tasas = resp.json()
    oficial = next((d for d in tasas if d.get('fuente') == 'oficial'), None)
    paralelo = next((d for d in tasas if d.get('fuente') == 'paralelo'), None)
    if not oficial or not paralelo:
        flash('No se encontraron tasas válidas.', 'error')
        return jsonify({'success': False, 'error': 'No se encontraron tasas válidas'}), 500
    if tasa == 'oficial':
        tasa_valor = float(oficial.get('promedio'))
    elif tasa == 'paralelo':
        tasa_valor = float(paralelo.get('promedio'))
    else:
        tasa_valor = (float(oficial.get('promedio')) + float(paralelo.get('promedio'))) / 2
    collection = get_product_collection(db)
    productos = collection.find({'user_id': ObjectId(session['user_id'])})
    for p in productos:
        precio_usd = p.get('precio', {}).get('$', 0)
        try:
            precio_usd = float(precio_usd)
        except:
            precio_usd = 0
        nuevo_bs = round(precio_usd * tasa_valor, 2)
        collection.update_one({'_id': p['_id'], 'user_id': ObjectId(session['user_id'])}, {'$set': {'precio.bs': nuevo_bs}})
    flash('Precios actualizados correctamente.', 'success')
    return jsonify({'success': True, 'redirect': url_for('index')})


@app.route('/producto/buscar')
@login_required
def buscar_producto():
    # Recoge todos los posibles filtros
    query = request.args.get('q', '').strip()
    filtro_tipo = request.args.get('filtro_tipo', '')
    caracteristica = request.args.get('caracteristica', '').strip()
    valor_caracteristica = request.args.get('valor_caracteristica', '').strip()
    stock_comp = request.args.get('stock_comp', '')
    stock_valor = request.args.get('stock_valor', '')
    precio_comp = request.args.get('precio_comp', '')
    precio_valor = request.args.get('precio_valor', '')
    precio_moneda = request.args.get('precio_moneda', '')

    collection = get_product_collection(db)
    filtro = {}
    if query:
        filtro['nombre'] = {'$regex': query, '$options': 'i'}
    if filtro_tipo == 'caracteristica' and caracteristica and valor_caracteristica:
        filtro[f'caracteristicas.{caracteristica}'] = valor_caracteristica
    if filtro_tipo == 'stock' and stock_comp and stock_valor:
        try:
            stock_valor = int(stock_valor)
            if stock_comp == 'gt':
                filtro['stock'] = {'$gt': stock_valor}
            elif stock_comp == 'lt':
                filtro['stock'] = {'$lt': stock_valor}
            elif stock_comp == 'eq':
                filtro['stock'] = stock_valor
        except ValueError:
            pass
    if filtro_tipo == 'precio' and precio_comp and precio_valor and precio_moneda:
        try:
            precio_valor = float(precio_valor)
            key = f'precio.{precio_moneda}'
            if precio_comp == 'gt':
                filtro[key] = {'$gt': precio_valor}
            elif precio_comp == 'lt':
                filtro[key] = {'$lt': precio_valor}
            elif precio_comp == 'eq':
                filtro[key] = precio_valor
        except ValueError:
            pass
    filtro['user_id'] = ObjectId(session['user_id'])
    products = list(collection.find(filtro))
    # Si es AJAX, devolver JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        for p in products:
            p['_id'] = str(p['_id'])
            p['user_id'] = str(p['user_id'])
        return jsonify(products)
    return render_template('buscar_producto.html', products=products, query=query, show_categorias=True, show_nuevo_producto=True, show_buscar_producto=True)


@app.route('/tasa_cambio', methods=['GET'])
@login_required
def tasa_cambio():
    """
    Devuelve la tasa de cambio actual (oficial y paralelo) desde la API https://ve.dolarapi.com/v1/dolares
    """
    try:
        resp = requests.get("https://ve.dolarapi.com/v1/dolares", timeout=5)
        if resp.status_code != 200:
            return jsonify({'success': False, 'error': 'No se pudo obtener la tasa de cambio.'}), 500
        tasas = resp.json()
        oficial = next((d for d in tasas if d.get('fuente') == 'oficial'), None)
        paralelo = next((d for d in tasas if d.get('fuente') == 'paralelo'), None)
        if not oficial or not paralelo:
            return jsonify({'success': False, 'error': 'No se encontraron tasas válidas.'}), 500
        return jsonify({
            'success': True,
            'oficial': {
                'promedio': float(oficial.get('promedio')),
                'fecha': oficial.get('fechaActualizacion')
            },
            'paralelo': {
                'promedio': float(paralelo.get('promedio')),
                'fecha': paralelo.get('fechaActualizacion')
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/dashboard')
@login_required
def dashboard():
    db = app.db
    users_col = db['users']
    user_doc = users_col.find_one({'email': session['user_email']})
    if not user_doc:
        flash('Usuario no encontrado.')
        return redirect(url_for('index'))
    # Pasar el documento completo del usuario al template
    return render_template('dashboard.html', user=user_doc)


@app.route('/configurar_columnas', methods=['GET', 'POST'])
@login_required
def configurar_columnas():
    user_id = session['user_id']
    config = get_table_config_for_user(db, user_id)
    if request.method == 'POST':
        # Recibe el nuevo orden y columnas personalizadas
        column_order = request.form.getlist('column_order')
        custom_names = request.form.getlist('custom_name')
        custom_types = request.form.getlist('custom_type')
        custom_columns = [
            {"name": n, "type": t}
            for n, t in zip(custom_names, custom_types) if n.strip()
        ]
        update_table_config_for_user(db, user_id, column_order, custom_columns)
        # Agregar el campo a los productos existentes si es nuevo
        prod_col = get_product_collection(db)
        for col in custom_columns:
            prod_col.update_many(
                {"user_id": ObjectId(user_id), col["name"]: {"$exists": False}},
                {"$set": {col["name"]: None}}
            )
        flash('Configuración de columnas actualizada.')
        return redirect(url_for('configurar_columnas'))
    return render_template('configurar_columnas.html', config=config)