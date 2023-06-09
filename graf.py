import threading
import time
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Buffer():
    def __init__(self, que):
        self.buffer_list = []
        self.size = 0
        self.max_size = 600
        self.que = que

    def add_data(self, data):
        self.buffer_list.append(data)
        self.size += 1
        self.que.put(data)


class Que():
    def __init__(self):
        self.que = []
        self.size = 0
        self.lock = threading.Lock()

    def put(self, obs):
        self.lock.acquire()
        self.que.append(obs)
        self.size += 1
        self.lock.release()

    def get(self):
        self.lock.acquire()
        if self.size == 0:
            self.lock.release()
            return None

        obs = self.que.pop(0)
        self.size -= 1
        self.lock.release()
        return obs


class Sensor(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.que = que

    def load_data(self):
        with open("H_data.txt", "r") as file:
            line = file.readline()
            self.que.put(float(line))  # Send data direkte til køen som float-værdi

    def run(self):
        while True:
            self.load_data()
            time.sleep(0.5)


class DB(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.que = que

    def run(self):
        while True:
            obs = self.que.get()
            if obs is not None:
                # Lagre data i databasen
                pass
            time.sleep(0.1)


class Graph():
    def __init__(self, que):
        self.que = que
        self.data = []

    def plot_graph(self):
        obs = self.que.get()
        if obs is not None:
            self.data.append(obs)  # Gem data til plotning

            # Plot grafen ved hjælp af Matplotlib
            plt.clf()  # Clear the previous plot
            plt.plot(self.data)


class MyGraph(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.que = Que()
        self.graph = Graph(self.que)

        self.figure = plt.figure(figsize=(8, 6))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_graph(self):
        self.graph.plot_graph()
        self.canvas.draw()
        self.after(500, self.update_graph)


def main():
    root = tk.Tk()

    canvas = MyGraph(root)
    canvas.pack(fill="both", expand=True)

    sensor = Sensor(canvas.que)
    db = DB(canvas.que)

    # Start de andre tråde
    sensor.start()
    db.start()

    # Start opdatering af grafen
    canvas.update_graph()

    # Start hovedloop
    root.mainloop()


if __name__ == '__main__':
    main()
