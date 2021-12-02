from utils.db import db

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    valor = db.Column(db.Integer)
    descripcion = db.Column(db.String(50))  
    estado = db.Column(db.String(1))

    def __init__(self, nombre, valor, descripcion, estado):
        self.nombre = nombre
        self.valor = valor
        self.descripcion = descripcion
        self.estado = estado
        