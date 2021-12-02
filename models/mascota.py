from utils.db import db

class Mascota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    id_especie = db.Column(db.Integer)
    id_raza = db.Column(db.Integer)
    id_color = db.Column(db.Integer)
    anio_nacimiento = db.Column(db.String(10))
    peso = db.Column(db.String(3))
    id_usuario = db.Column(db.Integer)   
    estado = db.Column(db.String(1)) 

    def __init__(self, nombre, id_especie, id_raza, id_color, anio_nacimiento, peso, id_usuario, estado):
        self.nombre = nombre
        self.id_especie = id_especie
        self.id_raza = id_raza
        self.id_color = id_color
        self.anio_nacimiento = anio_nacimiento
        self.peso = peso
        self.id_usuario = id_usuario
        self.estado = estado
        

