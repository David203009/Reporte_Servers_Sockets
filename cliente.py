import socket
import threading
from flask import Flask, render_template_string

app = Flask(__name__)

#lista de servidores por defecto
deps = ["LA PAZ", "COCHABAMBA", "PANDO", "BENI", "SANTA CRUZ", "TARIJA", "CHUQUISACA", "ORURO", "POTOSI"]

#data_recive es un object {"dep": "No disponible"} para cada departamento
data_recive = {server: "No disponible" for server in deps}

#instancia variables para hacer su calculo de la suma de todos los servidores
#sacando el total global
Total, Usado, Libre = 0,0,0

#variable para almacenar los totales en formato "totalG|usadoG|libreG"
totales = ""

#calcula el total sumando los espacios de los servidores disponibles
def calc_totales(items):
    global Total, Usado, Libre
    Total, Usado, Libre = 0,0,0
    for x,y in items.items():
        if y != "No disponible":
            tot, us, li, *args = y.split(',')
            Total += float(tot)
            Usado += float(us)
            Libre += float(li)
    return f"{Total:.2f}|{Usado:.2f}|{Libre:.2f}"

#inicia el socket y recibe datos
def listen_data(host, port):
    global data_recive, totales

    #inicia el socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()

        while True:
            #conn contiene los datos
            conn, addr = sock.accept()
            print(addr)

            with conn:
                datos = conn.recv(1024).decode('utf-8')
                #separa los datos recibidos del server
                total, usado, libre, name_serv = datos.split('|')
                #rellena con los datos que se envio de su correspondiente servidor
                data_recive[name_serv] = f"{total},{usado},{libre}"
                #almacena los totales
                totales = calc_totales(data_recive)

#Una ruta para levantar la pagina web con flask
@app.route('/')
def index():

    #separa los totales globales en un array para usar 
    tots = totales.split('|') if totales != "" else [0,0,0]

    all_data = data_recive

    #se necesita los departamentos para filtrar en el front posibles servidores no registrados entre los 9
    global deps
    deps = deps

    print(all_data)

    return render_template_string("""

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
            <title>Info Space</title>
        </head>
        <body class="container">
            <div>

                <div class="h1 text-center p-3">
                    Distritos
                </div>
                <div class="d-flex justify-content-center">
                    <div class="p-2 mx-2">Total {{ tots[0] }} GB</div>
                    <div class="p-2 mx-2">Usado {{ tots[1] }} GB</div>
                    <div class="p-2 mx-2">Libre {{ tots[2] }} GB</div>
                </div>

                <div class="d-flex justify-content-around flex-wrap mt-5">
                    {% for name, data in all_data.items() %}
                        {% if name in deps %}
                            <div class="bg-primary text-center m-2 p-3">
                                <h2>{{ name }}</h2>
                                <p>Imagen</p>
                                <p>{{ "Total: {}, usado: {}, libre: {}".format(*data.split(',')) if data != "No disponible" else "No Disponible" }}</p>
                                <p>porcentaje</p>
                            </div>     
                        {% endif %}
                    {% endfor %}
                    {% for name, data in all_data.items() %}
                        {% if not name in deps %}
                            <div class="bg-primary text-center m-2 p-3">
                                <h2>{{ name }}</h2>
                                <p>Imagen</p>
                                <p>{{ "Total: {}, usado: {}, libre: {}".format(*data.split(',')) if data != "No disponible" else "No Disponible" }}</p>
                                <p>porcentaje</p>
                            </div>     
                        {% endif %}
                    {% endfor %}
                </div>
            </div>
            
        </body>
        </html>

""", tots=tots, all_data=all_data, deps=deps)


if __name__ == "__main__":
    PORT = 18000
    HOST = '0.0.0.0'
    #necesita hilos para poder escuchar diferentes servidores
    threading.Thread(target=lambda: listen_data(HOST, PORT)).start()
    #inicia la pagina web
    app.run()

