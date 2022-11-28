from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'sistemaempleados'

mysql.init_app(app)

def leer_empleados():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * FROM empleados"

    cursor.execute(sql)
    empleados = cursor.fetchall()
    conn.commit()
    return empleados


@app.route('/')
def index():
    return render_template('empleados/index.html', empleados=leer_empleados())

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=["POST"])
def store():

    _nombre = request.form['txtnom']
    _correo = request.form['txtcorreo']
    _foto = request.files['txtfoto'].filename

    
    sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"
    datos = (_nombre, _correo, _foto)

    # sql = f"INSERT INTO empleados (nombre, correo, foto) values ('{_nombre}', '{_correo}', '{_foto}');"

    conn = mysql.connect()
    cursor = conn.cursor()

    # cursor.execute(sql)

    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

