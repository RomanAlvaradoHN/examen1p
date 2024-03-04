import socket
import threading
import mariadb
import json
from Utilities import *


############################################################################
#SOCKET SERVER
############################################################################
class ServerSocket:

    #INICIO DEL SOCKET----------------------------------------------------
    def __init__(self, params):
        host = params["server_ip"]
        port = params["server_port"]
        self.db = params["database_conexion"]
        self.utils = Utilities()

        ############################################################################
        #PUESTA EN MARCHA DEL SOCKET SERVIDOR
        ############################################################################
        try:
            self.utils.clear_console()
            self.clients = []
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((host, port))
            self.server_socket.listen(5)

            #Hilo para recibir los nuevos sockets cliente---------------------------
            client_socket_thread = threading.Thread(target = self.__client_sockets_listener)
            client_socket_thread.start()

            print("====================================================================")
            print(f"\n    Servidor escuchando en {host}:{port} \n")
            print("====================================================================")
        
        except BaseException as errorType:
            self.utils.error_handler(errorType)


    
    
    
    #CONTROLADOR DE NUEVOS SOCKET CLIENTE --------------------------------
    def __client_sockets_listener(self):
        while True:
            new_socket = self.server_socket.accept()

            #Hilo para comunicacion de cada sockets cliente---------------
            client_operations_thread = threading.Thread(target = self.__operation_controller, args=[new_socket])
            client_operations_thread.start()
            

    #ORQUESTADOR DE OPERACIONES ------------------------------------------
    def __operation_controller(self, new_socket):
        client_socket, client_address = new_socket
        
        while True:
            data = json.loads(client_socket.recv(1024).decode("utf-8"))

            #OPERACIONES -----------------------------------------------------
            if data["operacion"] == "login":
                print("Nuevo intento login: " + client_address[0])
                resp = self.db.validar_credenciales((data["username"], data["password"]))
                client_socket.send(resp.encode("utf-8"))


            elif data["operacion"] == "consultar_prestamos":
                resp = self.db.consultar_prestamos((data["id_cliente"]))
                client_socket.send(resp.encode("utf-8"))


            elif data["operacion"] == "consultar_pagos":
                resp = self.db.consultar_pagos((data["id_cliente"], data["id_prestamo"]))
                client_socket.send(resp.encode("utf-8"))


            elif data["operacion"] == "consultar_reversiones":
                resp = self.db.consultar_reversiones((data["id_cliente"], data["id_prestamo"]))
                client_socket.send(resp.encode("utf-8"))


            elif data["operacion"] == "registrar_pago":
                resp = self.db.registrar_pago((data["id_cliente"], data["id_prestamo"]))
                client_socket.send(resp.encode("utf-8"))


            elif data["operacion"] == "chat":
                pass


    
    
    
    
    
    
    
    
    ############################################################################
    #CONTROLADOR DE CHAT
    ############################################################################
    def __handle_client(self, client_socket):

        #Añadimos el nuevo participante a la lista
        self.clients.append({"name": client_name, "socket": client_socket})
        print("\n\nNueva conexión de {}:{}".format(client_address[0], client_address[1]))
        print("Participante: {}".format(client_name))
        print("====================")
        client_thread = threading.Thread(target = self.__handle_client, args=(client_socket,))
        client_thread.start()

        try:
            #encuentra quien envia el msj===================
            for client in self.clients:
                if client["socket"] == client_socket:
                    sender_name = client["name"] + ": "
                    break


            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                message = data.decode("utf-8")
                print(message)


                if message.startswith("@"):
                    recipient, message = message.split(":", 1)
                    recipient = recipient[1:]

                    if recipient == "server": #consola del servidor
                        self.send_message_to_server(sender_name, message)

                    else: #consola de participante específico
                        self.send_message_to_client(recipient, (sender_name + message))

                else: #consola de todos los participantes
                    self.broadcast((sender_name + message), client_socket)



            client_socket.close()

            if client_socket in self.clients:
                self.clients.remove(client_socket)

        except BaseException as error:
            self.utils.error_handler(error)
            self.server_socket.close()


    #Metodo para imprimir en consola ya sea la del server, cliente1, cliente2, ....
    def send_message_to_server(self, sender_name, message):
        print(sender_name, message)


    def send_message_to_client(self, recipient, message):
        for client in self.clients:
            if client["name"] == recipient:
                client["socket"].send(message.encode("utf-8"))
                break


    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client["socket"] != sender_socket:
                client["socket"].send(message.encode("utf-8"))






############################################################################
#CONTROL DE BASE DE DATOS - MARIADB
############################################################################
class DatabaseConexion():
    def __init__(self):
        try:
            self.__conexion = mariadb.connect(
                user="admin",
                password="grupo1",
                host="localhost",
                port=3306,
                database="sa1bd"
            )

            #self.conexion.autocommit = False

        except BaseException as error:
            print(error)



    def validar_credenciales(self, credenciales):
        cursor = self.__conexion.cursor()
        query = """
        SELECT a.id_cliente, b.nombre
        FROM usuarios a
        INNER JOIN clientes b ON b.id = a.id_cliente AND b.estado = 1
        WHERE a.cod_usuario = ? AND a.clave = ? AND a.estado = 1
        """

        cursor.execute(query, credenciales)
        data = cursor.fetchone()

        if cursor.rowcount == 1:
            return json.dumps({
                "authenticated": True,
                "id_cliente": data[0],
                "nombre": data[1]
            })

        else: return json.dumps({"authenticated": False})



    def consultar_prestamos(self, id_cliente):
        cursor = self.__conexion.cursor()

        query = """
        SELECT p.id id_prestamo, p.monto_prestamo, p.cuotas, p.monto_cuota, p.saldo_pendiente, e.descripcion estado
        FROM prestamos p
        INNER JOIN estados_prestamo e ON e.id = p.estado
        WHERE p.id_cliente = ?"""

        cursor.execute(query, id_cliente)

        resp = []
        for (id_prestamo, monto_prestamo, cuotas, monto_cuota, saldo_pendiente, estado) in cursor:
            resp.append({
                "id_prestamo": id_prestamo,
                "monto_prestamo": monto_prestamo,
                "cuotas": cuotas,
                "monto_cuota": monto_cuota,
                "saldo_pendiente": saldo_pendiente,
                "estado": estado
            })

        return json.dumps(resp)


    
    def consultar_pagos(self, ids):
        cursor = self.__conexion.cursor()

        query = """
        SELECT c.id id_cuota, c.id_prestamo, c.cuota, c.fecha, c.monto_cuota, e.descripcion estado
        FROM cuotas c
        INNER JOIN estados_cuota e ON e.id = c.estado
        WHERE c.id_cliente = ? AND c.id_prestamo = ?"""

        cursor.execute(query, ids)

        resp = []
        for (id_cuota, id_prestamo, cuota, fecha, monto_cuota, estado) in cursor:
            resp.append({
                "id_cuota": id_cuota,
                "id_prestamo": id_prestamo,
                "cuota": cuota,
                "fecha": fecha,
                "monto_cuota": monto_cuota,
                "estado": estado
            })

        return json.dumps(resp)



    def consultar_reversiones(self, ids):
        cursor = self.__conexion.cursor()

        query = """
        SELECT r.id id_reversion, r.fecha, r.id_prestamo, r.id_cuota
        FROM reversiones r
        WHERE r.id_cliente = ? AND r.id_prestamo = ?"""

        cursor.execute(query, ids)

        resp = []
        for (id_reversion, fecha, id_prestamo, id_cuota) in cursor:
            resp.append({
                "id_reversion": id_reversion,
                "fecha": fecha,
                "id_prestamo": id_prestamo,
                "id_cuota": id_cuota
            })

        return json.dumps(resp)



    def registrar_pago(self, ids):
            cursor = self.__conexion.cursor()

            query = "CALL PAGO_CUOTA_PRESTAMO(?, ?)"
            cursor.execute(query, ids)

            resp = "proccessed"
            return json.dumps(resp)





############################################################################
#BLOQUE DE INICIO DE SCRIPT SERVER.PY
############################################################################
if __name__ == "__main__":

    parametros = {
        "server_ip": '172.31.30.203',
        "server_port": 9999,
        "database_conexion": DatabaseConexion()
    }

    server = ServerSocket(parametros)
