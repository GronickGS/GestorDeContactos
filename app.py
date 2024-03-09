import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import csv 

class AplicacionGestorContactos:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Contactos")

        # Conexión a la base de datos SQLite
        self.conexion = sqlite3.connect('contactos.db')
        self.crear_tabla()

        # Marco principal
        self.marco_principal = tk.Frame(root)
        self.marco_principal.pack(fill=tk.BOTH, expand=True)

        # Título del sistema
        self.titulo_sistema = tk.Label(self.marco_principal, text="SISTEMA GS", font=("Helvetica", 14, "bold"))
        self.titulo_sistema.pack(side=tk.TOP, pady=10)

        # Marco para agregar contactos
        self.marco_agregar = tk.Frame(self.marco_principal, padx=10, pady=10)
        self.marco_agregar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Cargar la imagen y redimensionarla
        self.imagen_usuario = tk.PhotoImage(file="user.png").subsample(5, 5)  # Ajusta los valores según sea necesario

        # Crear un Label para mostrar la imagen encima de los campos de entrada
        self.etiqueta_imagen = tk.Label(self.marco_agregar, image=self.imagen_usuario)
        self.etiqueta_imagen.grid(row=0, column=1, padx=(0, 50), pady=0, sticky="nsew")

        # Crear los widgets para agregar contactos
        self.etiqueta_nombre = tk.Label(self.marco_agregar, text="Nombre:")
        self.etiqueta_nombre.grid(row=1, column=0, sticky="e", padx=10, pady=5)

        self.entrada_nombre = tk.Entry(self.marco_agregar)
        self.entrada_nombre.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        self.etiqueta_telefono = tk.Label(self.marco_agregar, text="Teléfono:")
        self.etiqueta_telefono.grid(row=2, column=0, sticky="e", padx=10, pady=5)

        self.entrada_telefono = tk.Entry(self.marco_agregar, validate="key", validatecommand=(root.register(self.es_numero), '%P'))
        self.entrada_telefono.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")

        self.boton_agregar = tk.Button(self.marco_agregar, text="Agregar Contacto", command=self.agregar_contacto)
        self.boton_agregar.grid(row=3, column=0, columnspan=2, pady=10)

        # Campo de búsqueda
        self.marco_buscar = tk.Frame(self.marco_principal)
        self.marco_buscar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.etiqueta_buscar = tk.Label(self.marco_buscar, text="Buscar:")
        self.etiqueta_buscar.pack(side=tk.LEFT, padx=(0, 5))

        self.entrada_buscar = tk.Entry(self.marco_buscar)
        self.entrada_buscar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entrada_buscar.bind('<KeyRelease>', self.buscar_contacto)

        # Marco para mostrar contactos
        self.marco_mostrar = tk.Frame(self.marco_principal, padx=10, pady=10)
        self.marco_mostrar.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Crear el árbol para mostrar contactos
        self.arbol = ttk.Treeview(self.marco_mostrar, columns=('Nombre', 'Teléfono'), show='headings')
        self.arbol.heading('Nombre', text='Nombre')
        self.arbol.heading('Teléfono', text='Teléfono')
        self.arbol.pack(expand=True, fill='both')

        # Botón para exportar a CSV
        self.boton_exportar = tk.Button(self.marco_mostrar, text="Exportar a CSV", command=self.exportar_a_csv)
        self.boton_exportar.pack(side=tk.BOTTOM, pady=10)

        # Marco para los botones de edición y borrado
        self.marco_botones = tk.Frame(self.marco_mostrar)
        self.marco_botones.pack(side=tk.BOTTOM)

        # Botones para editar y borrar contacto
        self.boton_editar = tk.Button(self.marco_botones, text="Editar", command=self.editar_contacto)
        self.boton_editar.pack(side=tk.LEFT, padx=5, pady=(10, 0))  # Ajusta el margen superior (top) a 5

        self.boton_borrar = tk.Button(self.marco_botones, text="Borrar", command=self.borrar_contacto)
        self.boton_borrar.pack(side=tk.LEFT, padx=5, pady=(10, 0))  # Ajusta el margen superior (top) a 5

        # Cargar contactos existentes
        self.cargar_contactos()

    def buscar_contacto(self, event=None):
        texto_busqueda = self.entrada_buscar.get().lower()
        contactos_filtrados = []

        for contacto in self.contactos:
            nombre = contacto[1].lower()
            telefono = contacto[2].lower()
            if texto_busqueda in nombre or texto_busqueda in telefono:
                contactos_filtrados.append(contacto)

        self.mostrar_contactos(contactos_filtrados)

    def crear_tabla(self):
        cursor = self.conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS contactos
                          (id INTEGER PRIMARY KEY, nombre TEXT, telefono TEXT)''')
        self.conexion.commit()

    def agregar_contacto(self):
        nombre = self.entrada_nombre.get().capitalize()  # Capitaliza la primera letra del nombre
        telefono = self.entrada_telefono.get()

        if nombre and telefono:
            cursor = self.conexion.cursor()
            cursor.execute('INSERT INTO contactos (nombre, telefono) VALUES (?, ?)', (nombre, telefono))
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Contacto agregado correctamente")
            self.limpiar_entradas()
            self.cargar_contactos()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos")

    def limpiar_entradas(self):
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_telefono.delete(0, tk.END)

    def cargar_contactos(self):
        cursor = self.conexion.cursor()
        cursor.execute('SELECT * FROM contactos ORDER BY nombre ASC')  # Ordenar por nombre de forma ascendente
        self.contactos = cursor.fetchall()
        self.mostrar_contactos()

    def mostrar_contactos(self, contactos=None):
        if contactos is None:
            contactos = self.contactos

        # Limpiar árbol antes de volver a cargar los contactos
        for row in self.arbol.get_children():
            self.arbol.delete(row)

        # Insertar contactos en el árbol
        for contacto in contactos:
            self.arbol.insert('', 'end', values=(contacto[1], contacto[2]))

    def exportar_a_csv(self):
        if self.contactos:
            nombre_archivo = "contactos.csv"
            with open(nombre_archivo, 'w', newline='') as csvfile:
                nombres_columnas = ['Nombre', 'Teléfono']
                escritor_csv = csv.DictWriter(csvfile, fieldnames=nombres_columnas)
                escritor_csv.writeheader()
                for contacto in self.contactos:
                    escritor_csv.writerow({'Nombre': contacto[1], 'Teléfono': contacto[2]})
            messagebox.showinfo("Éxito", f"Contactos exportados a {nombre_archivo}")
        else:
            messagebox.showerror("Error", "No hay contactos para exportar")
    
    def editar_contacto(self):
        elemento_seleccionado = self.arbol.selection()
        if elemento_seleccionado:
            nombre = self.arbol.item(elemento_seleccionado, 'values')[0]
            telefono = self.arbol.item(elemento_seleccionado, 'values')[1]

            # Popup para editar el contacto
            ventana_editar = tk.Toplevel(self.root)
            ventana_editar.title("Editar Contacto")

            etiqueta_nombre = tk.Label(ventana_editar, text="Nombre:")
            etiqueta_nombre.grid(row=0, column=0, padx=10, pady=5)
            entrada_nombre = tk.Entry(ventana_editar)
            entrada_nombre.insert(0, nombre)
            entrada_nombre.grid(row=0, column=1, padx=10, pady=5)

            etiqueta_telefono = tk.Label(ventana_editar, text="Teléfono:")
            etiqueta_telefono.grid(row=1, column=0, padx=10, pady=5)
            entrada_telefono = tk.Entry(ventana_editar)
            entrada_telefono.insert(0, telefono)
            entrada_telefono.grid(row=1, column=1, padx=10, pady=5)

            boton_guardar = tk.Button(ventana_editar, text="Guardar Cambios", command=lambda: self.guardar_cambios(elemento_seleccionado, entrada_nombre.get(), entrada_telefono.get(), ventana_editar))
            boton_guardar.grid(row=2, column=0, columnspan=2, pady=10)

    def borrar_contacto(self):
        elemento_seleccionado = self.arbol.selection()
        if elemento_seleccionado:
            confirmacion = messagebox.askyesno("Eliminar Contacto", "¿Está seguro que desea eliminar este contacto?")
            if confirmacion:
                cursor = self.conexion.cursor()
                cursor.execute('DELETE FROM contactos WHERE nombre=? AND telefono=?',
                            (self.arbol.item(elemento_seleccionado, 'values')[0], self.arbol.item(elemento_seleccionado, 'values')[1]))
                self.conexion.commit()
                self.cargar_contactos()

    def guardar_cambios(self, elemento_seleccionado, nuevo_nombre, nuevo_telefono, ventana_editar):
        cursor = self.conexion.cursor()
        cursor.execute('UPDATE contactos SET nombre=?, telefono=? WHERE nombre=? AND telefono=?',
                       (nuevo_nombre, nuevo_telefono, self.arbol.item(elemento_seleccionado, 'values')[0], self.arbol.item(elemento_seleccionado, 'values')[1]))
        self.conexion.commit()
        messagebox.showinfo("Éxito", "Contacto actualizado correctamente")
        ventana_editar.destroy()
        self.cargar_contactos()

    def es_numero(self, texto):
        return texto.isdigit() or texto == ""

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionGestorContactos(root)
    root.mainloop()
