import socket
import tkinter as tk
import json
from prestamo import *



class Menu():
    def __init__(self, sockt, usuario):
        self.sockt = sockt
        self.usuario = usuario


    def mostrar_ventana(self):
        self.pmenu = tk.Tk()
        self.pmenu.title("Interfaz Principal")

        screen_width = self.pmenu.winfo_screenwidth()
        screen_height = self.pmenu.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.pmenu.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        background_color = "#7FFF00"
        self.pmenu.configure(bg=background_color)

        titulo_label = tk.Label(self.pmenu, text="Menú Principal", font=("Arial Black", 28), bg=background_color)
        titulo_label.pack(pady=20)

        button_font = ("Arial Black", 16)
        button_width = 20
        button_height = 2
        button_relief_style = "groove"
        button_bg_color = "#007bff"

        boton_prestamos = tk.Button(self.pmenu, text="Préstamos", font=button_font, width=button_width, height=button_height, relief=button_relief_style, bg=button_bg_color, command=self.abrir_prestamos)
        boton_prestamos.pack(pady=5)

        boton_pagos = tk.Button(self.pmenu, text="Pagos", font=button_font, width=button_width, height=button_height, relief=button_relief_style, bg=button_bg_color, command=self.abrir_pagos)
        boton_pagos.pack(pady=5)

        boton_reversiones = tk.Button(self.pmenu, text="Reversiones", font=button_font, width=button_width, height=button_height, relief=button_relief_style, bg=button_bg_color, command=self.abrir_reversiones)
        boton_reversiones.pack(pady=5)

        boton_chat = tk.Button(self.pmenu, text="Chat", font=button_font, width=button_width, height=button_height, relief=button_relief_style, bg=button_bg_color, command=self.abrir_chat)
        boton_chat.pack(pady=5)

        id_label = tk.Label(self.pmenu, text=f"Cliente: {self.usuario["nombre"]}", font=("Arial Black", 12), bg=background_color)
        id_label.pack(pady=10)

        self.pmenu.mainloop()


    def abrir_prestamos(self):
        self.pmenu.withdraw()
        pprestamo = Prestamo(self.sockt, self.usuario)



    def abrir_pagos(self):
        pass

    def abrir_reversiones(self):
        pass

    def abrir_chat(self):
        pass


