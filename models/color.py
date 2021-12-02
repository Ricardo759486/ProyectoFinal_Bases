from utils.db import db

class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    estado = db.Column(db.String(1))

    def __init__(self, nombre, estado):
        self.nombre = nombre
        self.estado = estado 

