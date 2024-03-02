import socket
import threading
import tkinter as tk
from tkinter import messagebox
import json
from Utilities import *
from menu import *

############################################################################
#CONSTRUCCION DE LA VENTANA
############################################################################
class Ventana():
    def __init__(self, parametros):
        self.sockt = parametros["sockt"]
        self.utils = parametros["utils"]
        self.plogin = tk.Tk()
        
        self.plogin.title("Login")
        colorFondo = "white"
        self.plogin.configure(bg=colorFondo)

        ancho_ventana = self.plogin.winfo_screenwidth() // 2
        alto_ventana = self.plogin.winfo_screenheight() // 2
        posicion_x = (self.plogin.winfo_screenwidth() - ancho_ventana) // 2
        posicion_y = (self.plogin.winfo_screenheight() - alto_ventana) // 2
        self.plogin.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

        try:
            imagen_logo = tk.PhotoImage(file="logo.png")
            label_logo = tk.Label(self.plogin, image=imagen_logo, bg=colorFondo)
            label_logo.pack(pady=20)
        except tk.TclError:
            print("No se pudo cargar el logo.")


        fuente = ("Arial Black", 12)

        label_username = tk.Label(self.plogin, text="Usuario:", font=fuente, bg=colorFondo)
        label_username.pack()
        self.entry_username = tk.Entry(self.plogin, font=fuente)
        self.entry_username.pack()

        label_password = tk.Label(self.plogin, text="Contraseña:", font=fuente , bg=colorFondo)
        label_password.pack()
        self.entry_password = tk.Entry(self.plogin, show="*", font=fuente)
        self.entry_password.pack()

        boton_ingresar = tk.Button(self.plogin, text="Ingresar", command=self.validar_credenciales, font=fuente, bg='limegreen', fg='white', bd=0)
        boton_ingresar.pack(pady=10)

        self.plogin.mainloop()

    
    ############################################################################
    #ACCION DE BOTON LOGIN
    ############################################################################
    def validar_credenciales(self):
        self.sockt.send(
            json.dumps({
                "username": self.entry_username.get(),
                "password": self.entry_password.get()
            })
        )
        
        #se convierte el JSON a un Dict (diccionario)
        resp = json.loads(self.sockt.server_response)

        if "authenticated" in resp:
            if resp["authenticated"]:
                self.plogin.destroy()
                pmenu = Menu(self.sockt, resp)
                pmenu.mostrar_ventana()

            else:
                messagebox.showwarning("Login:", "Credenciales no validas")








############################################################################
#SOCKET CLIENTE
############################################################################
class LoginSocket():
    def __init__(self, parametros):
        self.server_response = json.dumps("")
        self.utils = parametros["utils"]

        ############################################################################
        #PUESTA EN MARCHA DEL SOCKET CLIENTE
        ############################################################################
        try:
            self.utils.clear_console()
            self.sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
            self.sockt.connect((parametros["server_ip"], parametros["server_port"]))
            print("===============================================================")
            print(f"\nSocket Cliente Establecido:\nhost: {parametros["server_ip"]}\nport: {parametros["server_port"]}\n")
            print("===============================================================")

            #Nuevo hilo para escuchar al servidor-----------------
            receive_thread = threading.Thread(target=self.receive)
            receive_thread.start()

        except BaseException as errorType: 
            self.utils.error_handler(errorType)
            self.server_socket.close()


    ############################################################################
    #ENVIO DE MENSAJES A SOCKET SERVIDOR
    ############################################################################
    def send(self, message):
        self.sockt.send(message.encode("utf-8"))


    
    ############################################################################
    #RECEPCION DE MENSAJES DEL SOCKET SERVIDOR
    ############################################################################
    def receive(self):
        self.send(json.dumps({"operacion": "login"}))  #<-- intento de login

        while True:
            #respuesta se recibe como un JSON
            self.server_response = self.sockt.recv(1024).decode("utf-8")
            #print(str(type(self.server_response)))






############################################################################
#BLOQUE DE INICIO DE SCRIPT LOGIN.PY
############################################################################
parametros = {
    "sockt": LoginSocket({
        "server_ip": "ec2-3-132-214-123.us-east-2.compute.amazonaws.com",
        "server_port": 9999,
        "utils": Utilities()
    }),
    "utils": Utilities()
}

login = Ventana(parametros)


