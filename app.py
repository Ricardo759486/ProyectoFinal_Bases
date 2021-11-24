from flask import Flask
from routes.user import users
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:R759486c/%)$(&@localhost/ProyectoFinal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLAlchemy(app)

app.register_blueprint(users)
