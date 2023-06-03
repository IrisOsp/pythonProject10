import random
class vitals: # Super klasse som indeholder de attributter som er tilfældes for subklasserne.
    def __init__(x, start, min, max, Delta):  # the constructor
        x.start = start
        x.min = min
        x.max = max
        x.delta = Delta

    def getVitals(x): # de funktioner som superklassen har.
        x.start = x.start + random.random() * 2 * x.delta - x.delta
        if x.start>= x.max: #Betingelse så den ikke kommer over 100
            x.start=x.start-x.delta
        if x.start<= x.min:
            x.start=x.start+x.delta
        return x.start

    def setVitals(x,b):
        x.start=b

class HB(vitals):
    def __init__(x,start, min, max, Delta):
        super().__init__(start, min, max, Delta)

class Sp02(vitals):
    def __init__(x, start, min, max, Delta):
        super().__init__(start, min, max, Delta)


puls=vitals(70,40,200,0.5)
