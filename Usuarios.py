import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import mysql.connector

class Database:
    def __init__(self):
        self.connection = self.connect_to_database()

    def connect_to_database(self):
        # Establecer la conexión
        connection = mysql.connector.connect(
            host="localhost",  # Cambia esto por la dirección del servidor de la base de datos
            user="root",  # Cambia esto por tu nombre de usuario de la base de datos
            password="",  # Cambia esto por tu contraseña de la base de datos
            database="reservaEventos"  # Cambia esto por el nombre de tu base de datos
        )

        return connection


class Usuarios:
    def __init__(self, root, database):
        self.root = root
        self.database = database

        self.id_usuario_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.numero_var = tk.StringVar()

        # Elementos de la interfaz
        self.id_usuario_label = tk.Label(root, text="ID:")
        self.id_usuario_entry = ttk.Entry(root, textvariable=self.id_usuario_var)
        self.nombre_label = tk.Label(root, text="Nombre:")
        self.nombre_entry = ttk.Entry(root, textvariable=self.nombre_var)
        self.correo_label = tk.Label(root, text="Correo:")
        self.correo_entry = ttk.Entry(root, textvariable=self.correo_var)
        self.numero_label = tk.Label(root, text="Número:")
        self.numero_entry = ttk.Entry(root, textvariable=self.numero_var)
        self.add_button = tk.Button(root, text="Agregar", command=self.add_user)
        self.search_button = tk.Button(root, text="Buscar", command=self.search_user)
        self.update_button = tk.Button(root, text="Actualizar", command=self.update_user)
        self.delete_button = tk.Button(root, text="Eliminar", command=self.delete_user)
        self.view_all_button = tk.Button(root, text="Ver todos", command=self.view_all_users)
        self.back_button = tk.Button(root, text="Regresar a Reservas", command=self.go_back_to_reservations)

        # Cargar la imagen
        self.image = Image.open("/Users/juanjo/Desktop/udem.png")
        self.image = self.image.resize((100, 100), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(root, image=self.photo)

        # Posicionamiento de los elementos
        self.id_usuario_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.id_usuario_entry.grid(row=0, column=1, padx=10, pady=5)
        self.nombre_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.nombre_entry.grid(row=1, column=1, padx=10, pady=5)
        self.correo_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.correo_entry.grid(row=2, column=1, padx=10, pady=5)
        self.numero_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.numero_entry.grid(row=3, column=1, padx=10, pady=5)
        self.add_button.grid(row=4, column=0, padx=10, pady=5)
        self.search_button.grid(row=4, column=1, padx=10, pady=5)
        self.update_button.grid(row=4, column=2, padx=10, pady=5)
        self.delete_button.grid(row=4, column=3, padx=10, pady=5)
        self.view_all_button.grid(row=4, column=4, padx=10, pady=5)
        self.back_button.grid(row=6, column=0, padx=10, pady=5)
        self.image_label.grid(row=0, column=5, rowspan=4, padx=10, pady=5, sticky=tk.NE)

        # Crear la conexión a la base de datos
        self.database = Database()

    def go_back_to_reservations(self):
        self.root.destroy()  # Cierra la ventana actual de Lugares

    def add_user(self):
        # Obtener los valores de los campos
        id_usuario = self.id_usuario_var.get()
        nombre = self.nombre_var.get()
        correo = self.correo_var.get()
        numero = self.numero_var.get()

        # Insertar el usuario en la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "INSERT INTO usuarios (id_usuario, nombre, correo, numero) VALUES (%s, %s, %s, %s)"
            values = (id_usuario, nombre, correo, numero)
            cursor.execute(query, values)
            self.database.connection.commit()
            messagebox.showinfo("Éxito", "Usuario agregado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el usuario: {str(e)}")

    def search_user(self):
        # Obtener el ID del usuario a buscar
        id_usuario = self.id_usuario_var.get()

        # Buscar el usuario en la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "SELECT * FROM usuarios WHERE id_usuario = %s"
            cursor.execute(query, (id_usuario,))
            usuario = cursor.fetchone()

            if usuario:
                self.nombre_var.set(usuario[1])
                self.correo_var.set(usuario[2])
                self.numero_var.set(usuario[3])
                messagebox.showinfo("Éxito", "Usuario encontrado")
            else:
                messagebox.showinfo("Información", "Usuario no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el usuario: {str(e)}")

    def update_user(self):
        # Obtener los valores actualizados de los campos
        id_usuario = self.id_usuario_var.get()
        nombre = self.nombre_var.get()
        correo = self.correo_var.get()
        numero = self.numero_var.get()

        # Actualizar el usuario en la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "UPDATE usuarios SET nombre = %s, correo = %s, numero = %s WHERE id_usuario = %s"
            values = (nombre, correo, numero, id_usuario)
            cursor.execute(query, values)
            self.database.connection.commit()
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el usuario: {str(e)}")

    def delete_user(self):
        # Obtener el ID del usuario a eliminar
        id_usuario = self.id_usuario_var.get()

        # Eliminar el usuario de la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "DELETE FROM usuarios WHERE id_usuario = %s"
            cursor.execute(query, (id_usuario,))
            self.database.connection.commit()
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el usuario: {str(e)}")

    def view_all_users(self):
        # Obtener todos los usuarios de la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "SELECT * FROM usuarios"
            cursor.execute(query)
            usuarios = cursor.fetchall()

            if usuarios:
                # Construir el mensaje con la información de los usuarios
                mensaje = ""
                for usuario in usuarios:
                    mensaje += f"ID: {usuario[0]}, Nombre: {usuario[1]}, Correo: {usuario[2]}, Número: {usuario[3]}\n"

                messagebox.showinfo("Lista de usuarios", mensaje)
            else:
                messagebox.showinfo("Información", "No hay usuarios registrados")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la lista de usuarios: {str(e)}")

    def clear_fields(self):
        self.id_usuario_var.set("")
        self.nombre_var.set("")
        self.correo_var.set("")
        self.numero_var.set("")

    def run(self):
        self.root.mainloop()






