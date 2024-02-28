import socket
import shutil

#declara los servidores que se va a usar
servers = ["LA PAZ", "COCHABAMBA", "PANDO", "BENI", "SANTA CRUZ", "TARIJA", "CHUQUISACA", "ORURO", "POTOSI"]

#obtiene el espacio y lo devuelve en un String separado por |
def obtener_datos_espacio():
    #obtiene los datos
    total, usado, libre = shutil.disk_usage('/')
    
    #Los convierte de bits a GB
    total = total / (2**30)
    usado = usado / (2**30)
    libre = libre / (2**30)
    return f"{total:.2f}|{usado:.2f}|{libre:.2f}"

#declaracion des socket y enviado de datos
def enviar_datos(host, port, name_server):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            #conecta al socket con el host y el puerto
            sock.connect((host, port))
            #obtiene los datos
            #info_pc es un string "total|usado|libre"
            info_pc = obtener_datos_espacio()
            #message es un string "total|usado|libre|name_server"
            message = f"{info_pc}|{name_server}"
            sock.sendall(message.encode('utf-8'))
            print(message)
    except Exception as e:
        print(f"Error al enviar datos: {e}")

#inicia el script
if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 18000
    NAME_SERVER = "Argentina"
    #ejecuta el socket
    enviar_datos(HOST, PORT, NAME_SERVER)


