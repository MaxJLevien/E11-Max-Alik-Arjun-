import time
import csv 
import serial

reset_pin = None

# For use with Raspberry Pi/Linux:

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

print("Found PM2.5 sensor, reading data...")
meta_data = ["Time","PM1.0","PM2.5","PM10"]
file = open("aq_data.csv", "w", newline='')
writer = csv.writer(file)
writer.writerow(meta_data)
start_time = time.time()
while (time.time() - start_time) < 20:


    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

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
    print("---------------------------------------")
    data_out = [time.time(), aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"]]
    writer.writerow(data_out)
    time.sleep(2)
    


