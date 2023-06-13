import tkinter
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
            c.execute("INSERT INTO målinger(EKG) VALUES(?)", (ekg,))
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


q_database = que()
q_graf = que()

# Oppretter en tråd for å hente data fra sensoren og legge dem til i bufferet og q1
sensor_thread1 = Thread(target=sensor_thread_func, args=(b, q_database, Database()))
sensor_thread1.start()

# Henter data fra q_database
print(q_database.getData())

#Laves til graf senere
#sensor_thread2 = Thread(target=sensor_thread_func, args=(b, q_graf, Graf()))
#sensor_thread2.start()

# Henter data fra q_graf
#print(q_graf.getData())

class Graf(tk.Frame):
    def __init__(self, h, w, q_graf):
        super().__init__()

        self.master.title("EKG")
        self.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self, width=w, height=h, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)




ujjj