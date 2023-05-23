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


class Lugares:
    def __init__(self, root, database):
        self.root = root
        self.database = database

        self.id_lugar_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.tipo_lugar_var = tk.StringVar()

        # Elementos de la interfaz
        self.id_lugar_label = tk.Label(root, text="ID:")
        self.id_lugar_entry = ttk.Entry(root, textvariable=self.id_lugar_var)
        self.direccion_label = tk.Label(root, text="Direccion:")
        self.direccion_entry = ttk.Entry(root, textvariable=self.direccion_var)
        self.tipo_lugar_label = tk.Label(root, text="Tipo lugar:")
        self.tipo_lugar_entry = ttk.Entry(root, textvariable=self.tipo_lugar_var)
        self.add_button = tk.Button(root, text="Agregar", command=self.add_place)
        self.search_button = tk.Button(root, text="Buscar", command=self.search_place)
        self.update_button = tk.Button(root, text="Actualizar", command=self.update_place)
        self.delete_button = tk.Button(root, text="Eliminar", command=self.delete_place)
        self.view_all_button = tk.Button(root, text="Ver todos", command=self.view_all_places)
        self.back_button = tk.Button(root, text="Regresar a Reservas", command=self.go_back_to_reservations)

        # Cargar la imagen
        self.image = Image.open("/Users/juanjo/Desktop/udem.png")
        self.image = self.image.resize((100, 100), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(root, image=self.photo)

        # Posicionamiento de los elementos
        self.id_lugar_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.id_lugar_entry.grid(row=0, column=1, padx=10, pady=5)
        self.direccion_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.direccion_entry.grid(row=1, column=1, padx=10, pady=5)
        self.tipo_lugar_label.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        self.tipo_lugar_entry.grid(row=4, column=1, padx=10, pady=5)
        self.add_button.grid(row=5, column=0, padx=5, pady=5)
        self.search_button.grid(row=5, column=1, padx=5, pady=5)
        self.update_button.grid(row=5, column=2, padx=5, pady=5)
        self.delete_button.grid(row=5, column=3, padx=5, pady=5)
        self.view_all_button.grid(row=5, column=4, padx=5, pady=5)
        self.back_button.grid(row=6, column=0, padx=10, pady=5)
        self.image_label.grid(row=0, column=5, rowspan=4, padx=10, pady=5, sticky=tk.NE)

        # Crear la conexión a la base de datos
        self.database = Database()



    def go_back_to_reservations(self):
        self.root.destroy()  # Cierra la ventana actual de Lugares

    def add_place(self):
        # Obtener los valores de los campos
        id_lugar = self.id_lugar_var.get()
        direccion = self.direccion_var.get()
        tipo_lugar = self.tipo_lugar_var.get()

        # Insertar el lugar en la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "INSERT INTO lugares (id_lugar, direccion, tipo_lugar) VALUES (%s, %s, %s)"
            values = (id_lugar, direccion, tipo_lugar)
            cursor.execute(query, values)
            self.database.connection.commit()
            messagebox.showinfo("Éxito", "Lugar agregado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el lugar: {str(e)}")

    def search_place(self):
        # Obtener el ID del lugar a buscar
        id_lugar = self.id_lugar_var.get()

        # Buscar el lugar en la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "SELECT * FROM lugares WHERE id_lugar = %s"
            cursor.execute(query, (id_lugar,))
            lugar = cursor.fetchone()

            if lugar:
                self.direccion_var.set(lugar[1])
                self.tipo_lugar_var.set(lugar[2])
                messagebox.showinfo("Éxito", "Lugar encontrado")
            else:
                messagebox.showinfo("Información", "Lugar no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el lugar: {str(e)}")

    def update_place(self):
        # Obtener los valores actualizados de los campos
        id_lugar = self.id_lugar_var.get()
        direccion = self.direccion_var.get()
        tipo_lugar = self.tipo_lugar_var.get()

        # Actualizar el lugar en la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "UPDATE lugares SET direccion = %s, tipo_lugar = %s WHERE id_lugar = %s"
            values = (direccion, tipo_lugar, id_lugar)
            cursor.execute(query, values)
            self.database.connection.commit()
            messagebox.showinfo("Éxito", "Lugar actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el lugar: {str(e)}")

    def delete_place(self):
        # Obtener el ID del lugar a eliminar
        id_lugar = self.id_lugar_var.get()

        # Eliminar el lugar de la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "DELETE FROM lugares WHERE id_lugar = %s"
            cursor.execute(query, (id_lugar,))
            self.database.connection.commit()
            messagebox.showinfo("Éxito", "Lugar eliminado correctamente")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el lugar: {str(e)}")

    def view_all_places(self):
        # Obtener todos los lugares de la base de datos
        try:
            cursor = self.database.connection.cursor()
            query = "SELECT * FROM lugares"
            cursor.execute(query)
            lugares = cursor.fetchall()

            if lugares:
                # Construir el mensaje con la información de los lugares
                mensaje = ""
                for lugar in lugares:
                    mensaje += f"ID: {lugar[0]}, Dirección: {lugar[1]}, Tipo de lugar: {lugar[2]}\n"

                messagebox.showinfo("Lista de lugares", mensaje)
            else:
                messagebox.showinfo("Información", "No hay lugares registrados")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la lista de lugares: {str(e)}")

    def clear_fields(self):
        self.id_lugar_var.set("")
        self.direccion_var.set("")
        self.tipo_lugar_var.set("")

    def run(self):
        self.root.mainloop()





