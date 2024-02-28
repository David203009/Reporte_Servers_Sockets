import socket
import shutil

servers = ["LA PAZ", "COCHABAMBA", "PANDO", "BENI", "SANTA CRUZ", "TARIJA", "CHUQUISACA", "ORURO", "POTOSI"]

def obtener_datos_espacio():
    total, usado, libre = shutil.disk_usage('/')
    total = total / (2**30)
    usado = usado / (2**30)
    libre = libre / (2**30)
    return f"{total:.2f}|{usado:.2f}|{libre:.2f}"


def enviar_datos(host, port, name_server):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            info_pc = obtener_datos_espacio()
            message = f"{info_pc}|{name_server}"
            sock.sendall(message.encode('utf-8'))
            print(message)
    except Exception as e:
        print(f"Error al enviar datos: {e}")


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 18000
    NAME_SERVER = servers[1]
    enviar_datos(HOST, PORT, NAME_SERVER)


