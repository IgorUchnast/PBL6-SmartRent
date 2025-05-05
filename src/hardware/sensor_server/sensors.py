import time
import grovepi  # type: ignore
import math
import requests
import os

# Ports 
LIGHT_SENSOR = 0    # A0
TEMP_HUM_SENSOR = 2 # D2
LED_PIN = 4         # D4
PIR_SENSOR = 7      # D7

# Turn on LED once sensor exceeds threshold resistance
THRESHOLD = 10

POST_URL = os.getenv("POST_URL", False)
POST_INTERVAL = int(os.getenv("POST_INTERVAL", 5))  # Default to 5 seconds if not set

grovepi.pinMode(LIGHT_SENSOR, "INPUT")
grovepi.pinMode(LED_PIN, "OUTPUT")
grovepi.pinMode(PIR_SENSOR, "INPUT")

def is_dark(light_value):
    try:
        resistance = (float)(1023 - light_value) * 10 / light_value  # kΩ
    except ZeroDivisionError:
        resistance = float('inf')  # Resistance is infinite if light_value is 0
    return resistance > THRESHOLD, resistance

def sensor_loop():
    global external_led_override
    last_post_time = 0

    while True:
        try:
            # Get sensor value
            light_value = grovepi.analogRead(LIGHT_SENSOR)
            dark, resistance = is_dark(light_value)
            [temp, humidity] = grovepi.dht(TEMP_HUM_SENSOR, 0)  # 0 for blue sensor
            motion = grovepi.digitalRead(PIR_SENSOR)

            if math.isnan(temp) == False and math.isnan(humidity) == False:
                print("temp = %.02f C humidity =%.02f%%" % (temp, humidity))

            # LED handling
            if dark and motion:
                grovepi.digitalWrite(LED_PIN, 1)
            else:
                grovepi.digitalWrite(LED_PIN, 0)

            # Manual LED control
            if external_led_override is True:
                grovepi.digitalWrite(LED_PIN, 1)
            elif external_led_override is False:
                grovepi.digitalWrite(LED_PIN, 0)
            else:
                # Automatic control based on light and motion
                grovepi.digitalWrite(LED_PIN, 1 if dark and motion else 0)

            print("light_value = %d resistance = %.2f" % (light_value, resistance))
            print("movement detected" if motion else "no movement detected")

            # If POST_URL is set, send data to the server
            if POST_URL:
                # Check if it's time to post data
                current_time = time.time()
                if current_time - last_post_time >= POST_INTERVAL:
                    # Send data to the server
                    data = {
                        "temperature": temp,
                        "humidity": humidity,
                        "light_sensor_value": light_value,
                        "light_sensor_resistance": resistance,
                        "is_dark": dark,
                        "motion_detected": bool(motion)
                    }

                    try:
                        response = requests.post(POST_URL, json=data)
                        print(f"POST status: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        print(f"POST error: {e}")

                    last_post_time = current_time

            time.sleep(0.5)

        except Exception as e:
            print(f"Error: {e}")
