from uberpy import Uber
import os
import json
import serial
from time import sleep
from SpeechRecog import SpeechRecog

# Setup keys
client_id=os.environ.get('UBER_KEY')
client_secret=os.environ.get('UBER_SECRET')
server_token=os.environ.get('UBER_SERVER_KEY')

s = serial.Serial('/dev/ttyACM0',9600, timeout = None)

def get_car_type():
    car = int(s.readline().strip('\r\n'))
    car_types = {0:'uberX',1:'uberXL',2:'UberBLACK'}
    return car_types[car]

def get_loc():
    sr = SpeechRecog()
    return sr.speechToCoord()


# Trip location data
start_latitude, start_longitude = (42.347097, -71.097011)
# end_latitude, end_longitude = (42.291641, -71.264653)

uber = Uber(client_id, server_token, client_secret)

time_data = json.dumps(uber.get_time_estimate(start_latitude, start_longitude))
time_estimate = json.loads(time_data)['times']

def get_time_estimate(car_type):
    product_id = None
    for car in time_estimate:
        if car['display_name'] == car_type:
            product_id = car['product_id']
            waiting_estimate = car['estimate']
            break
    return (product_id, waiting_estimate)

product_id, waiting_estimate = get_time_estimate(get_car_type())

end_latitude, end_longitude,output = get_loc()
print output

price_data = json.dumps(uber.get_price_estimate(start_latitude, start_longitude, end_latitude, end_longitude))
ride_data = json.loads(price_data)

all_rides = ride_data['prices']

for ride in all_rides:
    if ride['product_id'] == product_id:
        display_name = ride['display_name']
        price_estimate = ride['high_estimate']
#s.write("Olin College\nNeedham&")
s.write(str(output))
sleep(1)
s.write(str(price_estimate).zfill(2))
sleep(1)
s.write(str(int(waiting_estimate/60)).zfill(2))
'''

print ("Olin College\nNeedham&")
print (str(price_estimate).zfill(2))
print (str(int(waiting_estimate/60)).zfill(2))
'''
#print product_id
#print display_name
#print price_estimate
#print waiting_estimate
