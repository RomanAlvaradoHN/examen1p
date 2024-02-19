import tkinter as tk

def mostrar_mensaje():
    label_saludo.config(text="¡Hola, chat!")

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz de Hola chat")

# Crear un widget de etiqueta para mostrar el mensaje
label_saludo = tk.Label(root, text="", font=("Arial", 24))
label_saludo.pack(padx=20, pady=20)  # Agregar padding

# Crear un botón para activar la función mostrar_mensaje
boton_mostrar = tk.Button(root, text="Mostrar Saludo", command=mostrar_mensaje)
boton_mostrar.pack(pady=10)

# Ejecutar el bucle principal de la aplicación
root.mainloop()