from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.scaffold import F
from models.mascota import Mascota
from models.servicio import Servicio
from models.user import Usuario
from models.especie import Especie
from models.raza import Raza
from models.color import Color
from models.factura import Factura
from models.forma_pago import forma_pago
from models.rol import Rol
from models.facturadetalle import Facturadetalle
import MySQLdb
import hashlib
from utils.db import db
from datetime import datetime
from config import userdb, passworddb, hostdb, databasedb

proy = Blueprint('proy', __name__)

@proy.route("/")
def index():
    return render_template('index.html')

@proy.route('/new', methods=['POST'])
def add_user():

    try:
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        identificacion = request.form['identificacion']
        user = request.form['usuario']
        contraseña = request.form['contraseña']
        telefono = request.form['telefono']
        correo = request.form['correo']
        direccion = request.form['direccion']

        if nombres != "" and apellidos != "" and identificacion != "" and user != "" and contraseña != "" and telefono != "" and correo != "" and direccion != "" and int(identificacion) > 0 and int(telefono) > 0 and len(user) <= 50 and len(contraseña) <= 50 and len(identificacion) <= 11 and len(nombres) <= 50 and len(apellidos) <= 50 and len(telefono) <= 10 and len(correo) <= 50 and len(direccion) <= 50:

            id_rol = 1
            estado = "A"
            clave = contraseña.encode('utf-8')
            cifrado = hashlib.sha1(clave).hexdigest()
            new_usuario = Usuario(user,cifrado,identificacion,nombres,apellidos,telefono,correo,direccion,id_rol,estado)

            db.session.add(new_usuario)
            db.session.commit()
            #flash("Usuario creado correctamente")
            return redirect(url_for('proy.index')) 
        else:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return redirect(url_for('proy.index'))

    except:
        flash("Datos no permitidos, por favor revise la información nuevamente.")
        return redirect(url_for('proy.index'))

@proy.route('/usuario/<id>', methods=['POST','GET'])
def ir(id):
    usuario = Usuario.query.get(id)
    db=MySQLdb.connect(host=hostdb,user=userdb, passwd=passworddb,db=databasedb)
    cursor=db.cursor()
    cursor.execute('select j.id, j.nombre , r.nombre, c.nombre, p.nombre, j.anio_nacimiento, j.peso from mascota j, especie r, raza c , color p where j.id_usuario = '+ str(id) +' and j.id_especie = r.id and j.id_raza = c.id and j.id_color = p.id and j.estado = "A";')
    registro = cursor.fetchall()
    cursor.execute('select j.id_factura, sum(j.cantidad), sum(j.subtotal), sum(j.iva), sum(j.total), u.nombres, r.fecha_atencion from usuario u, facturadetalle j, factura r where j.id_factura = r.id and r.id_usuario = 1 and j.estado = "A" group by j.id_factura; ')
    listafacturas = cursor.fetchall()
    listaEspecie = Especie.query.all()
    listaRaza = Raza.query.all()
    listaColor = Color.query.all()
    listaServicios = Servicio.query.all()
    db.close()
    return render_template('usuario.html', listaUsuario = usuario, listaMascotas = registro, listaEspecie = listaEspecie, listaRaza = listaRaza, listaColor = listaColor, listaServicios = listaServicios, listafacturas = listafacturas)

@proy.route('/usuario', methods=['POST','GET'])
def login():

    try:
        user = request.form['usuario']
        contraseña = request.form['contraseña']
        clave = contraseña.encode('utf-8')
        cifrado = hashlib.sha1(clave).hexdigest()
        db=MySQLdb.connect(host=hostdb,user=userdb, passwd=passworddb,db=databasedb)
        cursor=db.cursor()
        cursor.execute('select id, id_rol from usuario where usuario = "' + user + '" and contrasenia = "' + cifrado + '";')
        registro = cursor.fetchone()

        if len(registro) > 0:
            
            if registro[1] == 1:
                db.close()
                return redirect(url_for('proy.ir', id =registro[0]))
            elif registro[1] == 2:
                db.close()
                return redirect(url_for('proy.irVeterinario', id =registro[0]))
            elif registro[1] == 3:
                db.close()
                return redirect(url_for('proy.irAdministrador', id =registro[0]))

        else:
            db.close()
            return redirect(url_for('proy.index'))
    
    except:
        return redirect(url_for('proy.index'))


@proy.route('/addpet/<id>', methods=['POST','GET'])
def add_pet(id):

    try:
        nombres = request.form['nombre']
        id_especie = request.form['especie']
        id_raza = request.form['raza']
        id_color = request.form['color']
        anio_nacimiento = request.form['nacimiento']
        peso = request.form['peso']
        id_usuario = id
        estado = "A"

        if nombres != "" and int(peso) > 0 and len(nombres) <= 50 and len(peso) <= 2:
            new_mascota = Mascota(nombres,id_especie,id_raza,id_color,anio_nacimiento,peso,id_usuario,estado)
            db.session.add(new_mascota)
            db.session.commit()
            flash("Mascota Agregada")
            return redirect(url_for('proy.ir', id =id))
        else:
            flash("No se ha podido agregar la mascota, por favor verifica la información ingresada.")
            return redirect(url_for('proy.ir', id =id))

    except:
        flash("No se ha podido agregar la mascota, por favor verifica la información ingresada.")
        return redirect(url_for('proy.ir', id =id))
    
        

@proy.route('/updatepet/<id>/<con>/<idActual>', methods=['POST','GET'])
def update_pet(id, con, idActual):
    mascota = Mascota.query.get(id)
    if request.method == 'POST':

        try:
            nombre = request.form['nombre']
            id_especie = request.form['especie']
            id_raza = request.form['raza']
            id_color = request.form['color']
            anio_nacimiento = request.form['nacimiento']
            peso = request.form['peso']

            if nombre != "" and id_especie != "" and id_raza != "" and id_color != "" and anio_nacimiento != "" and int(peso) > 0 and len(nombre) <= 50:
                mascota.nombre = request.form['nombre']
                mascota.id_especie = request.form['especie']
                mascota.id_raza = request.form['raza']
                mascota.id_color = request.form['color']
                mascota.anio_nacimiento = request.form['nacimiento']
                mascota.peso = request.form['peso']

                db.session.commit()

                if con == "1":
                    return redirect(url_for('proy.ir', id =idActual))    
                elif con == "2":
                    return redirect(url_for('proy.irVeterinario', id = idActual))
                elif con == "3":
                    return redirect(url_for('proy.irAdministrador', id = idActual))
        
            else:
                listaEspecie = Especie.query.all()
                listaRaza = Raza.query.all()
                listaColor = Color.query.all()
                db2=MySQLdb.connect(host=hostdb,user=userdb, passwd=passworddb,db=databasedb)
                cursor=db2.cursor()
                cursor.execute('select r.nombre, c.nombre, p.nombre from mascota j, especie r, raza c , color p where j.id_usuario = '+ str(mascota.id_usuario) +' and j.id = ' + str(mascota.id) + ' and j.id_especie = r.id and j.id_raza = c.id and j.id_color = p.id and j.estado = "A";')
                registro = cursor.fetchall()
                flash("Datos no permitidos, por favor revise la información nuevamente.")
                return render_template('updateMascota.html', mascota = mascota, infomascota = registro , listaEspecie = listaEspecie, listaRaza = listaRaza, listaColor = listaColor, con = con, idActual = idActual)

        except:

            listaEspecie = Especie.query.all()
            listaRaza = Raza.query.all()
            listaColor = Color.query.all()
            db2=MySQLdb.connect(host=hostdb,user=userdb, passwd=passworddb,db=databasedb)
            cursor=db2.cursor()
            cursor.execute('select r.nombre, c.nombre, p.nombre from mascota j, especie r, raza c , color p where j.id_usuario = '+ str(mascota.id_usuario) +' and j.id = ' + str(mascota.id) + ' and j.id_especie = r.id and j.id_raza = c.id and j.id_color = p.id and j.estado = "A";')
            registro = cursor.fetchall()
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return render_template('updateMascota.html', mascota = mascota, infomascota = registro , listaEspecie = listaEspecie, listaRaza = listaRaza, listaColor = listaColor, con = con, idActual = idActual)
                
    listaEspecie = Especie.query.all()
    listaRaza = Raza.query.all()
    listaColor = Color.query.all()
    db2=MySQLdb.connect(host=hostdb,user=userdb, passwd=passworddb,db=databasedb)
    cursor=db2.cursor()
    cursor.execute('select r.nombre, c.nombre, p.nombre from mascota j, especie r, raza c , color p where j.id_usuario = '+ str(mascota.id_usuario) +' and j.id = ' + str(mascota.id) + ' and j.id_especie = r.id and j.id_raza = c.id and j.id_color = p.id and j.estado = "A";')
    registro = cursor.fetchall()

    return render_template('updateMascota.html', mascota = mascota, infomascota = registro , listaEspecie = listaEspecie, listaRaza = listaRaza, listaColor = listaColor, con = con, idActual = idActual)

@proy.route('/deletepet/<id>/<con>/<idActual>')
def delete_pet(id, con, idActual):
    mascota = Mascota.query.get(id)
    mascota.estado = "B"
    db.session.commit()
    if con == "1":
        return redirect(url_for('proy.ir', id = idActual))    
    elif con == "2":
        return redirect(url_for('proy.irVeterinario', id = idActual))
    elif con == "3":
        return redirect(url_for('proy.irAdministrador', id = idActual))
    
@proy.route('/updateUsuario/<id>/<con>/<idActual>', methods=['POST','GET'])
def update_user(id, con, idActual):
    usuario = Usuario.query.get(id)

    if request.method == 'POST':

        try:
            uusuario = request.form['usuario']
            contrasenia = request.form['contraseña']
            identificacion = request.form['identificacion']
            nombres = request.form['nombres']
            apellidos = request.form['apellidos']
            telefono = request.form['telefono']
            correo = request.form['correo']
            direccion = request.form['direccion']

            if uusuario == "" or contrasenia == "" or identificacion == "" or nombres == "" or apellidos == "" or telefono == "" or correo == "" or direccion == "" or len(uusuario) > 50 or len(contrasenia) > 50 or len(identificacion) > 11 or len(nombres) > 50 or len(apellidos) > 50 or len(telefono) > 10 or len(correo) > 50:

                flash("Datos no permitidos, por favor revise la información nuevamente.")
                return render_template('updateUsuario.html', usuario = usuario, con = con, idActual = idActual)

            else:

                usuario.usuario = request.form['usuario']
                contra = request.form['contraseña']
                clave = contra.encode('utf-8')
                cifrado = hashlib.sha1(clave).hexdigest()
                usuario.contrasenia = cifrado
                usuario.identificacion = request.form['identificacion']
                usuario.nombres = request.form['nombres']
                usuario.apellidos = request.form['apellidos']
                usuario.telefono = request.form['telefono']
                usuario.correo = request.form['correo']
                usuario.direccion = request.form['direccion']

                db.session.commit()

                if con == "1":
                    return redirect(url_for('proy.ir', id = idActual))    
                elif con == "2":
                    return redirect(url_for('proy.irVeterinario', id = idActual))
                elif con == "3":
                    return redirect(url_for('proy.irAdministrador', id = idActual))

        except:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return render_template('updateUsuario.html', usuario = usuario, con = con, idActual = idActual)

    return render_template('updateUsuario.html', usuario = usuario, con = con, idActual = idActual)


@proy.route('/veterinario/<id>', methods=['POST','GET'])
def irVeterinario(id):
    usuario = Usuario.query.get(id)
    db=MySQLdb.connect(host=hostdb,user=userdb, passwd=passworddb,db=databasedb)
    cursor=db.cursor()
    cursor.execute('select * from usuario where id_rol = 1 and estado = "A";')
    usuarios = cursor.fetchall()
    cursor=db.cursor()
    cursor.execute('select j.id, j.nombre , r.nombre, c.nombre, p.nombre, j.anio_nacimiento, j.peso, u.id, u.nombres from usuario u, mascota j, especie r, raza c , color p where j.id_especie = r.id and j.id_raza = c.id and j.id_color = p.id and j.estado = "A" and j.id_usuario = u.id;')
    registro = cursor.fetchall()
    cursor.execute('select j.id_factura, sum(j.cantidad), sum(j.subtotal), sum(j.iva), sum(j.total), u.nombres, r.fecha_atencion from usuario u, facturadetalle j, factura r where j.id_factura = r.id and r.id_usuario = u.id and j.estado = "A" group by j.id_factura;')
    listaFactura = cursor.fetchall()
    listaServicios = Servicio.query.all()
    db.close()
    return render_template('veterinario.html', listaUsuario = usuario, listaMascotas = registro, listaServicios = listaServicios, usuarios = usuarios, listaFactura = listaFactura)

@proy.route("/addPago/<id>")
def addpago(id):
    listaPagos = forma_pago.query.all()
    return render_template('formapago.html', id = id, listaPagos = listaPagos)


@proy.route('/addfactura/<id>', methods=['POST','GET'])
def add_factura(id):

    try:

        formaPago = request.form['formapago']

        if formaPago != "":
            fecha = datetime.today().strftime('%Y-%m-%d')
            estado = "A"
            listaServicios = Servicio.query.all()

            new_factura = Factura(fecha,formaPago,id,estado)
            db.session.add(new_factura)
            db.session.commit()

            return render_template('servicio.html', id = id, listaServicios = listaServicios)
        
        else:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            listaPagos = forma_pago.query.all()
            return render_template('formapago.html', id = id, listaPagos = listaPagos)


    except:
        flash("Datos no permitidos, por favor revise la información nuevamente.")
        listaPagos = forma_pago.query.all()
        return render_template('formapago.html', id = id, listaPagos = listaPagos)
    

@proy.route('/addDetalle/<id>', methods=['POST','GET'])
def add_detalle(id):

    try:
        servicio = request.form['servicio']
        cantidad = request.form['cantidad']

        if int(cantidad) > 0 or servicio != "":
            n2 = Servicio.query.get(servicio)
            n = n2.valor
            subtotal = n * int(cantidad)
            iva = 0.19 * subtotal
            total = int(iva + subtotal)
            estado = "A"
            facturas = Factura.query.all()
            idFactura = facturas[len(facturas)-1].id
            listaServicios = Servicio.query.all()
            
            new_facturaDetalle = Facturadetalle(idFactura,servicio,cantidad,subtotal,int(iva),total,estado)
            db.session.add(new_facturaDetalle)
            db.session.commit()

            return render_template('servicio.html', id = id, listaServicios = listaServicios)

        else:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            listaServicios = Servicio.query.all()
            return render_template('servicio.html', id = id, listaServicios = listaServicios)
        

    except:
        flash("Datos no permitidos, por favor revise la información nuevamente.")
        listaServicios = Servicio.query.all()
        return render_template('servicio.html', id = id, listaServicios = listaServicios)
    

@proy.route('/administrador/<id>', methods=['POST','GET'])
def irAdministrador(id):
    usuario = Usuario.query.get(id)
    db=MySQLdb.connect(host=hostdb,user=userdb, passwd=passworddb,db=databasedb)
    cursor=db.cursor()
    cursor.execute('select j.id, j.nombre , r.nombre, c.nombre, p.nombre, j.anio_nacimiento, j.peso, u.id, u.nombres from usuario u, mascota j, especie r, raza c , color p where j.id_especie = r.id and j.id_raza = c.id and j.id_color = p.id and j.estado = "A" and j.id_usuario = u.id;')
    mascotas = cursor.fetchall()
    cursor.execute('select j.id_factura, count(j.id_servicio), sum(j.subtotal), sum(j.iva), sum(j.total), u.nombres, r.fecha_atencion from usuario u, facturadetalle j, factura r where j.id_factura = r.id and r.id_usuario = u.id and j.estado = "A" group by j.id_factura;')
    listaFactura = cursor.fetchall()
    cursor.execute('select * from servicio where estado = "A";')
    listaServicios = cursor.fetchall()
    cursor.execute('select * from forma_pago where estado = "A";')
    listaPagos = cursor.fetchall()
    cursor.execute('select * from especie where estado = "A";')
    listaEspecies = cursor.fetchall()
    cursor.execute('select * from raza where estado = "A";')
    listaRaza = cursor.fetchall()
    cursor.execute('select * from color where estado = "A";')
    listaColor = cursor.fetchall()
    cursor.execute('select * from rol where estado = "A";')
    listaRol = cursor.fetchall()

    cursor.execute('select * from usuario where id_rol = 1 and estado = "A";')
    usuarios = cursor.fetchall()

    cursor.execute('select * from usuario where id_rol = 2 and estado = "A";')
    usuarios2 = cursor.fetchall()

    db.close()
    return render_template('administrador.html', listaUsuario = usuario, listaMascotas = mascotas, listaServicios = listaServicios, usuarios = usuarios, listaFactura = listaFactura, listaPagos = listaPagos,listaEspecies = listaEspecies, listarazas = listaRaza, listaColor = listaColor, listaroles = listaRol, usuarios2 = usuarios2)
    
@proy.route('/addUsers/<id>', methods=['POST'])
def add_userAdm(id):

    try:
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        identificacion = request.form['identificacion']
        user = request.form['usuario']
        contraseña = request.form['contraseña']
        telefono = request.form['telefono']
        correo = request.form['correo']
        direccion = request.form['direccion']

        if nombres == "" or apellidos == "" or identificacion == "" or user == "" or contraseña == "" or telefono == "" or correo == "" or direccion == "" or len(user) > 50 or len(contraseña) > 50 or len(identificacion) > 11 or len(nombres) > 50 or len(apellidos) > 50 or len(telefono) > 10 or len(correo) > 50 or int(telefono) <= 0 or int(identificacion) <= 0 :
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return redirect(url_for('proy.irAdministrador', id = id))
            
        else:
            id_rol = 1
            estado = "A"
            clave = contraseña.encode('utf-8')
            cifrado = hashlib.sha1(clave).hexdigest()

            new_usuario = Usuario(user,cifrado,identificacion,nombres,apellidos,telefono,correo,direccion,id_rol,estado)

            db.session.add(new_usuario)
            db.session.commit()
            #flash("Usuario creado correctamente")
            return redirect(url_for('proy.irAdministrador', id = id))
            

    except:
        flash("Datos no permitidos, por favor revise la información nuevamente.")
        return redirect(url_for('proy.irAdministrador', id = id))

@proy.route('/addEmpleados/<id>', methods=['POST'])
def add_userEmpleado(id):

    try:
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        identificacion = request.form['identificacion']
        user = request.form['usuario']
        contraseña = request.form['contraseña']
        telefono = request.form['telefono']
        correo = request.form['correo']
        direccion = request.form['direccion']

        if nombres == "" or apellidos == "" or identificacion == "" or user == "" or contraseña == "" or telefono == "" or correo == "" or direccion == "" or len(user) > 50 or len(contraseña) > 50 or len(identificacion) > 11 or len(nombres) > 50 or len(apellidos) > 50 or len(telefono) > 10 or len(correo) > 50 or int(telefono) <= 0 or int(identificacion) <= 0 :
            
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return redirect(url_for('proy.irAdministrador', id = id))
            
        else:
            id_rol = 2
            estado = "A"

            clave = contraseña.encode('utf-8')
            cifrado = hashlib.sha1(clave).hexdigest()

            new_usuario = Usuario(user,cifrado,identificacion,nombres,apellidos,telefono,correo,direccion,id_rol,estado)

            db.session.add(new_usuario)
            db.session.commit()
            #flash("Usuario creado correctamente")
            return redirect(url_for('proy.irAdministrador', id = id))

    except:
        flash("Datos no permitidos, por favor revise la información nuevamente.")
        return redirect(url_for('proy.irAdministrador', id = id))
      
    

@proy.route('/deleteUser/<id>/<con>/<idActual>')
def delete_user(id, con, idActual):
    usuario = Usuario.query.get(id)
    usuario.estado = "B"
    db.session.commit()
    if con == "1":
        return redirect(url_for('proy.ir', id = idActual))    
    elif con == "2":
        return redirect(url_for('proy.ir', id = idActual))
    elif con == "3":
        return redirect(url_for('proy.irAdministrador', id = idActual))

@proy.route('/addService/<id>', methods=['POST'])
def add_Service(id):

    try:
        nombre = request.form['nombre']
        valor = request.form['valor']
        descripcion = request.form['descripcion']

        if nombre != "" or valor != "" or descripcion != "" or int(valor) > 0:
            
            estado = "A"
            new_Servicio = Servicio(nombre,valor,descripcion,estado)

            db.session.add(new_Servicio)
            db.session.commit()
            #flash("Usuario creado correctamente")
            return redirect(url_for('proy.irAdministrador', id = id))

        else:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return redirect(url_for('proy.irAdministrador', id = id))

    except:
        flash("Datos no permitidos, por favor revise la información nuevamente.")
        return redirect(url_for('proy.irAdministrador', id = id))
    

@proy.route('/addEspecie/<id>', methods=['POST'])
def add_Especie(id):

    try:
        nombre = request.form['nombre']

        if nombre != "":
            
            estado = "A"
            new_Especie = Especie(nombre,estado)

            db.session.add(new_Especie)
            db.session.commit()
            #flash("Usuario creado correctamente")
            return redirect(url_for('proy.irAdministrador', id = id))

        else:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return redirect(url_for('proy.irAdministrador', id = id))

    except:
        flash("Datos no permitidos, por favor revise la información nuevamente.")
        return redirect(url_for('proy.irAdministrador', id = id))


@proy.route('/addRaza/<id>', methods=['POST'])
def add_Raza(id):

    try:
        nombre = request.form['nombre']

        if nombre != "":
            
            estado = "A"
            new_Raza = Raza(nombre,estado)

            db.session.add(new_Raza)
            db.session.commit()
            #flash("Usuario creado correctamente")
            return redirect(url_for('proy.irAdministrador', id = id))

        else:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return redirect(url_for('proy.irAdministrador', id = id))

    except:
        flash("Datos no permitidos, por favor revise la información nuevamente.")
        return redirect(url_for('proy.irAdministrador', id = id))
  

@proy.route('/addColor/<id>', methods=['POST'])
def add_Color(id):
    try:
        nombre = request.form['nombre']
        if nombre != "":
            estado = "A"
            new_Color = Color(nombre,estado)

            db.session.add(new_Color)
            db.session.commit()
            #flash("Usuario creado correctamente")
            return redirect(url_for('proy.irAdministrador', id = id))

        else:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return redirect(url_for('proy.irAdministrador', id = id))
            
    except:
        flash("Datos no permitidos, por favor revise la información nuevamente.")
        return redirect(url_for('proy.irAdministrador', id = id))
    

@proy.route('/addFormaPago/<id>', methods=['POST'])
def add_FormaPago(id):
    try:
        nombre = request.form['nombre']

        if nombre != "":
            estado = "A"

            new_FormaPago = forma_pago(nombre,estado)

            db.session.add(new_FormaPago)
            db.session.commit()
            #flash("Usuario creado correctamente")
            return redirect(url_for('proy.irAdministrador', id = id))

        else:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return redirect(url_for('proy.irAdministrador', id = id))
            
    except:
        flash("Datos no permitidos, por favor revise la información nuevamente.")
        return redirect(url_for('proy.irAdministrador', id = id))
    
    

@proy.route('/updateServicios/<idUsuario>/<idS>', methods=['POST','GET'])
def update_Servicio(idUsuario, idS):
    servicio = Servicio.query.get(idS)

    if request.method == 'POST':

        try:
            nombre = request.form['nombre']
            valor = request.form['valor']
            descripcion = request.form['descripcion']

            if nombre != "" or valor != "" or int(valor) > 0 or descripcion != "":

                servicio.nombre = request.form['nombre']
                servicio.valor = request.form['valor']
                servicio.descripcion = request.form['descripcion']

                db.session.commit()
                return redirect(url_for('proy.irAdministrador', id = idUsuario))

            else:
                flash("Datos no permitidos, por favor revise la información nuevamente.")
                return render_template('updateServicio.html', servicio = servicio, idUsuario = idUsuario)

        except:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return render_template('updateServicio.html', servicio = servicio, idUsuario = idUsuario)

    return render_template('updateServicio.html', servicio = servicio, idUsuario = idUsuario)

@proy.route('/updateEspecie/<idUsuario>/<idE>', methods=['POST','GET'])
def update_Especie(idUsuario, idE):
    especie = Especie.query.get(idE)

    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            if nombre != "":
                especie.nombre = request.form['nombre']
                db.session.commit()
                return redirect(url_for('proy.irAdministrador', id = idUsuario))
            else:
                flash("Datos no permitidos, por favor revise la información nuevamente.")
                return render_template('updateEspecie.html', especie = especie, idUsuario = idUsuario)
        except:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return render_template('updateEspecie.html', especie = especie, idUsuario = idUsuario)

    return render_template('updateEspecie.html', especie = especie, idUsuario = idUsuario)

@proy.route('/updateRaza/<idUsuario>/<idR>', methods=['POST','GET'])
def update_Raza(idUsuario, idR):
    raza = Raza.query.get(idR)

    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            if nombre != "":
                raza.nombre = request.form['nombre']
                db.session.commit()
                return redirect(url_for('proy.irAdministrador', id = idUsuario))
            else:
                flash("Datos no permitidos, por favor revise la información nuevamente.")
                return render_template('updateRaza.html', raza = raza, idUsuario = idUsuario)
        except:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return render_template('updateRaza.html', raza = raza, idUsuario = idUsuario)
    
    return render_template('updateRaza.html', raza = raza, idUsuario = idUsuario)

@proy.route('/updateColor/<idUsuario>/<idC>', methods=['POST','GET'])
def update_Color(idUsuario, idC):
    color = Color.query.get(idC)

    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            if nombre != "":
                color.nombre = request.form['nombre']
                db.session.commit()
                return redirect(url_for('proy.irAdministrador', id = idUsuario))
            else:
                flash("Datos no permitidos, por favor revise la información nuevamente.")
                return render_template('updateColor.html', color = color, idUsuario = idUsuario)
        except:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return render_template('updateColor.html', color = color, idUsuario = idUsuario)

    return render_template('updateColor.html', color = color, idUsuario = idUsuario)

@proy.route('/updateFormasPago/<idUsuario>/<idFP>', methods=['POST','GET'])
def update_FormaColor(idUsuario, idFP):
    formaPago = forma_pago.query.get(idFP)

    if request.method == 'POST':
        try:
            tipodepago = request.form['formapago']
            if tipodepago != "":
                formaPago.tipodepago = request.form['formapago']
                db.session.commit()
                return redirect(url_for('proy.irAdministrador', id = idUsuario))
            else:
                flash("Datos no permitidos, por favor revise la información nuevamente.")
                return render_template('updateFormaPago.html', formapago = formaPago, idUsuario = idUsuario)
        except:
            flash("Datos no permitidos, por favor revise la información nuevamente.")
            return render_template('updateFormaPago.html', formapago = formaPago, idUsuario = idUsuario)
        

    return render_template('updateFormaPago.html', formapago = formaPago, idUsuario = idUsuario)

@proy.route('/deleteServicio/<idS>/<idUsuario>')
def delete_Servicio(idS, idUsuario):
    servicio = Servicio.query.get(idS)
    servicio.estado = "B"
    db.session.commit()

    return redirect(url_for('proy.irAdministrador', id = idUsuario))

@proy.route('/deleteEspecie/<idE>/<idUsuario>')
def delete_Especie(idE, idUsuario):
    especie = Especie.query.get(idE)
    especie.estado = "B"
    db.session.commit()

    return redirect(url_for('proy.irAdministrador', id = idUsuario))

@proy.route('/deleteRaza/<idR>/<idUsuario>')
def delete_Raza(idR, idUsuario):
    raza = Raza.query.get(idR)
    raza.estado = "B"
    db.session.commit()

    return redirect(url_for('proy.irAdministrador', id = idUsuario))

@proy.route('/deleteColor/<idC>/<idUsuario>')
def delete_Color(idC, idUsuario):
    color = Color.query.get(idC)
    color.estado = "B"
    db.session.commit()

    return redirect(url_for('proy.irAdministrador', id = idUsuario))

@proy.route('/deleteFormaPago/<idFP>/<idUsuario>')
def delete_Fomapago(idFP, idUsuario):
    formapago = forma_pago.query.get(idFP)
    formapago.estado = "B"
    db.session.commit()

    return redirect(url_for('proy.irAdministrador', id = idUsuario))