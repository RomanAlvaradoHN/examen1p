import socket
import tkinter as tk
from tkinter import ttk
import json



class Prestamo():
    def __init__(self, sockt, usuario):
        self.sockt = sockt
        self.usuario = usuario


    def mostrar_ventana():
        ventana = tk.Tk()
        ventana.title("Tabla de Préstamos")

        tabla = ttk.Treeview(ventana)
        tabla["columns"] = ("Id", "IdCliente", "MontoPrestamo", "Cuotas", "MontoCuota", "Estado")
        tabla.heading("#0", text="ID Préstamo")
        tabla.heading("Id", text="ID Préstamo")
        tabla.heading("IdCliente", text="ID Cliente")
        tabla.heading("MontoPrestamo", text="Monto Préstamo")
        tabla.heading("Cuotas", text="Cuotas")
        tabla.heading("MontoCuota", text="Monto Cuota")
        tabla.heading("Estado", text="Estado")

        #for prestamo in prestamos:
        #    tabla.insert("", "end", text=prestamo["id"], values=(prestamo["id"], prestamo["IdCliente"], prestamo["MontoPrestamo"], prestamo["cuotas"], prestamo["montocuota"], prestamo["Estado"]))

        tabla.pack()

        ventana.mainloop()
