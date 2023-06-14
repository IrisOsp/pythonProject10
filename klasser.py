import tkinter
import tkinter as tk
from threading import Thread, Condition
import sqlite3

class Buffer():
    def __init__(self):
        self.list = []
        self.size = 0
        self.max = 600

    def addData(self, data):
        self.list.extend(data)
        self.size += 1

b = Buffer()

class Sensor():
    def getData(self):
        file = open("H_data.txt", "r")
        lines = file.readlines()
        file.close()

        data = []
        for line in lines:
            data.append(float(line[:-2]))
        return data

s = Sensor()
data = s.getData()
b.addData(data)
# print(b.list)


class que():
    def __init__(self):
        self._empty, self._value = True, 0
        self._lock = Condition()

    def getData(self):
        with self._lock:
            while self._empty:
                self._lock.wait()
            self._empty = True
            self._lock.notify()
            return self._value

    def putData(self, value):
        with self._lock:
            self._value, self._empty = value, False
            self._lock.notify()


class Database:
    def sendToDatabase(self, ekg):
        try:
            conn = sqlite3.connect('EKG_Data.db')
            c = conn.cursor()
            c.execute("INSERT INTO målinger(EKG) VALUES(?)", (ekg,))
            conn.commit()
            c.close()
            conn.close()

        except sqlite3.Error as e:
            print("Kommunikationsfejl 3")



def sensor_thread_func(buffer, queue, sender):
    s = Sensor()
    data = s.getData()
    buffer.addData(data)
    queue.putData(data)
    sender.plot_graph(data)
    # Send hvert element fra listen til databasen
    for item in data:
        sender.sendToDatabase(item)

class Graph:
    def __init__(self, que, ax):
        self.que = que
        self.buffer = []
        self.ax = ax

    def plot_graph(self):
        obs = self.que.get()
        if obs is not None:
            self.buffer.extend(obs)
            if len(self.buffer) >= 800:
                x = list(range(len(self.buffer) - 800, len(self.buffer)))  # X-værdier for de seneste 6 værdier
                y = self.buffer[-800:]  # De seneste 6 værdier
                self.ax.clear()
                self.ax.plot(x, y)
                self.buffer = self.buffer[6:]



class MyGraph(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.que = que()
        self.figure = plt.figure(figsize=(5, 2))
        self.ax = self.figure.add_subplot(111)
        self.ax.xaxis.set_visible(True)
        self.ax.yaxis.set_visible(True)
        self.ax.tick_params(axis='both', which='both', labelsize=8)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.graph = Graph(self.que, self.ax)  # Opretter Graph-objektet

    def update_graph(self):
        self.graph.plot_graph()
        self.canvas.draw()
        self.after(1000, self.update_graph)

db_send = Database()
graf_send = Graph()

q_database = que()
q_graf = que()

# Oppretter en tråd for å hente data fra sensoren og legge dem til i bufferet og q1

sensor_thread1 = Thread(target=sensor_thread_func, args=(b, q_database, db_send, graf_send))
sensor_thread1.start()


# Henter data fra q_database
print(q_database.getData())

#Laves til graf senere


# Henter data fra q_graf
print(q_graf.getData())

sensor_thread2 = Thread(target=sensor_thread_func, args=(b, q_database, graf_send, db_send))
sensor_thread2.start()

