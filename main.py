import RPi.GPIO as GPIO
import dht11
import time
import datetime
import pyowm
import csv
import numpy as np

# initialize GPIO for input/output
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
c1 = -42.379 
c2 = 2.04901523 
c3 = 10.14333127
c4 = -0.22475541
c5 = -6.83783*pow(10,-3)
c6 = -5.481717*pow(10,-2)
c7 = 1.22874*pow(10,-3)
c8 = 8.5282*pow(10,-4)
c9 = -1.99*pow(10,-6)
 
# read data using pin 4
instance = dht11.DHT11(pin=14)
now = datetime.datetime.now()
   
#API Key to use Weather API to collect current data
owm = pyowm.OWM('a84022c6391609d95b57dabe30d9d809')  

rownum = 0

w, h = 31 , 24
matrix = [[0 for x in range(w)] for y in range(h)] 

frequency = [0 for y in range(h)]

for row in reader:
    
    	
    if rownum == 0:
        header = row
        summ = 0
        day = 0
        hour = 0
    else:
        colnum = 0
        for col in row:
            if colnum % 4 == 3:
		    summ += int( col)

	    colnum += 1
    	   
    if rownum % 60 == 1:        
    	#print '%s %-8s: %f %d' % (row[0],header[1],summ /60.0 ,rownum)
    	#print hour,day
    	matrix[hour][day] = summ / 60.0
    	
    	summ = 0  
    	hour += 1
    	if hour % 24 == 0:
    	   hour = 0
    	   day += 1

    rownum += 1  	
    
ifile.close()

for x in range(w):
    for y in range(h):
        if matrix[y][x] > 15:
            frequency[y] += 1
                    

print frequency

for i in frequency:
    if frequency[i] > 18:
        print frequency[i], i
        
while True:
	sensor = instance.read()
	if sensor.is_valid():
		print("Last valid input: " + str(datetime.datetime.now()))
		print("Temperature: %d C" % sensor.temperature)
		print("Humidity: %d %%" % sensor.humidity)
  
      indoorF = sensor.temperature*(9/5.0) + 32
      heatindex_room_F = c1 + c2*indoorF + c3*sensor.humidity + c4*indoorF*sensor.humidity + c5*pow(indoorF,2) + c6*pow(sensor.humidity,2) + c7*pow(indoorF,2)*sensor.humidity + c8*indoorF*pow(sensor.humidity,2) + c9*pow(sensor.humidity,2)*pow(indoorF,2)
	heatindex_room_C = (heatindex_room_F-32)*(5/9.0)
 
      # Search for current weather in Ahmedabad, India
	observation = owm.weather_at_place('Ahmadabad, IN')
	w = observation.get_weather()
	print(w)                      
      temp = w.get_temperature('celsius')
      api_temp = temp["temp_max"]
      api_humidity = w.get_humidity()
      
      
      difference = sensor.temperature - api_temp;
      if (sensor.temperature > 16 and sensor.temperature < 18) and (api_temp < 25 and api_temp > 20) and :
		print "No need of thermostat its pleasant outside"
	else if sensor.temperature > 10 and sensor.temperature < 18 and api_temp > 30:
		print "No need of thermostat its pleasant outside"
			
	print temp["temp_max"]
	
	time.sleep(60)
