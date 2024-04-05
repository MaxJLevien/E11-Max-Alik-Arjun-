import time
import RPi.GPIO as GPIO
import sys
import csv
import serial
import adafruit_bme680
import board
import numpy as np
from adafruit_pm25.uart import PM25_UART

i2c = board.I2C()   # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

reset_pin = None
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

startTime = time.time()
runTime = int(sys.argv[1])
now = time.time()

pm25 = PM25_UART(uart, reset_pin)

count = 0
runningCounts = 0
index = 1
print("running")

filename = sys.argv[2]
file = open(filename, "w", newline='')
writer = csv.writer(file)

meta_data = ["Entry", "Time (Epoch)","PM1.0","PM2.5","PM10","Temperature","Gas","Relative Humidity","Pressure","Altitude","Counts","Total Counts", "Count Rate (1/s)", "Running Count Rate (1/s)"]
writer.writerow(meta_data)

def my_callback(channel):
    global count
    global runningCounts

    count = count + 1
    runningCounts = runningCounts + 1

    print("Pulse Detected at " + str(time.time()))
   
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback)

while (time.time()-startTime) <= runTime:

    time.sleep(10)

    now = time.time()

    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    countRate = count/60
    runningCountRate = runningCounts/(time.time()-startTime)
    
    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print(f"\nTemperature: {bme680.temperature:.3f} C, Gas: {bme680.gas:.3f} Ohm, Humidity: {bme680.relative_humidity:.3f} %, Pressure: {bme680.pressure:.3f} hPa, Altitude = {bme680.altitude:.3f}, Time: {time.time()}")
    print("---------------------------------------")

    print("Current Amount of Pulses Detected: " + str(count))
    print("Count Rate: " + str(countRate) + " Counts/s")
    print("Total Amount of Pulses Detected: " + str(runningCounts))
    print("Running Count Rate: " + str(runningCountRate) + " Counts/s")

    data_out = [time.time(),index, aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"], bme680.temperature, bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude, count, runningCounts, countRate, runningCountRate]
    writer.writerow(data_out)
    count = 0
    index += 1


file.close()