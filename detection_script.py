import time
import RPi.GPIO as GPIO
import sys
import csv

count = 0
runningCounts = 0
index = 1
print("running")

startTime = time.time()
runTime = int(sys.argv[1])

filename = sys.argv[2]
file = open(filename, "w", newline='')
writer = csv.writer(file)

meta_data = ["Entry","Counts","Total Counts", "Count Rate (1/s)","Time (Epoch)"]
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
    time.sleep(60)
    index += 1
    countRate = count/60
    runningCountRate = runningCounts/(time.time()-startTime)
    print("Current Amount of Pulses Detected: " + str(count))
    print("Count Rate: " + str(countRate) + " Counts/s")
    print("Total Amount of Pulses Detected: " + str(runningCounts))
    print("Running Count Rate: " + str(runningCountRate) + " Counts/s")
    count = 0
    data_out = [index, count, runningCounts, countRate, time.time()]
    writer.writerow(data_out)