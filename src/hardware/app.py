import time
import grovepi # type: ignore

# Ports 
light_sensor = 0    # A0
led = 4             # D4
pir_sensor = 7      # D7

# Turn on LED once sensor exceeds threshold resistance
threshold = 10

grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(led,"OUTPUT")
grovepi.pinMode(pir_sensor,"INPUT")

def is_dark(sensor_value):
    try:
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value  # kΩ
    except ZeroDivisionError:
        resistance = float('inf')  # Resistance is infinite if sensor_value is 0
    return resistance > threshold, resistance

while True:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)
        dark, resistance = is_dark(sensor_value)

        if dark:
            if grovepi.digitalRead(pir_sensor):
                grovepi.digitalWrite(led, 1)
        else:
            grovepi.digitalWrite(led, 0)

        print("sensor_value = %d resistance = %.2f" %(sensor_value,  resistance))
        time.sleep(.5)

    except IOError:
        print ("Error")
