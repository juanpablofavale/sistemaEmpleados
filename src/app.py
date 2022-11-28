from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'sistemaempleados'

UPLOADS = os.path.join('src/uploads')
app.config['UPLOADS']=UPLOADS

mysql.init_app(app)

def leer_empleados():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * FROM empleados"

    cursor.execute(sql)
    empleados = cursor.fetchall()
    conn.commit()
    return empleados

def borrar_foto(foto):
        os.remove(os.path.join(app.config['UPLOADS'], foto))

@app.route('/')
def index():
    return render_template('empleados/index.html', empleados=leer_empleados(), empleado=[])

@app.route('/store', methods=["POST"])
def store():

    _nombre = request.form['txtnom']
    _correo = request.form['txtcorreo']
    _foto = request.files['txtfoto']

    if _foto.filename != '':
        hoy = datetime.now()
        tiempo = hoy.strftime('%Y%H%M%S')
        nuevoNombreFoto = tiempo + ' ' + _foto.filename
        _foto.save('src/uploads/' + nuevoNombreFoto)

    sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"
    datos = (_nombre, _correo, nuevoNombreFoto)

    # sql = f"INSERT INTO empleados (nombre, correo, foto) values ('{_nombre}', '{_correo}', '{_foto}');"

    conn = mysql.connect()
    cursor = conn.cursor()

    # cursor.execute(sql)

    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):

    conn = mysql.connect()
    cursor = conn.cursor()
    
    sql = f"SELECT foto FROM empleados WHERE id={id}"
    cursor.execute(sql)

    nombre_foto = cursor.fetchone()[0]
    borrar_foto(nombre_foto)


    sql = 'DELETE FROM empleados WHERE id=%s'
    cursor.execute(sql, id)
    conn.commit()
    return redirect('/')

@app.route('/modify/<int:id>')
def modify(id):
    sql=f"SELECT * FROM empleados WHERE id={id}"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleado = cursor.fetchone()
    conn.commit()

    return render_template('empleados/index.html', empleados=leer_empleados(), empleado=empleado)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtnom']
    _correo = request.form['txtcorreo']
    _foto = request.files['txtfoto']
    id = request.form['txtid']

    conn = mysql.connect()
    cursor = conn.cursor()

    if _foto.filename != '':
        hoy = datetime.now()
        tiempo = hoy.strftime('%Y%H%M%S')
        nuevoNombreFoto = tiempo + ' ' + _foto.filename
        _foto.save('src/uploads/' + nuevoNombreFoto)

        sql = f"SELECT foto FROM empleados WHERE id={id}"
        cursor.execute(sql)

        nombre_foto = cursor.fetchone()[0]
        borrar_foto(nombre_foto)

        sql = f'UPDATE empleados SET foto="{nuevoNombreFoto}" WHERE id={id}'
        cursor.execute(sql)
        conn.commit()


    sql = f'UPDATE empleados SET nombre="{_nombre}", correo="{_correo}" WHERE id={id}'
    cursor.execute(sql)
    conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)