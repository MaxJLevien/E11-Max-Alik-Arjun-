import adafruit_bme680
import time
import board
import csv
import numpy as np

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()   # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

weather_data = np.zeros([10,6])
start_time= time.time()
i = 0

while(time.time()-start_time) < 20:
    
    weather_data[i,0] = bme680.temperature
    weather_data[i,1] = bme680.gas
    weather_data[i,2] = bme680.relative_humidity
    weather_data[i,3] = bme680.pressure
    weather_data[i,4] = bme680.altitude
    weather_data[i,5] = time.time()
    
    i+=1
    
    print(f"\nTemperature: {bme680.temperature:.3f} C, Gas: {bme680.gas:.3f} Ohm, Humidity: {bme680.relative_humidity:.3f} %, Pressure: {bme680.pressure:.3f} hPa, Altitude = {bme680.altitude:.3f}, Time: {time.time()}")
    
    time.sleep(2)

np.savetxt('weather_data.csv',weather_data, delimiter=',', fmt='%.3f', header='Temperature(C),Gas(Ohm),Humidity(%),Pressure(hPa),Altitude(m),Time(Epoch)')
