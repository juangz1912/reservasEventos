import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
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

    def close_connection(self):
        self.connection.close()

    def insert_reservation(self, reservation):
        cursor = self.connection.cursor()
        query = "INSERT INTO reservas (id, event_name, date, time, attendees) VALUES (%s, %s, %s, %s, %s)"
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

    def get_reservation_by_event_name(self, event_name):
        cursor = self.connection.cursor()
        query = "SELECT * FROM reservas WHERE event_name = %s"
        values = (event_name,)

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

    def delete_reservation_by_event_name(self, event_name):
        cursor = self.connection.cursor()
        query = "DELETE FROM reservas WHERE event_name = %s"
        values = (event_name,)

        try:
            cursor.execute(query, values)
            self.connection.commit()
            messagebox.showinfo("Reserva Eliminada", "La reserva ha sido eliminada exitosamente.")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo eliminar la reserva: {error}")
        finally:
            cursor.close()

    def get_all_reservations(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM reservas"

        try:
            cursor.execute(query)
            reservations = cursor.fetchall()
            if reservations:
                return [
                    {
                        'id': reservation[0],
                        'event_name': reservation[1],
                        'date': reservation[2],
                        'time': reservation[3],
                        'attendees': reservation[4]
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
        self.id_label = ttk.Label(root, text="ID:")
        self.id_entry = ttk.Entry(root, textvariable=self.id_var)
        self.event_name_label = ttk.Label(root, text="Nombre del evento:")
        self.event_name_entry = ttk.Entry(root, textvariable=self.event_name_var)
        self.date_label = ttk.Label(root, text="Fecha (dd/mm/aaaa):")
        self.date_entry = ttk.Entry(root, textvariable=self.date_var)
        self.time_label = ttk.Label(root, text="Hora (hh:mm):")
        self.time_entry = ttk.Entry(root, textvariable=self.time_var)
        self.attendees_label = ttk.Label(root, text="Asistentes:")
        self.attendees_entry = ttk.Entry(root, textvariable=self.attendees_var)
        self.add_button = tk.Button(root, text="Agregar", command=self.add_reservation)
        self.search_button = tk.Button(root, text="Buscar", command=self.search_reservation)
        self.delete_button = tk.Button(root, text="Eliminar", command=self.delete_reservation)
        self.view_all_button = tk.Button(root, text="Ver todos", command=self.view_all_reservations)

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
        self.delete_button.grid(row=5, column=2, padx=10, pady=5)
        self.view_all_button.grid(row=5, column=3, padx=10, pady=5)

        # Conexión a la base de datos
        self.database = Database()

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
        event_name = self.event_name_var.get()

        if event_name:
            reservation = self.database.get_reservation_by_event_name(event_name)

            if reservation:
                messagebox.showinfo("Reserva encontrada", f"ID: {reservation['id']}\n"
                                                           f"Nombre del evento: {reservation['event_name']}\n"
                                                           f"Fecha: {reservation['date']}\n"
                                                           f"Hora: {reservation['time']}\n"
                                                           f"Asistentes: {reservation['attendees']}")
            else:
                messagebox.showinfo("Reserva no encontrada", "No se encontró ninguna reserva con ese nombre de evento.")
        else:
            messagebox.showwarning("Advertencia", "Por favor ingresa el nombre del evento a buscar.")

    def delete_reservation(self):
        event_name = self.event_name_var.get()

        if event_name:
            confirmation = messagebox.askyesno("Confirmación", "¿Estás seguro/a de que deseas eliminar la reserva?")

            if confirmation:
                self.database.delete_reservation_by_event_name(event_name)
                self.clear_entries()
        else:
            messagebox.showwarning("Advertencia", "Por favor ingresa el nombre del evento a eliminar.")

    def view_all_reservations(self):
        reservations = self.database.get_all_reservations()

        if reservations:
            messagebox.showinfo("Todas las reservas", "\n".join(
                f"ID: {reservation['id']}, Nombre del evento: {reservation['event_name']}, "
                f"Fecha: {reservation['date']}, Hora: {reservation['time']}, Asistentes: {reservation['attendees']}"
                for reservation in reservations
            ))
        else:
            messagebox.showinfo("Todas las reservas", "No se encontraron reservas.")

    def clear_entries(self):
        self.id_var.set("")
        self.event_name_var.set("")
        self.date_var.set("")
        self.time_var.set("")
        self.attendees_var.set("")


root = tk.Tk()
app = EventReservationApp(root)
root.mainloop()







