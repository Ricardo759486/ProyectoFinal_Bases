from flask import Blueprint, render_template, request
from models.user import usuario
from utils.db import db

users = Blueprint('users', __name__)

@users.route("/")
def home():
    return render_template('index.html')

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

    new_usuario = usuario(user,contraseña,identificacion,nombres,apellidos,telefono,correo,direccion,id_rol,estado)

    db.session.add(new_usuario)
    db.session.commit()

    print(new_usuario)

    return "saving a user"

@users.route('/update')
def update_user():
    return "update a user"

@users.route('/delete')
def delete_user():
    return "delete a user"
    
@users.route('/about')
def about():
    return render_template('about.html')