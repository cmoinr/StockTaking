from flask import Blueprint, request, session, redirect, url_for, flash, current_app, render_template
from bson.objectid import ObjectId
from models.venta import create_venta
import pytz

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/ventas/nueva', methods=['GET', 'POST'])
def nueva_venta():
    db = current_app.db
    productos_col = db['products']
    ventas_col = db['ventas']
    user_id = session['user_id']
    if request.method == 'POST':
        items = []
        total = float(request.form.get('total', 0))
        for p in productos_col.find({'user_id': ObjectId(user_id), 'stock': {'$gt': 0}}):
            agregar = request.form.get(f'agregar_{p["_id"]}')
            cantidad = int(request.form.get(f'cantidad_{p["_id"]}', 0))
            if agregar and cantidad > 0:
                precio_unitario = p['precio']['$'] if 'precio' in p and '$' in p['precio'] else 0
                subtotal = cantidad * precio_unitario
                if cantidad > p['stock']:
                    flash(f"Stock insuficiente para {p['nombre']}", 'error')
                    return redirect(url_for('ventas.nueva_venta'))
                items.append({
                    'producto_id': p['_id'],
                    'nombre': p['nombre'],
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'subtotal': subtotal
                })
        if not items:
            flash('Debes seleccionar al menos un producto y cantidad.', 'error')
            return redirect(url_for('ventas.nueva_venta'))
        cliente = {
            'nombre': request.form.get('cliente_nombre'),
            'telefono': request.form.get('cliente_telefono'),
            'email': request.form.get('cliente_email')
        } if request.form.get('cliente_nombre') else None
        metodo_pago = request.form.get('metodo_pago')
        # Descontar stock
        for item in items:
            productos_col.update_one({'_id': ObjectId(item['producto_id'])}, {'$inc': {'stock': -item['cantidad']}})
        # Guardar venta
        venta_doc = create_venta(user_id, items, total, cliente, metodo_pago)
        ventas_col.insert_one(venta_doc)
        flash('Venta registrada exitosamente.', 'success')
        return redirect(url_for('ventas.listar_ventas'))
    # GET: mostrar formulario
    productos = list(productos_col.find({'user_id': ObjectId(user_id), 'stock': {'$gt': 0}}))
    for p in productos:
        p['_id'] = str(p['_id'])
        p['user_id'] = str(p['user_id'])
    return render_template(
        'nueva_venta.html', 
        productos=productos,

        show_tasa_cambio=False,
        show_categorias=False,
        show_nuevo_producto=False,
        show_buscar_producto=False,
        show_dashboard=False,

        show_tasa_ventas=True,
        show_nueva_venta=True    
    )


@ventas_bp.route('/ventas')
def listar_ventas():
    db = current_app.db
    ventas_col = db['ventas']
    user_id = session['user_id']
    ventas_cursor = ventas_col.find({'user_id': ObjectId(user_id)}).sort('fecha', -1)
    ventas = list(ventas_cursor)
    caracas_tz = pytz.timezone('America/Caracas')
    for v in ventas:
        fecha = v.get('fecha')
        if fecha:
            if fecha.tzinfo is None:
                # Asume UTC si es naive
                fecha = pytz.utc.localize(fecha)
            v['fecha'] = fecha.astimezone(caracas_tz)
    return render_template(
        'ventas.html',
        ventas=ventas,

        show_tasa_cambio=False,
        show_categorias=False,
        show_nuevo_producto=False,
        show_buscar_producto=False,
        show_dashboard=False,

        show_tasa_ventas=True,
        show_nueva_venta=True    
    )


@ventas_bp.route('/tasa_dolar_ventas', methods=['GET'])
def tasa_dolar_ventas():
    return render_template(
        'tasa_dolar_ventas.html',
        show_tasa_cambio=False,
        show_categorias=False,
        show_nuevo_producto=False,
        show_buscar_producto=False,
        show_dashboard=False,

        show_tasa_ventas=True,
        show_nueva_venta=True
    )
