import time
import RPi.GPIO as GPIO

count = 0

startTime = time.time()
def my_callback(channel):
    global count
    count = count + 1
    print("Pulse Detected at" + str(time.time()))

while True:
    time.sleep(60)
    print("Current Amount of Pulses Detected: " + str(count))
    count = 0

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.IN)
    GPIO.add_event_detect(6, GPIO.FALLING, callback=my_callback)
 
 
finally:
    GPIO.cleanup()
 
print("Goodbye!")