import socket
import threading
import os
import mysql.connector

class Server:
    
    #Constructor de la clase ========================================
    def __init__(self, host, port, consultas, utilities):
        os.system('clear')
        self.host = host
        self.port = port
        self.consultas = consultas
        self.utils = utilities
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

    
    #Inicializador del script ========================================
    def start(self):
        self.server_socket.listen(5)
        print("Servidor escuchando en {}:{}".format(self.host, self.port))
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                client_name = client_socket.recv(1024).decode("utf-8")


                print("\n\nNueva conexión de {}:{}".format(client_address[0], client_address[1]))
                print("Participante: {}".format(client_name))
                print("====================")

                #Añadimos el nuevo participante a la lista
                self.clients.append({"name": client_name, "socket": client_socket})


                client_thread = threading.Thread(target = self.handle_client, args=(client_socket,))
                client_thread.start()


        except BaseException as errorType: 
            self.utils.error_handler(errorType)


    #Obtener datos  del mensaje y determinar qué metodo procesa la salida del mensaje: ==========================
    def handle_client(self, client_socket):
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

                #MANEJO DE TRAMAS, MENSAJERIA Y COMUNICACION ==============================================
                if message.startswith("1"): #Validar credenciales
                    self.consultas.validarCredenciales(message)
                
                elif message.startswith("@"):
                    recipient, message = message.split(":", 1)
                    recipient = recipient[1:]

                    if recipient == "server": #consola del servidor
                        self.send_message_to_server(sender_name, message)
                    
                    else: #consola de participante específico
                        self.send_message_to_client(recipient, (sender_name + message))
                
                else: #consola de todos los participantes
                    self.broadcast((sender_name + message), client_socket)

            client_socket.close()
            self.clients.remove(client_socket)

        except BaseException as error:
            self.utils.error_handler(error)



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









class Consultas():

    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                user="admin",
                password="grupo1",
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

        if(type(errorType) is KeyboardInterrupt):
            msj = "Script terminado por teclado"
            print(msj)


        elif(type(errorType) is ValueError):
            msj = "Usuario abandonó"
            print(msj)

        print("Error", errorType)
        self.server_socket.close()
        exit()




    #Limpiar pantalla =====================================================
    def limpiarConsola(self):
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Linux, Unix, macOS
            os.system('clear')





#Bloque de entrada e inicio del script =========================================
if __name__ == "__main__":
    consultas = Consultas()
    utilities = Utilities()
    server = Server('172.31.42.187', 9999, consultas, utilities)
    server.start()
