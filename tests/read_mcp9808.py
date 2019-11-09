import board
import busio
import adafruit_mcp9808
import adafruit_bmp280
import time
import sys




i2c = busio.I2C(board.SCL, board.SDA)
#mcp = adafruit_mcp9808.MCP9808(i2c)
try:
    bmp280 = adafruit_mcp9808.MCP9808(i2c)
except Exception as e:
    sys.stderr.write("Can't read sensor. Error={}".format(e))
    sys.exit(1)

#bmp280.mode = adafruit_bmp280.MODE_NORMAL


while True:
    try:
        temp = bmp280.temperature
        pressure = 0
        print("Temp#1={} Pressure={}".format(temp, pressure))
    except:
        pass
    time.sleep(1)
