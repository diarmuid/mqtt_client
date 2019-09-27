import board
import busio
import adafruit_mcp9808
i2c = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808.MCP9808(i2c)
print('Temperature: {} degrees C'.format(mcp.temperature))