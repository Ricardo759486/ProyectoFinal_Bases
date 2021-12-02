from utils.db import db

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_atencion = db.Column(db.String(10))
    id_pago = db.Column(db.Integer)
    id_usuario = db.Column(db.Integer)   
    estado = db.Column(db.String(1)) 

    def __init__(self, fecha_atencion, id_pago, id_usuario, estado):
        self.fecha_atencion = fecha_atencion
        self.id_pago = id_pago
        self.id_usuario = id_usuario
        self.estado = estado
        

