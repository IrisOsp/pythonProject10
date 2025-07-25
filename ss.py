import threading
import serial
import time
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
from puls import *

class Sensor:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate, timeout=10)  # Opretter et serielt objekt til at kommunikere med sensoren

    def read_data(self):
        return self.ser.readline().decode().strip()  # Læser en linje fra sensoren og returnerer en streng uden mellemrum

class Buffer:
    def __init__(self):
        self.data = None  # Datafelt til midlertidig opbevaring af data
        self.lock = threading.Lock()  # Lås til sikker adgang til datafeltet fra flere tråde
        self.condition = threading.Condition(lock=self.lock)  # Betingelse for at vente og signalere mellem tråde

    def put(self, data):
        with self.lock:
            self.data = data  # Placerer data i bufferen
            self.condition.notify()  # Vækker en ventende tråd

    def get(self):
        with self.lock:
            while self.data is None:  # Venter, indtil der er data tilgængelig i bufferen
                self.condition.wait()
            data = self.data  # Henter data fra bufferen
            self.data = None  # Nulstiller datafeltet til at være tomt igen
            return data

class Queue:
    def __init__(self):
        self.queue = []  # Tom liste til at repræsentere køen
        self.lock = threading.Lock()  # Lås til sikker adgang til køen fra flere tråde

    def put(self, data):
        with self.lock:
            self.queue.append(data)  # Tilføjer data til køen

    def get(self):
        with self.lock:
            if self.queue:
                return self.queue.pop(0)  # Fjerner og returnerer det første element i køen
            else:
                return None  # Hvis køen er tom, returneres 'None'

class PulseBox(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Puls')
        self.grid(row=1, column=1, rowspan=1, columnspan=1, sticky='nswe')
        self.pulse_label = PulseLabel(self)
        self.pulse_label.configure(bg="white")
        self.pulse_label.pack(fill='both', expand=True)

class PulseLabel(tk.Label):
    def __init__(self, parent):
        super().__init__(parent, bg="white", fg="green", width=10, height=2)
        self.config(font=("Helvetica", 20))
        self.update_pulse()

    def update_pulse(self):
        value = round(puls.getVitals())  # Erstatter 'puls.getVitals()' med rigtig kilde for pulsdata'en
        self.config(text=value)  # Opdaterer teksten i widgetten med den nye værdi
        self.after(1000, self.update_pulse)  # Planlægger en gentagen opdatering af pulsdata for hvert sekund

class SensorApp:
    def __init__(self, master, port, baudrate):
        self.master = master
        self.master.title("Sensor Data Plot")
        self.master.geometry("1200x400")

        self.sensor = Sensor(port, baudrate)  # Opretter en Sensor-klasse med givet port og baudrate
        self.buffer = Buffer()  # Opretter en Buffer-klasse
        self.queue = Queue()  # Opretter en Queue-klasse
        self.running = False  # Programmets tilstand, der angiver om programmet kører
        self.connection = None  # SQLite-forbindelse

        self.fig = Figure(figsize=(10, 3), dpi=100)  # Opretter en figur til plot
        self.ax = self.fig.add_subplot(111)  # Opretter en enkelt akse til plot
        self.ax.set_xlabel("")  # Sætter x-akse-label til ingenting
        self.ax.set_ylabel("Sensor Data")  # Sætter y-akse-label til "Sensor Data"

        self.x_data, self.y_data = [], []  # Tomme lister til x- og y-data
        self.line, = self.ax.plot(self.x_data, self.y_data)  # Opretter en linjeplot-linje til dataene

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)  # Opretter en Canvas-widget til at vise figuren
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")  # Placerer figuren på GUI'en

        self.search_entry = ttk.Entry(self.master)  # Opretter en skriftboks til søgning
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Placerer indtastningsboksen på GUI'en
        search_button = ttk.Button(self.master, text="Søg Patient", command=self.search_data)  # Opretter en knap til søgning
        search_button.grid(row=0, column=0, padx=10, pady=10, sticky="e")  # Placerer søgeknappen på GUI'en

        self.text_box = tk.Text(self.master, height=2, width=40)  # Opretter et tekstfelt til resultatvisning
        self.text_box.grid(row=0, column=1, padx=10, pady=10, sticky="w")  # Placerer tekstfeltet på GUI'en

    def start(self):
        self.running = True  # Tilstand, der angiver at programmet kører
        self.connection = sqlite3.connect("EKG_data.db")  # Opretter forbindelse til SQLite-databasen
        threading.Thread(target=self.read_sensor).start()  # Starter en separat tråd til at læse data fra sensoren
        threading.Thread(target=self.update_plot).start()  # Starter en separat tråd til at opdatere plottet

    def stop(self):
        self.running = False  # Tilstand, der angiver at programmet skal stoppe
        self.buffer.put(None)  # Indsætter et stopsignal i bufferen for at stoppe update_plot-tråden
        self.connection.close()  # Lukker SQLite-forbindelsen
        self.master.destroy()  # Lukker GUI-vinduet

    def read_sensor(self):
        connection = sqlite3.connect("EKG_data.db")  # Opretter forbindelse til SQLite-databasen
        while self.running:  # Kører indtil programmet er stoppet
            data = self.sensor.read_data()  # Læser data fra sensoren
            self.buffer.put(data)  # Indsætter data i bufferen til plot-opdatering

            timestamp = time.time()  # Henter tidsstempel til dataen
            cursor = connection.cursor()  # Opretter en databasecursor
            cursor.execute("INSERT INTO målinger(EKG) VALUES(?)", (data,))  # Indsætter data i databasen med tidsstempel
            connection.commit()  # Gemmer ændringerne i databasen
            cursor.close()  # Lukker databasen

            print("Sensor data:", data)  # Udskriver værdien, der er læst fra sensoren

        connection.close()  # Lukker SQLite-forbindelsen

    def update_plot(self):
        buffer_size = 600  # Størrelse af bufferen til x- og y-data
        while self.running:  # Kører indtil programmet er stoppet
            data = self.buffer.get()  # Henter data fra bufferen
            if data is None:  # Tjekker om der er modtaget et stopsignal
                break

            self.queue.put(data)  # Indsætter data i køen til plot-opdatering

            x_data = []  # Liste til x-data
            y_data = []  # Liste til y-data
            while True:  # Fortsætter indtil der ikke er mere data i køen
                data = self.queue.get()  # Henter data fra køen
                if data is None:  # Tjekker om der er modtaget et stopsignal
                    break
                x_data.append(time.time())  # Tilføjer tidsstempel til x-data
                y_data.append(float(data))  # Konverterer data til flydende tal og tilføjer til y-data

            if len(x_data) == 0:  # Tjekker om der er data til plot-opdatering
                time.sleep(0.1)
                continue

            self.x_data.extend(x_data)  # Udvider x-data med de nye data
            self.y_data.extend(y_data)  # Udvider y-data med de nye data

            max_data_points = 600  # Maksimalt antal datapunkter i plottet
            if len(self.x_data) > max_data_points:  # Tjekker om antallet af datapunkter er større end maksimum
                self.x_data = self.x_data[-max_data_points:]  # Beholder kun de seneste datapunkter
                self.y_data = self.y_data[-max_data_points:]  # Beholder kun de seneste datapunkter

            if len(self.x_data) >= buffer_size:  # Tjekker om bufferen er fyldt
                start_index = len(self.x_data) - buffer_size  # Bestemmer startindeks for x- og y-data
                self.line.set_data(self.x_data[start_index:], self.y_data[start_index:])  # Opdaterer linjen i plottet

                self.ax.relim()  # Opdaterer plottets grænser
                self.ax.autoscale_view(scalex=True, scaley=True)  # Justerer skalaen for x- og y-aksen

                self.fig.canvas.draw()  # Opdaterer plottet i figuren

    def search_data(self):
        keyword = self.search_entry.get()  # Henter søgeordet fra indtastningsboksen
        self.text_box.delete("1.0", tk.END)  # Sletter tidligere resultat fra tekstfeltet

        cursor = self.connection.cursor()  # Opretter en databasecursor
        cursor.execute("SELECT * FROM person WHERE person_id=?", (keyword,))  # Henter data fra databasen baseret på søgeordet
        rows = cursor.fetchall()  # Henter alle rækker fra resultatet
        for row in rows:  # Gennemløber hver række
            self.text_box.insert(tk.END, str(row) + '\n')  # Indsætter række i tekstfeltet
        cursor.close()  # Lukker databasen

if __name__ == "__main__":
    root = tk.Tk()  # Opretter et GUI-vindue
    app = SensorApp(root, "/dev/cu.usbmodem101", 38400)  # Opretter en SensorApp-instans
    app.start()  # Starter programmet
    pulse_box = PulseBox(root)  # Opretter en PulseBox-widget
    pulse_box.grid(row=1, column=0, sticky='nswe')  # Placerer PulseBox-widget'en på GUI'en
    root.protocol("WM_DELETE_WINDOW", app.stop)  # Tilføjer stop-metoden til lukningshandlingen
    root.mainloop()  # Starter GUI-loopet