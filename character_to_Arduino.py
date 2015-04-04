import serial
from time import sleep
import struct

s = serial.Serial('/dev/ttyACM0', 9600, timeout = 5)
s.readline()
l = "Hello World!\nTesting newline!&"
#s.write("Hello world!\n testing newline-")
l += " 5 3"
s.write(l)
sleep(10)
l = "& 2"
s.write(l)
sleep(10)
s.write("& 1")
for i in xrange(100):
    test = s.readline()
    print test
