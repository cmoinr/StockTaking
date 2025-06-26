from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from flask_mail import Message
from models.user import User
from login_required import login_required
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
import random
import string
import re

auth_bp = Blueprint('auth', __name__)

def send_verification_email(email, code):
    mail = current_app.extensions.get('mail')
    msg = Message('StockTaking | Código de verificación de tu cuenta',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[email])
    msg.body = f"""
        Hola,
        Gracias por registrarte en StockTaking. Para completar tu registro, por favor verifica tu cuenta
        Tu código de verificación es: {code}
        Por favor, ingrésalo en la página de verificación para completar tu registro.
    """
    mail.send(msg)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        db = current_app.db
        users_col = db['users']
        if users_col.find_one({'email': email}):
            flash('El email ya está registrado.', 'error')
            return redirect(url_for('auth.register'))
        # Validación de email
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(email_regex, email):
            flash('El correo electrónico no es válido.', 'error')
            return redirect(url_for('auth.register'))
        # Validación de teléfono Venezuela (+58 o 04xx)
        phone_regex = r"^(\+58|58|0)(4\d{2})(\d{7})$"
        if not re.match(phone_regex, phone):
            flash('El teléfono debe ser venezolano y válido (ej: +584121234567 o 04121234567).', 'error')
            return redirect(url_for('auth.register'))
        # Generar código de verificación único (6 dígitos)
        verification_code = ''.join(random.choices(string.digits, k=6))
        user = User.create(email, password)
        users_col.insert_one({
            'first_name': first_name,
            'last_name': last_name,
            'email': user.email,
            'phone': phone,
            'password_hash': user.password_hash,
            'is_verified': False,
            'verification_code': verification_code
        })
        send_verification_email(email, verification_code)
        flash('Registro exitoso. Revisa tu correo para verificar tu cuenta.', 'success')
        return redirect(url_for('auth.verify_email', email=email))
    return render_template('register.html')


@auth_bp.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    email = request.args.get('email') or request.form.get('email')
    if request.method == 'POST':
        code = request.form['code']
        db = current_app.db
        users_col = db['users']
        user = users_col.find_one({'email': email})
        if user and user.get('verification_code') == code:
            users_col.update_one({'email': email}, {'$set': {'is_verified': True}, '$unset': {'verification_code': ''}})
            if 'user_email' in session:
                flash('Cuenta verificada correctamente.', 'success')             
                return redirect(url_for('dashboard'))
            else:
                flash('Cuenta verificada correctamente. Ahora puedes iniciar sesión.', 'success')
                return redirect(url_for('auth.login'))
        else:
            flash('Código incorrecto. Intenta nuevamente.', 'error')
    else:
        verification_code = ''.join(random.choices(string.digits, k=6))
        db = current_app.db
        users_col = db['users']
        users_col.update_one({'email': email}, {'$set': {'verification_code': verification_code}})
        if not email:
            flash('Por favor, proporciona un correo electrónico para verificar.', 'warning')
        else:
            send_verification_email(email, verification_code)
        return render_template('verify_email.html', email=email)
    return render_template('verify_email.html', email=email)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = current_app.db
        users_col = db['users']
        user_doc = users_col.find_one({'email': email})
        if user_doc:
            user = User(user_doc['email'], user_doc['password_hash'])
            if user.check_password(password):
                session['user_email'] = user.email
                session['user_id'] = str(user_doc['_id'])
                flash('Inicio de sesión exitoso.', 'success')
                return redirect(url_for('user_home'))
        flash('Credenciales incorrectas.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/contact_edit', methods=['GET', 'POST'])
def contact_edit():
    db = current_app.db
    users_col = db['users']
    user_doc = users_col.find_one({'email': session['user_email']})
    if not user_doc:
        flash('Usuario no encontrado.', 'error')
        return redirect(url_for('contact_info'))
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        # Validación de email
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(email_regex, email):
            flash('El correo electrónico no es válido.', 'error')
            return render_template('contact_edit.html', user=user_doc)
        # Validación de teléfono Venezuela (+58 o 04xx)
        phone_regex = r"^(\+58|58|0)(4\d{2})(\d{7})$"
        if not re.match(phone_regex, phone):
            flash('El teléfono debe ser venezolano y válido (ej: +584121234567 o 04121234567).', 'error')
            return render_template('contact_edit.html', user=user_doc)
        # Verificar si el email ya existe en otro usuario
        if email != user_doc['email'] and users_col.find_one({'email': email}):
            flash('El email ya está registrado por otro usuario.', 'error')
            return render_template('contact_edit.html', user=user_doc)
        users_col.update_one({'_id': user_doc['_id']}, {'$set': {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone
        }})
        session['user_email'] = email
        flash('Información actualizada correctamente.', 'success')
        return redirect(url_for('contact_info'))
    return render_template('contact_edit.html', user=user_doc)


@auth_bp.route('/cambiar_contrasena', methods=['GET', 'POST'])
@login_required
def cambiar_contrasena():
    db = current_app.db
    user_id = session.get('user_id')
    users_col = db['users']
    user_doc = users_col.find_one({'_id': ObjectId(user_id)})
    if request.method == 'POST':
        actual = request.form['actual']
        nueva = request.form['nueva']
        confirmar = request.form['confirmar']
        if nueva != confirmar:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('cambiar_contrasena.html')
        # Crear instancia de User a partir del documento de MongoDB
        user = User.from_document(user_doc)
        if not user.check_password(actual):
            flash('Contraseña actual incorrecta.', 'error')
            return render_template('cambiar_contrasena.html')
        # Generar hash de la nueva contraseña
        nueva_password_hash = generate_password_hash(nueva)
        users_col.update_one({'_id': ObjectId(user_id)}, {'$set': {'password_hash': nueva_password_hash}})
        flash('Contraseña cambiada exitosamente.', 'success')
        return redirect(url_for('user_home'))
    return render_template('cambiar_contrasena.html')
