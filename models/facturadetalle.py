from utils.db import db

class Facturadetalle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_factura = db.Column(db.Integer)
    id_servicio = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    subtotal = db.Column(db.Integer)
    iva = db.Column(db.Integer)
    total = db.Column(db.Integer)   
    estado = db.Column(db.String(1)) 

    def __init__(self, id_factura, id_servicio, cantidad, subtotal, iva, total, estado):
        self.id_factura = id_factura
        self.id_servicio = id_servicio
        self.cantidad = cantidad
        self.subtotal = subtotal
        self.iva = iva
        self.total = total
        self.estado = estado
        
