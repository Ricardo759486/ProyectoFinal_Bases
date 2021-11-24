from utils.db import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasenia = db.Column(db.String(50))
    identificacion = db.Column(db.String(11)) 
    nombres = db.Column(db.String(50))         
    apellidos = db.Column(db.String(50)) 
    telefono = db.Column(db.String(10)) 
    correo = db.Column(db.String(50)) 
    direccion = db.Column(db.String(50)) 
    id_rol = db.Column(db.Integer)  
    estado = db.Column(db.String(1)) 

    def __init__(self, usuario, contraseña, identificacion, nombres, apellidos, telefono, correo,direccion, id_rol, estado):
        self.usuario = usuario
        self.contrasenia = contraseña
        self.identificacion = identificacion
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.id_rol = id_rol
        self.estado = estado 

