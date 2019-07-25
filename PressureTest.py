import ms5837
import time

sensor = ms5837.MS5837_30BA()  # Default I2C bus is 1 (Raspberry Pi 3)

# We must initialize the sensor before reading it
if not sensor.init():
    print("Sensor could not be initialized")
    exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    print("Sensor read failed!")
    exit(1)

# Spew readings
while True:
    sensor.read()
    print(sensor.pressure())
    time.sleep(.05)
