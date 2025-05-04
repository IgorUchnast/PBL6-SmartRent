import time
import grovepi  # type: ignore
import math

# Ports 
LIGHT_SENSOR = 0    # A0
TEMP_HUM_SENSOR = 2 # D2
LED_PIN = 4         # D4
PIR_SENSOR = 7      # D7

# Turn on LED once sensor exceeds threshold resistance
THRESHOLD = 10

grovepi.pinMode(LIGHT_SENSOR,"INPUT")
grovepi.pinMode(LED_PIN,"OUTPUT")
grovepi.pinMode(PIR_SENSOR,"INPUT")

def is_dark(sensor_value):
    try:
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value  # kΩ
    except ZeroDivisionError:
        resistance = float('inf')  # Resistance is infinite if sensor_value is 0
    return resistance > THRESHOLD, resistance

while True:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(LIGHT_SENSOR)
        dark, resistance = is_dark(sensor_value)

        [temp, humidity] = grovepi.dht(TEMP_HUM_SENSOR, 0)  # 0 for blue sensor
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))

        if dark:
            if grovepi.digitalRead(PIR_SENSOR):
                grovepi.digitalWrite(LED_PIN, 1)
            else:
                grovepi.digitalWrite(LED_PIN, 0)
        else:
            grovepi.digitalWrite(LED_PIN, 0)

        print("sensor_value = %d resistance = %.2f" %(sensor_value,  resistance))
        print("movement detected" if grovepi.digitalRead(PIR_SENSOR) else "no movement detected")
        time.sleep(.5)

    except IOError:
        print ("Error")
