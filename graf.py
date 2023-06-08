import threading
import time
import matplotlib.pyplot as plt


class GraphThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.data = []
        self.running = True

    def run(self):
        while self.running:
            # Henter data fra databasen
            data = self.fetch_data_from_database()

            # Opretter graf
            plt.plot(data)

            # Opdatere graf
            plt.pause(0.001)

            time.sleep(0.5)

        plt.show()

    def fetch_data_from_database():
        with open("h_data.txt", "r") as file:
            data = file.read()

        data = data.strip().split("\n")

        return data

    def stop(self):
        self.running = False