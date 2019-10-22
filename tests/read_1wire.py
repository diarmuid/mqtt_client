from ds18b20 import DS18B20
import time

print(DS18B20.get_available_sensors())

sensor = DS18B20()
while True:
    temperature_in_celsius = sensor.get_temperature()
    print(temperature_in_celsius)
    time.sleep(2)
