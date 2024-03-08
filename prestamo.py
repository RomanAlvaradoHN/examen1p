import socket
import tkinter as tk
from tkinter import ttk
import json



class Prestamo():
    def __init__(self, sockt, usuario):
        self.sockt = sockt
        self.usuario = usuario


    def mostrar_ventana(self):
        self.pprestamo = tk.Tk()
        self.pprestamo.title("Tabla de Préstamos")

        columnas = ('id_prestamo', 'monto_prestamo', 'cuotas', 'monto_cuota', 'saldo_pendiente', 'estado')
        displaycolumnas = ('id_prestamo', 'monto_prestamo', 'cuotas', 'monto_cuota', 'saldo_pendiente', 'estado')
        self.tabla = ttk.Treeview(self.pprestamo, displaycolumns=displaycolumnas, columns=columnas)


        #for prestamo in prestamos:
        #    tabla.insert("", "end", text=prestamo["id"], values=(prestamo["id"], prestamo["IdCliente"], prestamo["MontoPrestamo"], prestamo["cuotas"], prestamo["montocuota"], prestamo["Estado"]))

        self.tabla.pack()
        
        self.get_prestamos_cliente()
        self.pprestamo.mainloop()



    def get_prestamos_cliente(self):
        self.sockt.server_response = None

        self.sockt.send(
            json.dumps({
                "operacion": "consultar_prestamos",
                "id_cliente": self.usuario["id_cliente"]
            })
        )

        while True:
            if not self.sockt.server_response: pass
            else:
                prestamos = json.loads(self.sockt.server_response)
                #print(str(type(resp)), f"\n {resp}")

                for prestamo in prestamos:
                    self.tabla.insert("", "end", values=(
                        prestamo["id_prestamo"],
                        prestamo["monto_prestamo"],
                        prestamo["cuotas"],
                        prestamo["monto_cuota"],
                        prestamo["saldo_pendiente"],
                        prestamo["estado"]))

                break

