import os
import socket
import sys
import json


def receive():
    try:
        data = s.recv(2048)
        data_decoded = data.decode('utf-8')
        mensaje = json.loads(data_decoded)
        mensaje = mensaje.split(" ")
        if mensaje[0] == "get":
            if len(mensaje)<3:
                mensaje = mensaje[1]
            else:
                nombre_nuevo = mensaje[2]
                with open(mensaje[2], "wb") as f:
                    f.write(bytearray(mensaje[1].encode()))
                    mensaje = "se guardo un archivo con el nombre {}".format(nombre_nuevo)
        elif mensaje[0] == "send":
            mensaje = mensaje[1]
        elif mensaje[0] == "ls":
            mensaje = mensaje[1:]
        else:
            mensaje = mensaje[0]
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

    C_DIR = os.getcwd()
    HOST = "localhost"
    PORT = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        connected = True

    except socket.error:
        print("No fue posible realizar la conexión")
        sys.exit()

    while connected:

        S_DIR = receive()
        command = input(S_DIR + " $ ")
        commands = command.split(" ")

        if command[0] == "logout":
            msj_final_json = json.dumps(commands)
            s.send(msj_final_json.encode('utf-8'))
            # Aviso al servidor que me desconecto
            connected = False

        elif commands[0] == "ls":
            # Muetra carpetas y archivos en el directorio del servidor
            msj_final_json = json.dumps(commands)
            s.send(msj_final_json.encode('utf-8'))
            pass

        elif commands[0] == "get":
            msj_final_json = json.dumps(commands)
            s.send(msj_final_json.encode('utf-8'))
            # Le pides un archivo al servidor
            pass

        elif commands[0] == "send":
            # le mandas un archivo al servidor
            file_path = get_abs_path(commands[1])
            if os.path.exists(file_path):
                with open(commands[1], "rb") as f:
                    archivo = f.read()
                    mensaje = "send " + str(archivo) + " " + commands[2]
                pass
            else:
                print(commands[1] + " doesn't exist.")
