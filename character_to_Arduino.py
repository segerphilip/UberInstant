import serial
from time import sleep

s = serial.Serial('/dev/ttyACM0', 9600, timeout = 50)
sleep(2)
s.write("Hello world!")
test = s.readline()

print test
