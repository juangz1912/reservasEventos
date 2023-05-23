import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
import datetime

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

        # Estilos
        self.style = ttk.Style()
        self.style.configure("TEntry", font=("Arial", 12))
        self.style.configure("TButton", font=("Arial", 12))

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
        self.add_button = ttk.Button(root, text="Agregar", command=self.add_reservation)
        self.search_button = ttk.Button(root, text="Buscar", command=self.search_reservation)
        self.delete_button = ttk.Button(root, text="Eliminar", command=self.delete_reservation)

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

        # Conexión a la base de datos
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

    def add_reservation(self):
        id = self.id_var.get()
        event_name = self.event_name_var.get()
        date_str = self.date_var.get()
        time_str = self.time_var.get()
        attendees = self.attendees_var.get()

        # Validar que todos los campos estén completos
        if id and event_name and date_str and time_str and attendees:
            try:
                # Convertir la fecha al formato de número entero
                date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
                date_int = date_obj.strftime("%Y%m%d")

                # Convertir la hora al formato de número entero
                time_obj = datetime.datetime.strptime(time_str, "%H:%M")
                time_int = time_obj.strftime("%H%M")

                cursor = self.connection.cursor()

                # Verificar si ya existe un evento con el mismo ID
                query = "SELECT * FROM reservas WHERE id = %s"
                values = (id,)
                cursor.execute(query, values)
                existing_event = cursor.fetchone()

                if existing_event:
                    messagebox.showerror("Error", "Ya existe un evento con el mismo ID.")
                else:
                    # Verificar si ya existe un evento con el mismo nombre
                    query = "SELECT * FROM reservas WHERE event_name = %s"
                    values = (event_name,)
                    cursor.execute(query, values)
                    existing_event = cursor.fetchone()

                    if existing_event:
                        messagebox.showerror("Error", "Ya existe un evento con el mismo nombre.")
                    else:
                        # Ejemplo de consulta INSERT
                        query = "INSERT INTO reservas (id, event_name, date, time, attendees) VALUES (%s, %s, %s, %s, %s)"
                        values = (id, event_name, date_int, time_int, attendees)
                        cursor.execute(query, values)

                        self.connection.commit()
                        cursor.close()

                        messagebox.showinfo("Reserva Agregada", "La reserva ha sido agregada exitosamente.")

                        # Limpiar los campos después de agregar
                        self.id_var.set("")
                        self.event_name_var.set("")
                        self.date_var.set("")
                        self.time_var.set("")
                        self.attendees_var.set("")
            except ValueError:
                messagebox.showerror("Error", "Por favor, introduce valores válidos en los campos de fecha (dd/mm/aaaa) y hora (hh:mm).")
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos antes de agregar una reserva.")

    def search_reservation(self):
        event_name = self.event_name_var.get()

        cursor = self.connection.cursor()

        # Ejemplo de consulta SELECT
        query = "SELECT * FROM reservas WHERE event_name = %s"
        values = (event_name,)
        cursor.execute(query, values)
        reservation = cursor.fetchone()

        if reservation:
            self.id_var.set(reservation[0])
            self.date_var.set(reservation[2])
            self.time_var.set(reservation[3])
            self.attendees_var.set(reservation[4])
        else:
            messagebox.showerror("Error", "No se encontró ninguna reserva con el nombre de evento especificado.")

        cursor.close()

    def delete_reservation(self):
        event_name = self.event_name_var.get()

        cursor = self.connection.cursor()

        # Ejemplo de consulta DELETE
        query = "DELETE FROM reservas WHERE event_name = %s"
        values = (event_name,)
        cursor.execute(query, values)

        self.connection.commit()
        cursor.close()

        messagebox.showinfo("Reserva Eliminada", "La reserva ha sido eliminada exitosamente.")

        # Limpiar los campos después de eliminar
        self.id_var.set("")
        self.event_name_var.set("")
        self.date_var.set("")
        self.time_var.set("")
        self.attendees_var.set("")

    def close_connection(self):
        # Cerrar la conexión cuando se cierre la ventana
        self.connection.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = EventReservationApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_connection)
    root.mainloop()




