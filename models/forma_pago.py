from utils.db import db

class forma_pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipodepago = db.Column(db.String(50))
    estado = db.Column(db.String(1))

    def __init__(self, tipodepago, estado):
        self.tipodepago = tipodepago
        self.estado = estado 

