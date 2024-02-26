import socket
import threading
import os
import mariadb
import json

class SocketServer:

    def __init__(self, parametros):
        self.host  = parametros["server_ip"]
        self.port  = parametros["server_port"]
        self.msgi  = parametros["minterp"]
        self.db    = parametros["database_conexion"]
        self.utils = parametros["utilities"]

        #Inicio de socket ===========================================
        try:
            self.utils.limpiarConsola()
            self.clients = []
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print("===============================================================")
            print(f"\n    Servidor escuchando en {self.host}:{self.port}        \n")
            print("===============================================================")
        except BaseException as errorType:
            self.utils.error_handler(errorType)


        #Escucha de mensajes ========================================
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                message = client_socket.recv(1024).decode("utf-8")

                if message.startswith("login"):
                    print("Nuevo intento login: " + client_address[0])
                    client_thread = threading.Thread(target = self.__loginRequests, args=([client_socket]))
                    client_thread.start()






                elif message.startswith("chat"):
                    pass


        except BaseException as errorType:
            self.utils.error_handler(errorType)




    def __loginRequests(self, client_socket):
        while True:
            credenciales = login.loads(client_socket.recv(1024).decode("utf-8"))
            
            if not data: break
            ****
            resp = self.db.validarCredenciales(credenciales)
            client_socket.send(resp.encode())




    #Obtener datos  del mensaje y determinar qué metodo procesa la salida del mensaje: ==========================
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




#Clases de trabajo =============================================================
class Message_Interpreter():
    
    def getCredentials(self, message):
        m = message.replace("login:", "")
        username, password = m.split(":", 1)
        return (username, password)

class DataBase_Conexion():
    #Prepara un objeto conexion ============
    def __init__(self):
        try:
            self.conexion = mariadb.connect(
                user="admin",
                password="grupo1",
                host="localhost",
                port=3306,
                database="sa1bd"
            )

            #self.conexion.autocommit = False

        except BaseException as error:
            print(error)



    def validarCredenciales(self, credenciales):
        cursor = self.conexion.cursor()

        query = """
        SELECT a.id_cliente, b.nombre        
        FROM usuarios a
        INNER JOIN clientes b ON b.id = a.id_cliente AND b.estado = 1   
        WHERE a.cod_usuario = ?
        AND a.clave = ?
        AND a.estado = 1
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

class Utilities():

    #Manejador de errores de socket =======================================
    def error_handler(self, e):
        msj = ""

        if(type(e) is KeyboardInterrupt):
            msj = "Script terminado por teclado"

        elif(type(e) is ValueError):
            msj = "Usuario abandonó"

        elif(type(e) is OSError):
            msj = "Direccion en uso. Utilize: ss -ltpn | grep [server_port]"

        elif(type(e) is mariadb.Error):
            msj = "Error con la base de datos:\n{e}"

        else:    
            msj = f"Error: {type(e)}\n{e}"

        self.limpiarConsola()
        print(msj + "\n\n")
        exit()


    #Limpiar pantalla =====================================================
    def limpiarConsola(self):
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Linux, Unix, macOS, POSIX
            os.system('clear')







#Bloque de entrada e inicio del script =========================================
if __name__ == "__main__":

    parametros = {
        "server_ip": '172.31.30.203',
        "server_port": 9999,
        "minterp": Message_Interpreter(),
        "database_conexion": DataBase_Conexion(),
        "utilities": Utilities()
    }

    server = SocketServer(parametros)
