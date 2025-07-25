import tkinter as tk
import sqlite3
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import serial
from sys import stdout
import queue

class Buffer():
    def __init__(self):
        self.list = []
        self.size = 0
        self.max = 600

    def addData(self, data):
        self.list.append(data)
        self.size += 1

    def getData(self):
        return = self.list

    def getLength(self):
        return = self.size


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
            print("Kommunikationsfejl 3", e)

def readSerialData(buffer, queue, db_send):
    arduino_port = '/dev/cu.usbmodem101'
    baud_rate = 38400

    ser = serial.Serial(arduino_port, baud_rate, timeout=1)

    run = True
    ser.setDTR(run)

    while run:
        try:
            data = ser.readline().decode().strip()
            if data:
                value = float(data)
                buffer.addData([value])
                queue.put(value)
                db_send.sendToDatabase(data)
                print(value)
            else:
                print(".", end="")
                stdout.flush()
        except KeyboardInterrupt:
            run = False
            break

    ser.setDTR(run)
    ser.close()

class Graph:
    def __init__(self, ax):
        self.buffer = []
        self.ax = ax

    def plot_graph(self, obs):
        self.buffer.extend(obs)
        if len(self.buffer) >= 600:
            x = list(range(len(self.buffer) - 600, len(self.buffer)))
            y = self.buffer[-600:]
            self.ax.clear()
            self.ax.plot(x, y)
            self.buffer = self.buffer[-600:]

class MyGraph(tk.Frame):
    def __init__(self, parent, buffer, data_queue):
        tk.Frame.__init__(self, parent)
        self.master = parent
        self.buffer = buffer
        self.data_queue = data_queue
        self.figure = plt.figure(figsize=(5, 2))
        self.ax = self.figure.add_subplot(111)
        self.ax.xaxis.set_visible(True)
        self.ax.yaxis.set_visible(True)
        self.ax.tick_params(axis='both', which='both', labelsize=8)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.graph = Graph(self.ax)

    def startGraphUpdate(self):
        self.updateGraph()

    def updateGraph(self):
        try:
            while True:
                data = self.data_queue.get(block=False)
                self.buffer.addData([data])
                self.graph.plot_graph([data])
        except queue.Empty:
            pass

        self.canvas.draw()
        self.master.after(1000, self.updateGraph)

def main():
    root = tk.Tk()
    buffer = Buffer()
    data_queue = queue.Queue()
    canvas = MyGraph(root, buffer, data_queue)
    canvas.pack(fill=tk.BOTH, expand=True)
    db = Database()

    # Start serial data reading in a separate thread
    serial_thread = threading.Thread(target=readSerialData, args=(buffer, data_queue, db))
    serial_thread.start()

    canvas.startGraphUpdate()

    root.mainloop()

if __name__ == '__main__':
    main()
