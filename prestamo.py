import tkinter as tk
from tkinter import ttk
import mysql.connector
from login import cliente_id

# Función para obtener el ID del cliente del label
def obtener_id_cliente():
    # Aquí obtienes el valor real del label
    return cliente_id

# Función para obtener datos de la base de datos
def obtener_prestamos_por_cliente(id_cliente):
    # Conectarse a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sa1bd"
    )

    cursor = conexion.cursor(dictionary=True)

    # Consulta SQL para obtener los préstamos por cliente
    consulta = f"SELECT * FROM prestamo WHERE IdCliente = {id_cliente}"

    cursor.execute(consulta)
    prestamos = cursor.fetchall()

    conexion.close()

    return prestamos

# Función para mostrar los datos en una tabla
def mostrar_tabla_prestamos(prestamos):
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

    for prestamo in prestamos:
        tabla.insert("", "end", text=prestamo["id"], values=(prestamo["id"], prestamo["IdCliente"], prestamo["MontoPrestamo"], prestamo["cuotas"], prestamo["montocuota"], prestamo["Estado"]))

    tabla.pack()

    ventana.mainloop()

# Obtener el ID del cliente del label
id_cliente = obtener_id_cliente()

# Verificar el valor del label y mostrar los préstamos si es válido
if id_cliente is not None:
    prestamos = obtener_prestamos_por_cliente(id_cliente)
    mostrar_tabla_prestamos(prestamos)
else:
    print("No se pudo obtener el ID del cliente del label.")
