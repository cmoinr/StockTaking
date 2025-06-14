from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = current_app.db
        users_col = db['users']
        if users_col.find_one({'email': email}):
            flash('El email ya está registrado.')
            return redirect(url_for('auth.register'))
        user = User.create(username, email, password)
        users_col.insert_one({
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash
        })
        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = current_app.db
        users_col = db['users']
        user_doc = users_col.find_one({'email': email})
        if user_doc:
            user = User(user_doc['username'], user_doc['email'], user_doc['password_hash'])
            if user.check_password(password):
                session['user_email'] = user.email
                session['user_id'] = str(user_doc['_id'])
                flash('Inicio de sesión exitoso.')
                return redirect(url_for('index'))
        flash('Credenciales incorrectas.')
        return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('Sesión cerrada.')
    return redirect(url_for('auth.login'))
