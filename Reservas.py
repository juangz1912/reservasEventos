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
class Reservas:
    def __init__(self, root, database):
        self.root = root
        self.database = database

        self.id_reserva_var = tk.StringVar()
        self.id_lugar_var = tk.StringVar()
        self.id_usuario_var = tk.StringVar()
        self.id_evento_var = tk.StringVar()

        # Elementos de la interfaz
        self.id_reserva_label = tk.Label(root, text="ID Reserva: (solo poner en caso de busqueda)")
        self.id_reserva_entry = ttk.Entry(root, textvariable=self.id_reserva_var)
        self.id_lugar_label = tk.Label(root, text="ID Lugar:")
        self.id_lugar_entry = ttk.Entry(root, textvariable=self.id_lugar_var)
        self.id_usuario_label = tk.Label(root, text="ID Usuario:")
        self.id_usuario_entry = ttk.Entry(root, textvariable=self.id_usuario_var)
        self.id_evento_label = tk.Label(root, text="ID Evento:")
        self.id_evento_entry = ttk.Entry(root, textvariable=self.id_evento_var)
        self.count_users_button = tk.Button(root, text="Contar Usuarios", command=self.count_users)
        self.count_reservations_button = tk.Button(root, text="Contar Reservas", command=self.count_reservations)
        self.create_button = tk.Button(root, text="Crear Reserva", command=self.create_reservation)
        self.read_button = tk.Button(root, text="Leer Reserva", command=self.read_reservation)
        self.update_button = tk.Button(root, text="Actualizar Reserva", command=self.update_reservation)
        self.delete_button = tk.Button(root, text="Eliminar Reserva", command=self.delete_reservation)

        # Cargar la imagen
        self.image = Image.open("/Users/juanjo/Desktop/udem.png")
        self.image = self.image.resize((100, 100), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(root, image=self.photo)

        # Posicionamiento de los elementos
        self.id_reserva_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.id_reserva_entry.grid(row=0, column=1, padx=10, pady=5)
        self.id_lugar_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.id_lugar_entry.grid(row=1, column=1, padx=10, pady=5)
        self.id_usuario_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.id_usuario_entry.grid(row=2, column=1, padx=10, pady=5)
        self.id_evento_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.id_evento_entry.grid(row=3, column=1, padx=10, pady=5)
        self.count_users_button.grid(row=4, column=0, padx=10, pady=5)
        self.count_reservations_button.grid(row=4, column=1, padx=10, pady=5)
        self.create_button.grid(row=5, column=0, padx=10, pady=5)
        self.read_button.grid(row=5, column=1, padx=10, pady=5)
        self.update_button.grid(row=6, column=0, padx=10, pady=5)
        self.delete_button.grid(row=6, column=1, padx=10, pady=5)

        # Crear la conexión a la base de datos
        self.database = database

    def count_users(self):
        # Obtener el ID de la reserva
        id_reserva = self.id_reserva_var.get()

        # Contar los usuarios en la reserva


    def count_reservations(self):
        # Obtener el ID del usuario
        id_usuario = self.id_usuario_var.get()

        # Contar las reservas del usuario


    def create_reservation(self):
        # Obtener los datos de la reserva
        id_lugar = self.id_lugar_var.get()
        id_usuario = self.id_usuario_var.get()
        id_evento = self.id_evento_var.get()

        # Crear una nueva reserva en la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "INSERT INTO reservas (id_lugar, id_usuario, id_evento) VALUES (%s, %s, %s)"
            cursor.execute(query, (id_lugar, id_usuario, id_evento))
            self.database.connection.commit()

            messagebox.showinfo("Creación Exitosa", "La reserva se ha creado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la reserva: recuerda poner solo id de las otras tablas")

    def read_reservation(self):
        # Obtener el ID de la reserva
        id_reserva = self.id_reserva_var.get()

        # Leer los datos de la reserva desde la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "SELECT id_lugar, id_usuario, id_evento FROM reservas WHERE id_reserva = %s"
            cursor.execute(query, (id_reserva,))
            data = cursor.fetchone()

            if data:
                id_lugar, id_usuario, id_evento = data
                self.id_lugar_var.set(id_lugar)
                self.id_usuario_var.set(id_usuario)
                self.id_evento_var.set(id_evento)
                messagebox.showinfo("Lectura Exitosa", "Datos de reserva cargados correctamente")
            else:
                messagebox.showinfo("Reserva no encontrada", f"No se encontró la reserva con ID {id_reserva}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer la reserva: {str(e)}")

    def update_reservation(self):
        # Obtener los datos actualizados de la reserva
        id_reserva = self.id_reserva_var.get()
        id_lugar = self.id_lugar_var.get()
        id_usuario = self.id_usuario_var.get()
        id_evento = self.id_evento_var.get()

        # Actualizar los datos de la reserva en la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "UPDATE reservas SET id_lugar = %s, id_usuario = %s, id_evento = %s WHERE id_reserva = %s"
            cursor.execute(query, (id_lugar, id_usuario, id_evento, id_reserva))
            self.database.connection.commit()

            messagebox.showinfo("Actualización Exitosa", "La reserva se ha actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la reserva: {str(e)}")

    def delete_reservation(self):
        # Obtener el ID de la reserva a eliminar
        id_reserva = self.id_reserva_var.get()

        # Eliminar la reserva de la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "DELETE FROM reservas WHERE id_reserva = %s"
            cursor.execute(query, (id_reserva,))
            self.database.connection.commit()

            messagebox.showinfo("Eliminación Exitosa", "La reserva se ha eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la reserva: {str(e)}")

    def run(self):
        self.root.mainloop()
