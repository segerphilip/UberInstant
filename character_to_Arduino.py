import serial
from time import sleep
import struct

s = serial.Serial('/dev/ttyACM0', 9600, timeout = None)
test = s.readline()
print test
sleep(2)
l = "Hello World!\nTesting newline!&"
l += " 5"

s.write(l)
raw_input()
l = " 2"
s.write(l)

raw_input()
l = "Fuck this shit\nLol jk&99"
s.write(l)
raw_input()
l = " 3"

raw_input()
s.write(" 1")
raw_input()
s.write("10")
raw_input()
for i in xrange(100):
    test = s.readline()
    print test
