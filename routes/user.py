from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import Usuario
from utils.db import db

users = Blueprint('users', __name__)

@users.route("/")
def index():
    listaUsuario = Usuario.query.all()
    return render_template('index.html', listaUsuario = listaUsuario)

@users.route("/single-blog")
def singleblog():
    return render_template('single-blog.html')

@users.route('/new', methods=['POST'])
def add_user():
    user = request.form['usuario']
    contraseña = request.form['contraseña']
    identificacion = request.form['identificacion']
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    telefono = request.form['telefono']
    correo = request.form['correo']
    direccion = request.form['direccion']
    id_rol = request.form['id_rol']
    estado = request.form['estado']

    new_usuario = Usuario(user,contraseña,identificacion,nombres,apellidos,telefono,correo,direccion,id_rol,estado)

    db.session.add(new_usuario)
    db.session.commit()
    flash("Usuario creado correctamente")
    return redirect(url_for('users.index'))

@users.route('/update/<id>', methods=['POST','GET'])
def update_user(id):
    usuario = Usuario.query.get(id)

    if request.method == 'POST':
        usuario.usuario = request.form['usuario']
        usuario.contrasenia = request.form['contraseña']
        usuario.identificacion = request.form['identificacion']
        usuario.nombres = request.form['nombres']
        usuario.apellidos = request.form['apellidos']
        usuario.telefono = request.form['telefono']
        usuario.correo = request.form['correo']
        usuario.direccion = request.form['direccion']
        usuario.id_rol = request.form['id_rol']
        usuario.estado = request.form['estado']

        db.session.commit()
        flash("Usuario actualizado correctamente")
        return redirect(url_for('users.index'))

    return render_template('update.html', usuario = usuario)

@users.route('/delete/<id>')
def delete_user(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario eliminado correctamente")
    return redirect(url_for('users.index'))

@users.route('/about')
def about():
    return render_template('about.html')