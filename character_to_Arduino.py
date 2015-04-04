import serial
from time import sleep
import struct

s = serial.Serial('/dev/ttyACM0', 9600, timeout = 50)
sleep(2)
l = "Hello World!\nTesting newline!&"
l += struct.pack('!B', 0)
l += struct.pack('!B', 5)
l += struct.pack('!B', 3)
#s.write("Hello world!\n testing newline-")
s.write(l)
for i in xrange(100):
    test = s.readline()
    print test
