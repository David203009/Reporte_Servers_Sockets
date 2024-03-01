import socket
import shutil
import psutil
from datetime import datetime 

#declara los servidores que se va a usar
servers = ["LA PAZ", "COCHABAMBA", "PANDO", "BENI", "SANTA CRUZ", "TARIJA", "CHUQUISACA", "ORURO", "POTOSI"]

#obtiene el espacio y lo devuelve en un String separado por |
def obtener_datos_espacio():
    #obtiene los datos
    total, usado, libre = shutil.disk_usage('/')
    ram = psutil.virtual_memory()
    
    ram = ram.total / (1024**3)
    
    #Los convierte de bits a GB
    total = total / (2**30)
    usado = usado / (2**30)
    libre = libre / (2**30)

    ip_address = get_ip_address()

    ahora = datetime.now()
    hora_actual = ahora.strftime("%Y-%m-%d %H:%M:%S")

    return f"{total:.2f}|{usado:.2f}|{libre:.2f}|{ram:.2f}|{ip_address}|{hora_actual}"


def get_ip_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

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
    NAME_SERVER = servers[0]
    #ejecuta el socket
    enviar_datos(HOST, PORT, NAME_SERVER)


