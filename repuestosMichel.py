from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="contraseña123",
    database="api"
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
        fecha = request.form['fecha']
        vproductos = request.form['vproductos']
        cur = mydb.cursor()
        cur.execute('INSERT INTO ventas (idventas, tipo de venta, idempleados, fecha , productos) VALUES (%s ,%s, %s, %s, %s)',
                    (idventas, tipoventa, idempleados, fecha, vproductos))
        mydb.commit()
        return redirect(url_for('Index'))
