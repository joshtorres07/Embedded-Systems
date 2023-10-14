from datetime import datetime
import serial
import time
import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

# Inicializa la conexión serie en el puerto COM3
arduino = serial.Serial("COM6", 9600)

@app.route('/', methods=["GET", "POST"])
def home():
    msg = ""
    if request.method == 'POST':
        if request.form.get('Led') == 'Led':
            print('*** Led ***')
            msg = "Encendido/Apagado de Led"
            serialLed()
        elif request.form.get('Leer') == 'Leer':
            print('*** Leer ***')
            msg = serialRead()
        elif request.form.get('Grabar') == 'Grabar':
            print('*** Grabar ***')
            msg = "Datos grabados"
            writeBD()
        return render_template('home.html', msg=msg)
    elif request.method == 'GET':
        return render_template('home.html', msg=msg)

def serialLed():
    time.sleep(1)
    arduino.write(b'1')

def serialRead():
    arduino.write(b'2')
    time.sleep(1)
    datos = arduino.readline()
    cadena = str(datos, 'utf-8')
    print(datos)
    return cadena

def writeBD():
    grados = serialRead()

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="sensores"
    )
    mycursor = mydb.cursor()
    fh = datetime.now()
    sql = "INSERT INTO temperatura (fh, grados) VALUES (%s, %s)"
    val = (fh, grados)
    mycursor.execute(sql, val)
    mydb.commit()

if __name__ == '__main__':
    try:
        app.run(port=5000)
    except KeyboardInterrupt:
        arduino.close()
