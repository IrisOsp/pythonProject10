from threading import Thread, Condition
from time import sleep


class buffer():
    list = []
    size = 0 #evt. undvære dette og skriv ind i Main (if len(list bla bla.....))
    max = 600

b = buffer()
b.list.append(1)
print(b.list)

class sensor():
    def getData(self):
        file = open("H_data.txt", "r")
        linje = file.readlines()
        for i in range(len(linje)):
            linje[i] = float(linje[i][:-2])
        print(linje)

s=sensor()
print(s.getData())

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

