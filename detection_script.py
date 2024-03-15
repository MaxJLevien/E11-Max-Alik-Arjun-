import time
import RPi.GPIO as GPIO

count = 0
print("running")

def my_callback(channel):
    global count
    count = count + 1
    print("Pulse Detected at" + str(time.time()))
   
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback)

while True:
    time.sleep(60)
    countRate = count/60
    print("Current Amount of Pulses Detected: " + str(count))
    print("Count Rate: " + str(countRate))
    count = 0