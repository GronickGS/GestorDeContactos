import tkinter as tk

def convertir_a_binario():
    try:
        numero_decimal = int(entrada_decimal.get())
        binario = bin(numero_decimal)[2:]  # Convertir a binario y quitar el prefijo '0b'
        texto_binario.set(binario)
    except ValueError:
        texto_binario.set("Error: Ingrese un número válido")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Conversor Decimal a Binario")

# Crear etiqueta y entrada para el número decimal
etiqueta_decimal = tk.Label(ventana, text="Número Decimal:")
etiqueta_decimal.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entrada_decimal = tk.Entry(ventana)
entrada_decimal.grid(row=0, column=1, padx=5, pady=5)

# Crear botón de conversión
boton_convertir = tk.Button(ventana, text="Convertir a Binario", command=convertir_a_binario)
boton_convertir.grid(row=0, column=2, padx=5, pady=5)

# Crear etiqueta y campo de texto para el resultado binario
texto_binario = tk.StringVar()
etiqueta_binario = tk.Label(ventana, text="Binario:")
etiqueta_binario.grid(row=1, column=0, padx=5, pady=5, sticky="w")
campo_binario = tk.Entry(ventana, textvariable=texto_binario, state='readonly')
campo_binario.grid(row=1, column=1, padx=5, pady=5)

# Ejecutar el bucle principal de la aplicación
ventana.mainloop()
