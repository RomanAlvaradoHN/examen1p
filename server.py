import socket
import threading
import os
import mariadb
import json
from Utilities import *


############################################################################
#SOCKET SERVER
############################################################################
class SocketServer:

    def __init__(self, parametros):
        self.host  = parametros["server_ip"]
        self.port  = parametros["server_port"]
        self.db    = parametros["database_conexion"]
        self.utils = parametros["utilities"]

        ############################################################################
        #PUESTA EN MARCHA DEL SOCKET SERVIDOR
        ############################################################################
        try:
            self.utils.clear_console()
            self.clients = []
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print("===============================================================")
            print(f"\n    Servidor escuchando en {self.host}:{self.port}        \n")
            print("===============================================================")
        except BaseException as errorType:
            self.utils.error_handler(errorType)


        ############################################################################
        #CONTROLADOR DE FUNCIONAMIENTO DEL SOCKET SERVEIDOR
        ############################################################################
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                m = json.loads(client_socket.recv(1024).decode("utf-8"))
                operacion = m["oper"]

                if operacion == "login":
                    print("Nuevo intento login: " + client_address[0])
                    client_thread = threading.Thread(target = self.login_controller, args=([client_socket]))
                    client_thread.start()


                elif operacion == "consultar_prestamos":
                    resp = self.db.consultar_prestamos((m["id_cliente"]))
                    client_socket.send(resp.encode("utf-8"))


                elif operacion == "consultar_pagos":
                    resp = self.db.consultar_pagos((m["id_cliente"], m["id_prestamo"]))
                    client_socket.send(resp.encode("utf-8"))


                elif operacion == "consultar_reversiones":
                    resp = self.db.consultar_reversiones((m["id_cliente"], m["id_prestamo"]))
                    client_socket.send(resp.encode("utf-8"))






                elif operacion == "registrar_pago":
                    self.db.registrar_pago((m["id_cliente"], m["id_prestamo"]))
                    client_socket.send("RESPUESTA".encode("utf-8"))


                elif operacion == "chat":
                    pass


        except BaseException as errorType:
            self.utils.error_handler(errorType)


    ############################################################################
    #CONTROLADOR DE LOGIN
    ############################################################################
    def login_controller(self, client_socket):
        while True:
            cred = json.loads(client_socket.recv(1024).decode("utf-8"))

            #print(f"str(type(cred)) \n {cred}")
            resp = self.db.validar_credenciales((cred["username"], cred["password"]))
            client_socket.send(resp.encode())

            if resp["authenticated"]: break






############################################################################
#BLOQUE DE INICIO DE SCRIPT SERVER.PY
############################################################################
if __name__ == "__main__":

    parametros = {
        "server_ip": '172.31.30.203',
        "server_port": 9999,
        "database_conexion": DatabaseConexion(),
        "utilities": Utilities()
    }

    server = SocketServer(parametros)
