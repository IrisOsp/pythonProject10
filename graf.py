import threading
import time
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Buffer:
    def __init__(self, que):
        self.buffer_list = []
        self.size = 0
        self.max_size = 1200
        self.que = que

    def add_data(self, data):
        self.buffer_list.append(data)
        self.size += 1
        if self.size == 1200:
            self.que.put(self.buffer_list[:])  # Send en kopi af de seneste 12 observationer
            self.buffer_list = []
            self.size = 0

class Que:
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
    def __init__(self, que, buffer):
        threading.Thread.__init__(self)
        self.que = que
        self.buffer = buffer

    def load_data(self):
        with open("h_data.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    try:
                        data = list(map(float, line.split()))  # Ændret til at håndtere flere tal ad gangen
                        self.buffer.add_data(data)
                    except ValueError:
                        print("Invalid data:", repr(line))

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
                pass
            time.sleep(0.5)


class Graph:
    def __init__(self, que, ax):
        self.que = que
        self.buffer = []
        self.ax = ax

    def plot_graph(self):
        obs = self.que.get()
        if obs is not None:
            self.buffer.extend(obs)
            if len(self.buffer) >= 1200:
                x = list(range(len(self.buffer) - 1200, len(self.buffer)))  # X-værdier for de seneste 6 værdier
                y = self.buffer[-1200:]  # De seneste 6 værdier
                self.ax.clear()
                self.ax.plot(x, y)
                self.buffer = self.buffer[6:]


class MyGraph(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.que = Que()
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



def main():
    root = tk.Tk()

    canvas = MyGraph(root)
    canvas.pack(fill="both", expand=True)

    sensor = Sensor(canvas.que, Buffer(canvas.que))
    db = DB(canvas.que)

    canvas.after(1000, canvas.update_graph)  # Opdater grafen efter 1 sekund

    sensor.start()
    db.start()

    root.mainloop()


if __name__ == '__main__':
    main()
