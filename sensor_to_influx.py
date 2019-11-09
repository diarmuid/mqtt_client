import board
import busio
import adafruit_mcp9808
import adafruit_bmp280
import time
import sys
from ds18b20 import DS18B20
from influxdb import InfluxDBClient
from typing import NamedTuple

# Influx database details
INFLUXDB_ADDRESS = 'ec2-34-245-159-219.eu-west-1.compute.amazonaws.com'
INFLUXDB_USER = 'root'
INFLUXDB_PASSWORD = 'root'
INFLUXDB_DATABASE = 'home_db'
bmp280_calibration_offset = -1.7


class SensorData(NamedTuple):
    location: str
    measurement: str
    value: float


def _init_influxdb_database(influxdb_client):
    """
    Connect to an influx database
    :param influxdb_client:
    :return:
    """
    databases = influxdb_client.get_list_database()
    print("Connected to influx database")
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)


def send_sensor_data_to_influxdb(sensor_data, influxdb_client):
    """
    Send the data to the client
    :param sensor_data:
    :param influxdb_client:
    :return:
    """
    json_body = [
        {
            'measurement': sensor_data.measurement,
            'tags': {
                'location': sensor_data.location
            },
            'fields': {
                'value': sensor_data.value
            }
        }
    ]
    if not influxdb_client.ping():
        _init_influxdb_database(influxdb_client)

    if not influxdb_client.write_points(json_body):
        _init_influxdb_database(influxdb_client)

    #print("Sending data to influx {}".format(json_body))


# I2c of indoor pressure and temp sensor

i2c = busio.I2C(board.SCL, board.SDA)
try:
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
except Exception as e:
    sys.stderr.write("Can't read sensor. Error={}".format(e))
    sys.exit(1)

bmp280.mode = adafruit_bmp280.MODE_NORMAL
# The outside temperature sensor
try:
    ext_sensor = DS18B20()
except:
    ext_sensor_en = False
else:
    ext_sensor_en = True

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
_init_influxdb_database(influxdb_client)

while True:
    #
    try:
        temp = bmp280.temperature + bmp280_calibration_offset
        pressure = bmp280.pressure
    except:
        pass
    else:
        data = SensorData("house", "temperature", temp)
        send_sensor_data_to_influxdb(data, influxdb_client)

    try:
        pressure = bmp280.pressure
    except:
        pass
    else:
        data = SensorData("house", "pressure", pressure)
        send_sensor_data_to_influxdb(data, influxdb_client)
    if ext_sensor_en:
        try:
            ext_temp = ext_sensor.get_temperature()
        except:
            pass
        else:
            data = SensorData("house", "outsidetemperature", ext_temp)
            send_sensor_data_to_influxdb(data, influxdb_client)

    time.sleep(1)
