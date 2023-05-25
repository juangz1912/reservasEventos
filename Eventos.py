import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import mysql.connector
from PIL import ImageTk, Image
import Lugares
import Usuarios
import Reservas

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

    def close_connection(self):
        self.connection.close()

    def insert_reservation(self, reservation):
        cursor = self.connection.cursor()
        query = "INSERT INTO eventos (id, event_name, date, time, attendees) VALUES (%s, %s, %s, %s, %s)"
        values = (
            reservation['id'],
            reservation['event_name'],
            reservation['date'],
            reservation['time'],
            reservation['attendees']
        )

        try:
            cursor.execute(query, values)
            self.connection.commit()
            messagebox.showinfo("Reserva Agregada", "La reserva ha sido agregada exitosamente.")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo agregar la reserva: {error}")
        finally:
            cursor.close()

    def get_reservation_by_id(self, id):
        cursor = self.connection.cursor()
        query = "SELECT * FROM eventos WHERE id = %s"
        values = (id,)

        try:
            cursor.execute(query, values)
            reservation = cursor.fetchone()
            if reservation:
                return {
                    'id': reservation[0],
                    'event_name': reservation[1],
                    'date': reservation[2],
                    'time': reservation[3],
                    'attendees': reservation[4]
                }
            else:
                return None
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo buscar la reserva: {error}")
        finally:
            cursor.close()

    def delete_reservation_by_id(self, id):
        cursor = self.connection.cursor()
        query = "DELETE FROM eventos WHERE id = %s"
        values = (id,)

        try:
            cursor.execute(query, values)
            self.connection.commit()
            messagebox.showinfo("Reserva Eliminada", "La reserva ha sido eliminada exitosamente.")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo eliminar la reserva: {error}")
        finally:
            cursor.close()

    def update_reservation(self, reservation):
        cursor = self.connection.cursor()
        query = "UPDATE eventos SET id = %s, event_name = %s, date = %s, time = %s, attendees = %s WHERE event_name = %s"
        values = (
            reservation['id'],
            reservation['event_name'],
            reservation['date'],
            reservation['time'],
            reservation['attendees'],
            reservation['event_name']  # Utilizamos el nombre del evento como criterio de búsqueda para actualizar
        )

        try:
            cursor.execute(query, values)
            self.connection.commit()
            messagebox.showinfo("Reserva Actualizada", "La reserva ha sido actualizada exitosamente.")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo actualizar la reserva: {error}")
        finally:
            cursor.close()

    def get_all_reservations(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM eventos"

        try:
            cursor.execute(query)
            reservations = cursor.fetchall()
            if reservations:
                return [
                    {
                        'id': reservation[0],
                        'event_name': reservation[1]
                    }
                    for reservation in reservations
                ]
            else:
                return []
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo obtener las reservas: {error}")
        finally:
            cursor.close()

class EventReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reserva de Eventos")


        # Variables de entrada
        self.id_var = tk.StringVar()
        self.event_name_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.attendees_var = tk.StringVar()

        # Elementos de la interfaz
        self.id_label = tk.Label(root, text="ID:")
        self.id_entry = ttk.Entry(root, textvariable=self.id_var)
        self.event_name_label = tk.Label(root, text="Nombre del evento:")
        self.event_name_entry = ttk.Entry(root, textvariable=self.event_name_var)
        self.date_label = tk.Label(root, text="Fecha (dd/mm/aaaa):")
        self.date_entry = ttk.Entry(root, textvariable=self.date_var)
        self.time_label = tk.Label(root, text="Hora (hh:mm):")
        self.time_entry = ttk.Entry(root, textvariable=self.time_var)
        self.attendees_label = tk.Label(root, text="Asistentes:")
        self.attendees_entry = ttk.Entry(root, textvariable=self.attendees_var)
        self.add_button = tk.Button(root, text="Agregar", command=self.add_reservation)
        self.search_button = tk.Button(root, text="Buscar", command=self.search_reservation)
        self.update_button = tk.Button(root, text="Actualizar", command=self.update_reservation)
        self.delete_button = tk.Button(root, text="Eliminar", command=self.delete_reservation)
        self.view_all_button = tk.Button(root, text="Ver todos", command=self.view_all_reservations)

        # Cargar la imagen
        self.image = Image.open("/Users/juanjo/Desktop/udem.png")
        self.image = self.image.resize((100, 100), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(root, image=self.photo)

        # Posicionamiento de los elementos
        self.id_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5)
        self.event_name_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.event_name_entry.grid(row=1, column=1, padx=10, pady=5)
        self.date_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.date_entry.grid(row=2, column=1, padx=10, pady=5)
        self.time_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.time_entry.grid(row=3, column=1, padx=10, pady=5)
        self.attendees_label.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        self.attendees_entry.grid(row=4, column=1, padx=10, pady=5)
        self.add_button.grid(row=5, column=0, padx=10, pady=5)
        self.search_button.grid(row=5, column=1, padx=10, pady=5)
        self.update_button.grid(row=5, column=2, padx=10, pady=5)
        self.delete_button.grid(row=5, column=3, padx=10, pady=5)
        self.view_all_button.grid(row=5, column=4, padx=10, pady=5)
        self.image_label.grid(row=0, column=5, rowspan=4, padx=10, pady=5, sticky=tk.NE)

        # Conexión a la base de datos
        self.database = Database()

        #ventanas
        self.lugares_button = tk.Button(root, text="Gestionar Lugares", command=self.open_new_window)
        self.lugares_button.grid(row=6, column=0, padx=10, pady=5)

        self.usuarios_button = tk.Button(root, text="Gestionar Usuarios", command=self.open_usuarios_window)
        self.usuarios_button.grid(row=6, column=1, padx=10, pady=5)

        self.reservas_button = tk.Button(root, text="Gestionar Reservas", command=self.open_reservas_window)
        self.reservas_button.grid(row=6, column=2, padx=10, pady=5)

    def open_new_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Gestión de Lugares")
        lugares_instance = Lugares.Lugares(new_window, self.database) # Crea una instancia de la clase Lugares
        lugares_instance.run()

    def open_usuarios_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Gestión de Usuarios")
        usuarios_instance = Usuarios.Usuarios(new_window, self.database)  # Crea una instancia de la clase Usuarios
        usuarios_instance.run()

    def open_reservas_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Gestión de Reservas")
        reservas_instance = Reservas.Reservas(new_window, self.database)  # Crea una instancia de la clase Reservas
        reservas_instance.run()

    def add_reservation(self):
        id = self.id_var.get()
        event_name = self.event_name_var.get()
        date_str = self.date_var.get()
        time_str = self.time_var.get()
        attendees = self.attendees_var.get()

        if id and event_name and date_str and time_str and attendees:
            try:
                date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
                date_int = date_obj.strftime("%Y%m%d")

                time_obj = datetime.datetime.strptime(time_str, "%H:%M")
                time_int = time_obj.strftime("%H%M")

                reservation = {
                    'id': id,
                    'event_name': event_name,
                    'date': date_int,
                    'time': time_int,
                    'attendees': attendees
                }

                self.database.insert_reservation(reservation)

                self.clear_entries()
            except ValueError:
                messagebox.showerror("Error", "Fecha u hora inválida. Utiliza el formato correcto.")
        else:
            messagebox.showwarning("Advertencia", "Por favor completa todos los campos.")

    def search_reservation(self):
        id = self.id_var.get()

        if id:
            reservation = self.database.get_reservation_by_id(id)

            if reservation:
                self.id_var.set(reservation['id'])
                self.event_name_var.set(reservation['event_name'])
                self.date_var.set(reservation['date'])
                self.time_var.set(reservation['time'])
                self.attendees_var.set(reservation['attendees'])

                messagebox.showinfo("Evento encontrado", f"Se encontró la reserva con el ID: {reservation['id']}")
            else:
                messagebox.showinfo("Evento no encontrado", "No se encontró ninguna reserva con ese ID.")
        else:
            messagebox.showwarning("Advertencia", "Por favor ingresa el ID de la reserva a buscar.")

    def update_reservation(self):
        id = self.id_var.get()
        event_name = self.event_name_var.get()
        date_str = self.date_var.get()
        time_str = self.time_var.get()
        attendees = self.attendees_var.get()

        if id and event_name and date_str and time_str and attendees:
            try:
                date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
                date_int = date_obj.strftime("%Y%m%d")

                time_obj = datetime.datetime.strptime(time_str, "%H:%M")
                time_int = time_obj.strftime("%H%M")

                reservation = {
                    'id': id,
                    'event_name': event_name,
                    'date': date_int,
                    'time': time_int,
                    'attendees': attendees
                }

                self.database.update_reservation(reservation)

                self.clear_entries()
            except ValueError:
                messagebox.showerror("Error", "Fecha u hora inválida. Utiliza el formato correcto.")
        else:
            messagebox.showwarning("Advertencia", "Por favor completa todos los campos.")

    def delete_reservation(self):
        id = self.id_var.get()

        if id:
            confirmation = messagebox.askyesno("Confirmación", f"¿Estás seguro/a de eliminar la reserva '{id}'?")
            if confirmation:
                self.database.delete_reservation_by_id(id)
                self.clear_entries()
        else:
            messagebox.showwarning("Advertencia", "Por favor ingresa el id del evento a eliminar.")

    def view_all_reservations(self):
        reservations = self.database.get_all_reservations()

        if reservations:
            messagebox.showinfo("Todos los eventos", "\n".join([f"ID: {reservation['id']}, Nombre del evento: {reservation['event_name']}"
                                                                 for reservation in reservations]))
        else:
            messagebox.showinfo("Todos los eventos", "No se encontraron reservas.")

    def clear_entries(self):
        self.id_var.set("")
        self.event_name_var.set("")
        self.date_var.set("")
        self.time_var.set("")
        self.attendees_var.set("")

    def run(self):
        self.root.mainloop()

root = tk.Tk()
app = EventReservationApp(root)
app.run()

