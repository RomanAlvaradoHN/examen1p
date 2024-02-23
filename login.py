import socket
import threading
import os
import tkinter as tk
from tkinter import messagebox
import subprocess

class Ventana():

    #Constructor de clase (ventana login )================================
    def __init__(self, parametros):
        self.sokt = parametros["clientsocket"]
        self.utils        = parametros["utils"]
        root              = tk.Tk()
        
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

        boton_ingresar = tk.Button(root, text="Ingresar", command=self.__validarCredenciales, font=fuente, bg='limegreen', fg='white', bd=0)
        boton_ingresar.pack(pady=10)
        
        root.mainloop()
       

    
    
    #Validacion de credenciales ==========================================
    def __validarCredenciales(self): #Inicio de trama: 1
        username = self.entry_username.get()
        password = self.entry_password.get()
        self.sokt.send(f"credenciales:{username}:{password}")








class ClientSocket():   
    
    #Constructor de clase =============================
    def __init__(self, parametros):
        self.utils = parametros["utils"]

        try:
            #Establecer conexion de socket =============
            self.utils.limpiarConsola()
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
            self.client_socket.connect((parametros["server_ip"], parametros["server_port"]))
            print("Socket establecido con éxito")
        
        except BaseException as errorType: 
            self.utils.error_handler(errorType)
            self.server_socket.close()


    #Enviar trama a servidor ==========================
    def send(self, message):
        self.client_socket.send(message.encode("utf-8"))


    #Recibir respuesta de servidor ====================
    def receive(self):

        while True:

            data = self.client_socket.recv(1024)
            
            if not data:
                break
            
            #print(data.decode("utf-8"))

            message = data.decode("utf-8")
            print(message)



class Utilities():

    #Manejador de errores de socket =======================================
    def error_handler(self, errorType):
        msj = None

        if(type(errorType) is KeyboardInterrupt):
            msj = "Script terminado por teclado"

        elif(type(errorType) is ValueError):
            msj = "Usuario abandonó"

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

"""
cliente_id = None

def verificar_credenciales(usuario, contraseña):


        cursor = conexion.cursor()
        consulta = "SELECT idCliente FROM usuairo WHERE codUsuario = %s AND clave = %s"
        cursor.execute(consulta, (usuario, contraseña))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            cliente_id = resultado[0]
            messagebox.showinfo("Inicio de sesión exitoso", "¡Bienvenido!")
            root.destroy()
            subprocess.run(["python", "menu.py", str(cliente_id)])  # Pasar cliente_id como argumento al menú
        else:
            messagebox.showerror("Error de inicio de sesión", "Credenciales incorrectas")
    except mysql.connector.Error as error:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {error}")

    """
#INICIO DE SCRIPT========================================================================
parametros = {
    "clientsocket": ClientSocket({
        "server_ip": "ec2-3-143-210-52.us-east-2.compute.amazonaws.com",
        "server_port": 9999,
        "utils": Utilities()
    }),
    "utils": Utilities()
}

login = Ventana(parametros)


