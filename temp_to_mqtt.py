import paho.mqtt.client as mqtt #import the client1
import board
import busio
import adafruit_mcp9808
import adafruit_bmp280
import time
import sys
from ds18b20 import DS18B20


broker_address="192.168.1.201"
MQTT_USER = 'mqttuser'
MQTT_PASSWORD = 'mqttpassword'


i2c = busio.I2C(board.SCL, board.SDA)
#mcp = adafruit_mcp9808.MCP9808(i2c)
try:
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
except Exception as e:
    sys.stderr.write("Can't read sensor. Error={}".format(e))
    sys.exit(1)

bmp280.mode = adafruit_bmp280.MODE_NORMAL

try:
    ext_sensor = DS18B20()
except:
    ext_sensor_en = False
else:
    ext_sensor_en = True

#broker_address="iot.eclipse.org" #use external broker
client = mqtt.Client("P1") #create new instance
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(broker_address) #connect to broker
client.loop_start()

while True:
    #temp = mcp.temperature
    try:
        temp = bmp280.temperature
        pressure = bmp280.pressure
        #print("Temp#1={} Pressure={}".format(temp, pressure))
        print(".", end='')
        client.publish("home/house/temperature", temp)
        client.publish("home/house/pressure", pressure)
        if ext_sensor_en:
            ext_temp = ext_sensor.get_temperature()
            client.publish("home/house/outsidetemperature", ext_temp)

    except:
        pass
    time.sleep(1)
