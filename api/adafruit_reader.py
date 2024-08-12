import sys
import Adafruit_DHT
from datetime import datetime

def readCurrentTemAndHumidity():
	sensor = Adafruit_DHT.DHT22
	pin = 9
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		result = 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
		print(result)
		return result
	# now = datetime.now()
	# formatted_time = now.strftime("%m-%d %H:%M")
	# with open('/home/pi/Shared/TemperatureAndHumidity.txt', 'a', encoding='utf-8') as the_file:
	#     resultStr = formatted_time + ": " + result + '\n'
	#     the_file.write(resultStr)
	else:
		print('Failed to get reading. Try again!')
		sys.exit(1)

def readTheLastTemAndHumidity():
	sensor = Adafruit_DHT.DHT22
	pin = 9
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		result = 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
		print(result)
	# now = datetime.now()
	# formatted_time = now.strftime("%m-%d %H:%M")
	# with open('/home/pi/Shared/TemperatureAndHumidity.txt', 'a', encoding='utf-8') as the_file:
	#     resultStr = formatted_time + ": " + result + '\n'
	#     the_file.write(resultStr)
	else:
		print('Failed to get reading. Try again!')
		sys.exit(1)