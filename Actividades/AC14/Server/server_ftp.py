import os
import socket
import json
import pickle

def send(nombre_archivo):
    # Funcion para mandar comandos y archivos


    pass


def receive():
    # Funcion que recibe cualquier dato mandado por el servidor
    try:
        data = cliente.recv(2048)
        data_decoded = data.decode('utf-8')
        mensaje = json.loads(data_decoded)
    except AttributeError:
        print('Cliente desconectado')
    return mensaje


def get_path(path):
    abs_path = get_abs_path(path)
    if not os.path.exists(abs_path):
        return -1
    elif not os.path.isdir(abs_path):
        return 0
    else:
        return abs_path


def get_abs_path(path):
    if os.path.isabs(path):
        return path
    else:
        return os.path.abspath(os.sep.join(C_DIR.split(os.sep) +
                                           path.split(os.sep)))


if __name__ == '__main__':

    HOST = "localhost"
    PORT = 8080
    C_DIR = os.getcwd()
    client = None

    while True:
        # Conectarse al servidor
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        cliente, address = s.accept()
        connected = True
        mensaje = "conectado"
        msj_final_json = json.dumps(mensaje)
        cliente.send(msj_final_json.encode('utf-8'))

        while connected:
            # Recibir comandos
            message = receive()
            action = message[0]

            if action == "ls":
                mensaje = str(os.listdir())
                mensaje = "ls " + mensaje
                print(mensaje)
                msj_final_json = json.dumps(mensaje)
                cliente.send(msj_final_json.encode('utf-8'))
                pass

            elif action == "logout":
                cliente_nuevo, address = s.accept()
                client = cliente_nuevo
                pass

            elif action == "get":
                nombre_archivo = message[1]
                nuevo_nombre = message[2]
                if os.isfile(nombre_archivo):
                    with open(nombre_archivo, "rb") as f:
                        archivo = f.read()
                        mensaje = "get " + str(archivo) + " " + nuevo_nombre
                elif os.isdir(nombre_archivo):
                    mensaje = "get " + "El archivo corresponde a una carpeta."
                else:
                    mensaje = "get "+"El archivo no existe en el servidor."
                msj_final_json = json.dumps(mensaje)
                cliente.send(msj_final_json.encode('utf-8'))

            elif action == "send":
                nombre_nuevo = mensaje[2]
                if os.isfile(nombre_nuevo):
                    mensaje = "send "+"El archivo ya existe."
                else:
                    with open(action[2], "wb") as f:
                        f.write(bytearray(action[1]))
                        mensaje = "send "+"Archivo recibido."
                msj_final_json = json.dumps(mensaje)
                cliente.send(msj_final_json.encode('utf-8'))
