from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# url_for se usa para direccionar directamente a una funcion sin usar el route
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

def queryMySql(query, data=()):
    conn = mysql.connect()
    cursor = conn.cursor()
    if len(data)>0:
        cursor.execute(query, data)
    else:
        cursor.execute(query)

    conn.commit()
    return cursor

def leer_empleados():
    return queryMySql("SELECT * FROM empleados")

def borrar_foto(foto):
    try:
        os.remove(os.path.join(app.config['UPLOADS'], foto))
    except:
        pass

@app.route('/imagenes/<path:nombre_foto>')
def uploads(nombre_foto):
    return send_from_directory(os.path.join('uploads'), nombre_foto)

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
    queryMySql(sql, datos)

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):

    cursor = queryMySql("SELECT foto FROM empleados WHERE id='%s'", (id,))

    nombre_foto = cursor.fetchone()[0]
    borrar_foto(nombre_foto)

    queryMySql("DELETE FROM empleados WHERE id='%s'", (id,))

    return redirect('/')

@app.route('/modify/<int:id>')
def modify(id):

    cursor = queryMySql("SELECT * FROM empleados WHERE id='%s'", (id,))
    empleado = cursor.fetchone()
    
    return render_template('empleados/index.html', empleados=leer_empleados(), empleado=empleado)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtnom']
    _correo = request.form['txtcorreo']
    _foto = request.files['txtfoto']
    id = request.form['txtid']

    if _foto.filename != '':
        hoy = datetime.now()
        tiempo = hoy.strftime('%Y%H%M%S')
        nuevoNombreFoto = tiempo + ' ' + _foto.filename
        _foto.save('src/uploads/' + nuevoNombreFoto)

        cursor = queryMySql("SELECT foto FROM empleados WHERE id=%s", (id,))
        nombre_foto = cursor.fetchone()[0]
        borrar_foto(nombre_foto)

        sql = 'UPDATE empleados SET foto=%s WHERE id=%s'
        queryMySql(sql, (nuevoNombreFoto, (id,)))


    sql = 'UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s'
    data=(_nombre, _correo, id)
    queryMySql(sql, data)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)