from flask import Flask, render_template , request, redirect, url_for, flash
from getpass import getpass
from mysql.connector import connect, Error
import mysql.connector



app = Flask(__name__)

try:
    with connect(
        host='127.0.0.1', 
        port=3306,
        user= input('usuario: '),
        password=getpass('la contraseña es: '),
        database='API',   
     ) as connection:
        print(connection)
except Error as e:
    print (e)

@app.route("/")
def Index():
    base = mysql.connector.connect(database="api")
    cur = base.connect.cursor()
    cur.execute('SELECT * FROM datos_empleados')
    datos = cur.fetchall()
    return render_template('index.html', contactos = datos)

@app.route('/add_empleados', methods=['POST'])
def add_empleados():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        correo = request.form['correo']
        cur = connection.cursor()
        cur.execute('INSET INTO datos_empleados (nombre, telefono correo) VALUES (%s, %s ,%s)',
                    (nombre, telefono, correo))
        connection.commit()
        return redirect(url_for('Index'))