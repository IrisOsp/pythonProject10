import tkinter as tk
from threading import Thread, Condition
import sqlite3
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Buffer():
    def __init__(self):
        self.list = []
        self.size = 0
        self.max = 600

    def addData(self, data):
        self.list.extend(data)
        self.size += len(data)

b = Buffer()

class Sensor():
    def getData(self):
        file = open("H_data.txt", "r")
        lines = file.readlines()
        file.close()

        data = []
        for line in lines:
            data.append(float(line.strip()))
        return data

s = Sensor()
data = s.getData()
b.addData(data)


class que():
    def __init__(self, buffer):
        self._buffer = buffer
        self._empty, self._value = True, None
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

            # Hvis que har nået sin maksimumskapacitet, henter vi værdier fra bufferen
            if len(self._buffer.list) >= self._buffer.max:
                data = self._buffer.list[:self._buffer.max]
                self._buffer.list = self._buffer.list[self._buffer.max:]
                self._buffer.size -= len(data)
                self._value = data
                self._empty = False

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

def sensor_thread_func(buffer, queue, db_send):
    while True:
        data = s.getData()
        buffer.addData(data)
        queue.putData(data)
        for item in data:
            db_send.sendToDatabase(item)

def graph_thread_func(queue, canvas):
    while True:
        data = queue.getData()
        canvas.plot_graph(data)

class Graph:
    def __init__(self, ax):
        self.buffer = []
        self.ax = ax

    def plot_graph(self, obs):
        self.buffer.extend(obs)
        if len(self.buffer) >= 800:
            x = list(range(len(self.buffer) - 800, len(self.buffer)))
            y = self.buffer[-800:]
            self.ax.clear()
            self.ax.plot(x, y)
            self.buffer = self.buffer[-800:]

class MyGraph(tk.Frame):
    def __init__(self, master, buffer):
        tk.Frame.__init__(self, master)
        self.master = master
        self.buffer = buffer
        self.que = que(self.buffer)
        self.figure = plt.figure(figsize=(5, 2))
        self.ax = self.figure.add_subplot(111)
        self.ax.xaxis.set_visible(True)
        self.ax.yaxis.set_visible(True)
        self.ax.tick_params(axis='both', which='both', labelsize=8)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.graph = Graph(self.ax)

    def update_graph(self):
        data = self.que.getData()
        self.graph.plot_graph(data)
        self.canvas.draw()
        self.after(1000, self.update_graph)

def main():
    root = tk.Tk()
    buffer = Buffer()
    canvas = MyGraph(root, buffer)
    canvas.pack(fill=tk.BOTH, expand=True)
    db = Database()
    queue = que(buffer)  # Send buffer til que-konstruktøren

    sensor_thread = Thread(target=sensor_thread_func, args=(buffer, canvas.que, db))
    sensor_thread.start()

    graph_thread = Thread(target=graph_thread_func, args=(canvas.que, canvas.graph))
    graph_thread.start()

    canvas.update_graph()

    root.mainloop()


if __name__ == '__main__':
    main()









