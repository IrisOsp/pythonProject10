import tkinter as tk
from threading import Thread, Condition
from time import sleep
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
            c.execute("INSERT INTO målinger(EKG) VALUES(?)", (ekg)) #Person_id indsættes i målinger og
            conn.commit()
            c.close()
            conn.close()

        except sqlite3.Error as e:
            print("Kommunikationsfejl 3")



def sensor_thread_func(buffer, queue, db_send):
    s = Sensor()
    data = s.getData()
    buffer.addData(data)
    queue.putData(data)
    # Send hvert element fra listen til databasen
    for item in data:
        db_send.sendToDatabase(item)

def sensor_thread_func2(buffer, queue, graph_send):
    s = Sensor()
    data = s.getData()
    buffer.addData(data)
    queue.putData(data)
    graph_send.draw_graph(data)

q_database = que()
q_graf = que()

# Oppretter en tråd for å hente data fra sensoren og legge dem til i bufferet og q1
sensor_thread1 = Thread(target=sensor_thread_func, args=(b, q_database, Database()))
sensor_thread1.start()

# Henter data fra q_database
print(q_database.getData())

class Graph(tk.Canvas):
    def __init__(self, parent, data, width, height):
        super().__init__(parent, width=width, height=height, bg="white")
        self.data = sensor_thread2
        self.width =2000
        self.height = 500

    def draw_graph(self):
        if not self.data:
            return

        # Find den mindste og største værdi i listen af tal
        min_val = min(self.data)
        max_val = max(self.data)

        # Beregn skalaen for x- og y-aksen
        x_scale = self.width / len(self.data)
        y_scale = self.height / (max_val - min_val)

        # Tegn graflinjen
        prev_x = 0
        prev_y = self.height - (self.data[0] - min_val) * y_scale

        for i in range(1, len(self.data)):
            x = i * x_scale
            y = self.height - (self.data[i] - min_val) * y_scale

            self.create_line(prev_x, prev_y, x, y, fill="blue")
            prev_x = x
            prev_y = y

#Laves til graf senere
sensor_thread2 = Thread(target=sensor_thread_func2, args=(b, q_graf, Graph()))
sensor_thread2.start()

# Henter data fra q_graf
print(q_graf.getData())

data=sensor_thread2

root = tk.Tk()
graph = Graph(root, data)
graph.pack()

graph.draw_graph()

root.mainloop()


