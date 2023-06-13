import threading
import time
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



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

    canvas.update_graph()

    sensor.start()
    db.start()

    root.mainloop()


if _name_ == '_main_':
    main()