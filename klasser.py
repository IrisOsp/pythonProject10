from threading import Thread, Condition
from time import sleep

class Buffer():
    def __init__(self):
        self.list = []
        self.size = 0
        self.max = 600

    def addData(self, data):
        self.list.append(data)
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
print(b.list)


class que():
    def __init__(self):
        self._empty, self._value = True, 0
        self._lock=Condition


    def getData(self):
        with self.lock:
            while self._empty:
                self._lock.wait()
            self._empty = True;
            self._lock.notify()
            return self._value


    def putData(self, value):
        with self._lock:
            self._value, self._empty = value, False
            self._lock.notify()


q1=que()
q2=que()

