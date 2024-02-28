import socket
import threading
import os
import tkinter as tk
from tkinter import messagebox
import subprocess
import json


############################################################################
#CONSTRUCCION DE LA VENTANA
############################################################################
class Ventana():
    def __init__(self, parametros):
        self.login_socket   = parametros["login_socket"]
        self.utils  = parametros["utils"]
        root        = tk.Tk()
        
        root.title("Login")
        colorFondo = "white"
        root.configure(bg=colorFondo)

        ancho_ventana = root.winfo_screenwidth() // 2
        alto_ventana = root.winfo_screenheight() // 2
        posicion_x = (root.winfo_screenwidth() - ancho_ventana) // 2
        posicion_y = (root.winfo_screenheight() - alto_ventana) // 2
        root.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

        try:
            imagen_logo = tk.PhotoImage(file="logo.png")
            label_logo = tk.Label(root, image=imagen_logo, bg=colorFondo)
            label_logo.pack(pady=20)
        except tk.TclError:
            print("No se pudo cargar el logo.")


        fuente = ("Arial Black", 12)

        label_username = tk.Label(root, text="Usuario:", font=fuente, bg=colorFondo)
        label_username.pack()
        self.entry_username = tk.Entry(root, font=fuente)
        self.entry_username.pack()

        label_password = tk.Label(root, text="Contraseña:", font=fuente , bg=colorFondo)
        label_password.pack()
        self.entry_password = tk.Entry(root, show="*", font=fuente)
        self.entry_password.pack()

        boton_ingresar = tk.Button(root, text="Ingresar", command=self.validar_credenciales, font=fuente, bg='limegreen', fg='white', bd=0)
        boton_ingresar.pack(pady=10)

        root.mainloop()

    
    ############################################################################
    #ACCION DE BOTON LOGIN
    ############################################################################
    def validar_credenciales(self):
        self.login_socket.send(
            json.dumps({
                "username": self.entry_username.get(),
                "password": self.entry_password.get()
            })
        )








############################################################################
#SOCKET CLIENTE
############################################################################
class LoginSocket():
    def __init__(self, parametros):
        self.utils = parametros["utils"]

        ############################################################################
        #PUESTA EN MARCHA DEL SOCKET CLIENTE
        ############################################################################
        try:
            self.utils.limpiarConsola()
            self.login_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
            self.login_socket.connect((parametros["server_ip"], parametros["server_port"]))
            print("===============================================================")
            print(f"\nSocket Cliente Establecido:\nhost: {parametros["server_ip"]}\nport: {parametros["server_port"]}\n")
            print("===============================================================")

            receive_thread = threading.Thread(target=self.receive)
            receive_thread.start()

            self.send(json.dumps({"oper": "login"}))

        except BaseException as errorType: 
            self.utils.error_handler(errorType)
            self.server_socket.close()


    ############################################################################
    #ENVIO DE MENSAJES A SOCKET SERVIDOR
    ############################################################################
    def send(self, message):
        self.login_socket.send(message.encode("utf-8"))


    
    
    ############################################################################
    #RECEPCION DE MENSAJES DEL SOCKET SERVIDOR
    ############################################################################
    def receive(self):
        while True:
            data = self.login_socket.recv(1024).decode("utf-8")

            if json.loads(data)["authenticated"]:
                subprocess.run(["python", "menu.py", str(data)])
            else:
                messagebox.showwarning("Login:", "Credenciales no validas")









############################################################################
#CONTROL DE EXCEPCIONES
############################################################################
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

        elif(type(e) is ConnectionRefusedError):
            msj = "Conexion rechazada. Valide que el servidor este activo y a la escucha"

        else:    
            msj = f"Error: {type(e)}\n{e}"

        self.limpiarConsola()
        print(msj + "\n\n")
        exit()



    #Limpiar pantalla =====================================================
    def limpiarConsola(self):
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Linux, Unix, macOS
            os.system('clear')









############################################################################
#BLOQUE DE INICIO DE SCRIPT LOGIN.PY
############################################################################
parametros = {
    "login_socket": LoginSocket({
        "server_ip": "ec2-3-139-109-145.us-east-2.compute.amazonaws.com",
        "server_port": 9999,
        "utils": Utilities()
    }),
    "utils": Utilities()
}

login = Ventana(parametros)


