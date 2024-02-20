from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="contraseña123",
    database="mydb"
)

@app.route("/")
def Index():
    cur = mydb.cursor()
    cur.execute('SELECT * FROM datos_empleados')
    datos = cur.fetchall()
    cur.close()

    cur = mydb.cursor()
    cur.execute('SELECT * FROM productos')
    datos2 = cur.fetchall()
    cur.close()
    
    cur = mydb.cursor()
    cur.execute('SELECT * FROM ventas')
    datos3 = cur.fetchall()
    cur.close()

    return render_template('index.html', contactos=datos, articulos=datos2, ventas=datos3)

@app.route('/add_empleados', methods=['POST'])
def add_empleados():
    if request.method == 'POST':
        idempleados = request.form['id']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        correo = request.form['correo']
        cur = mydb.cursor()
        cur.execute('INSERT INTO datos_empleados (idempleados, nombre, telefono, correo) VALUES (%s, %s, %s, %s)',
                    (idempleados, nombre, telefono, correo))
        mydb.commit()
        return redirect(url_for('Index'))
    
@app.route('/add_productos', methods=['POST'])
def add_productos():
    if request.method == 'POST':
        idproductos = request.form['idproducto']
        articulo = request.form['articulo']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        cur = mydb.cursor()
        cur.execute('INSERT INTO productos (idproductos, articulo, cantidad, precio) VALUES (%s, %s, %s, %s)',
                    (idproductos, articulo, cantidad, precio))
        mydb.commit()
        return redirect(url_for('Index'))
    
@app.route('/add_ventas', methods=['POST'])
def add_ventas():
    if request.method == 'POST':
        idventas = request.form['idventas']
        tipoventa = request.form['tipoventa']
        idempleados = request.form['idempleados']
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
        vproductos = request.form['vproductos']
        cur = mydb.cursor()
        cur.execute('INSERT INTO ventas (idventas, tipo_venta, fecha , productos, datos_empleados_idempleados) VALUES (%s ,%s, %s, %s, %s)',
                    (idventas, tipoventa,idempleados, fecha ,vproductos))
        mydb.commit()
        return redirect(url_for('Index'))
    
@app.route('/borrar_contacto/<string:id>')
def borrar_contacto(id):
    cur = mydb.cursor()
    cur.execute('DELETE FROM datos_empleados WHERE idempleados = {0}'.format(id))
    mydb.commit()
    return redirect(url_for('Index'))

@app.route('/borrar_articulos/<string:id>')
def borrar_productos(id):
    cur = mydb.cursor()
    cur.execute('DELETE FROM productos WHERE idproductos = {0}'.format(id))
    mydb.commit()
    return redirect(url_for('Index'))

@app.route('/borrar_ventas/<string:id>')
def borrar_ventas(id):
    cur = mydb.cursor()
    cur.execute('DELETE FROM ventas WHERE idventas = {0}'.format(id))
    mydb.commit()
    return redirect(url_for('Index'))

@app.route('/editar_empleados/<string:id>')
def editar_empleados(id):
    cur = mydb.cursor()
    cur.execute('SELECT * FROM datos_empleados WHERE idempleados = %s', (id,))
    datose = cur.fetchall()
    return render_template('editar_empleados.html', contacto=datose[0])

@app.route('/actualizar_empleados/<string:id>', methods=['POST'])
def actualizar_empleados(id):
    if request.method == 'POST':
        idempleados = request.form['id']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        correo = request.form['correo']
        cur = mydb.cursor()
        cur.execute(""" 
            UPDATE datos_empleados
            SET idempleados = %s,
                nombre = %s,
                telefono = %s,
                correo = %s
            WHERE idempleados = %s
                    """, (idempleados, nombre, telefono, correo, id))
        mydb.commit()
    return redirect(url_for('Index'))

@app.route('/editar_articulos/<string:id>')
def editar_articulo(id):
    cur = mydb.cursor()
    cur.execute('SELECT * FROM productos WHERE idproductos = %s', (id,))
    datosp = cur.fetchall()
    return render_template('editar_articulo.html', articulos=datosp[0])

@app.route('/actualizar_articulo/<string:id>', methods=['POST'])
def actualizar_articulo(id):
    if request.method == 'POST':
        idprodutos = request.form['idproducto']
        articulo = request.form['articulo']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        cur = mydb.cursor()
        cur.execute(""" 
            UPDATE productos
            SET idproductos = %s,
                articulo = %s,
                cantidad = %s,
                precio = %s
            WHERE idproductos = %s
                    """, (idprodutos, articulo, cantidad, precio, id))
        mydb.commit()
    return redirect(url_for('Index'))

@app.route('/editar_ventas/<string:id>')
def editar_ventas(id):
    cur = mydb.cursor()
    cur.execute('SELECT * FROM ventas WHERE idventas = %s', (id,))
    datosp = cur.fetchall()
    return render_template('editar_venta.html', venta=datosp[0])

@app.route('/actualizar_venta/<string:id>', methods=['POST'])
def actualizar_venta(id):
    if request.method == 'POST':
        idventas = request.form['idventas']
        tipo = request.form['tipo']
        idempleados = request.form['idempleados']
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
        productos = request.form['productos']
        cur = mydb.cursor()
        cur.execute(""" 
    UPDATE ventas
    SET idventas = %s,
        tipo_venta = %s,
        fecha = %s,
        productos = %s
        datos_empleados_idempleados = %s,
    WHERE idventas = %s
            """, (idventas, tipo, idempleados, fecha, productos, id))
        mydb.commit()
    return redirect(url_for('Index'))
