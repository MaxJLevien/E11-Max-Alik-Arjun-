import sys
import random
import time
import csv
import numpy as np

print(sys.argv)

startTime = time.time()
runTime = int(sys.argv[1])
now = time.time()

filename = 'data.csv'
filename = sys.argv[2]
file = open(filename,'w',newline='')
writer = csv.writer(file)

metaData = ['Time', 'Data']
print(metaData)
writer.writerow(metaData)

while (now - startTime) < runTime:
    time.sleep(1)

    data = random.random()
    now = time.time()

    dataList = [now,data]
    print(dataList)
    writer.writerow(dataList)