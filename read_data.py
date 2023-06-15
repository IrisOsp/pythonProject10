import serial
from sys import stdout

arduino_port = '/dev/cu.usbmodem101'
baud_rate = 38400  # samme baudrate, som er angivet i Arduino-koden

ser = serial.Serial(arduino_port, baud_rate, timeout=1)

file_path = 'TEST_data.txt'  # Angiv stien

file = open(file_path, 'w')


run = True
ser.setDTR(run)

while run:
    try:
        data = ser.readline().decode().strip()  # Læs en linje fra seriel forbindelse og omkod den til en streng
        if data:
            file.write(data + '\n')  # Gemmer data i tekstfilen med en ny linje
            print(data)  # Udskriv dataene
        else:
            print(".", end="")
            stdout.flush()
    except KeyboardInterrupt:
        run = False
        break

ser.setDTR(run)
ser.close()
file.close()
