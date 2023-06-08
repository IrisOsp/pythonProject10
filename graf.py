import threading
import time

class Buffer():
    def __init__(self):
        self.buffer_list = []
        self.size = 0
        self.max_size = 600


class Que():
    def __init__(self):
        self.que = []
        self.size = 0
        self.lock = threading.Lock()

    def put(self, obs):
        self.lock.acquire()  # Henter lås før køen ændres
        self.que.append(obs)
        self.size += 1
        self.lock.release()  # Slipper låsen efter ændring af køen

    def get(self):
        self.lock.acquire()   # Henter lås før køen ændres
        if self.size == 0:
            self.lock.release()  # Slipper låsen, hvis køen er tom
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
            self.que.put(line)  # Tilføj data til køen eller bufferen

    def run(self):
        while True:
            self.load_data()
            time.sleep(0.5)  # Sov/vent i 0.5 sekund, før der indlæses de næste data

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
            time.sleep(0.1)  # Sov/vent i 0.1 sekunder, før der behandles det næste i køen

class Graph():
    def __init__(self, buffer):
        self.buffer = buffer

    def plot_graph(self):
        # Plotter grafen fra data fra Bufferen
        pass

buffer = Buffer()
que = Que()
sensor = Sensor(que)
db = DB(que)
graph = Graph(buffer)

sensor.start()
db.start()

# Fortsætter med at køre grafen i hovedtråden
while True:
    graph.plot_graph()
    time.sleep(1)  # Sov/vent 1 sekund, før der plottes den næste måling/observation

