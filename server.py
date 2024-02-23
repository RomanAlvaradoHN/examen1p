import socket
import threading
import os
import mariadb

class Server:


    def __init__(self, parametros):
        self.host  = parametros["server_ip"]
        self.port  = parametros["server_port"]
        self.db    = parametros["database_conexion"]
        self.utils = parametros["utilities"]

        #Inicio de socket ===========================================
        try:
            self.utils.limpiarConsola
            self.clients = []
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print("Servidor escuchando en {}:{}".format(self.host, self.port))

        except BaseException as errorType:
            self.utils.error_handler(errorType)
        

        #Escucha de mensajes ========================================
        try:
            while True:
                self.__socketActivityHandler


        except BaseException as errorType:
            self.utils.error_handler(errorType)





    def __socketActivityHandler(self):
        client_socket, client_address = self.server_socket.accept()
        message = client_socket.recv(1024).decode("utf-8")

        if message.startswith("credenciales"):
            pass
        
        elif message.startswith("chat"):
            self.__handle_client(message)



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



    #Metodos para imprimir en consola ya sea la del server, cliente1, cliente2, ....
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




    





class DataBase_Conexion():

    def __init__(self):
        try:
            self.conexion = mariadb.connect(
                user="admin",
                password="grupo1",
                host="localhost",
                port=3306,
                database="sa1bd"
            )

        except BaseException as error:
            print(error)


    def validarCredenciales(self, trama):
        subTramas = trama.split("-", 2)
        username = subTramas[2]
        password = subTramas[3]

        cursor = self.conexion.cursor()
        query = "SELECT COUNT(*) FROM usuairo WHERE codUsuario = %s AND clave = %s"
        cursor.execute(query, (username, password))
        respuesta = cursor.fetchone()

        print(respuesta)
        self.conexion.close()

    """
        if respuesta:
            cliente_id = resultado[0]
            messagebox.showinfo("Inicio de sesión exitoso", "¡Bienvenido!")
            root.destroy()
            subprocess.run(["python", "menu.py", str(cliente_id)])  # Pasar cliente_id como argumento al menú
        else:
            messagebox.showerror("Error de inicio de sesión", "Credenciales incorrectas")
    """


class Utilities():

    #Manejador de errores de socket =======================================
    def error_handler(self, errorType):
        msj = None

        if(type(errorType) is KeyboardInterrupt):
            msj = "Script terminado por teclado"

        elif(type(errorType) is ValueError):
            msj = "Usuario abandonó"

        elif(type(errorType) is OSError):
            msj = "Direccion en uso. Utilize: ss -ltpn | grep [server_port]"
        
        else: print("Nuevo Error:", errorType)

        self.limpiarConsola()
        print(msj + "\n\n")
        exit()




    #Limpiar pantalla =====================================================
    def limpiarConsola(self):
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Linux, Unix, macOS
            os.system('clear')





#Bloque de entrada e inicio del script =========================================
if __name__ == "__main__":

    parametros = {
        "server_ip": '172.31.30.203',
        "server_port": 9999,
        "database_conexion": DataBase_Conexion(),
        "utilities": Utilities()
    }

    server = Server(parametros)
