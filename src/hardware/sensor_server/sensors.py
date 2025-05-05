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

# Threshold for light resistance (kΩ)
THRESHOLD = 10

POST_URL = os.getenv("POST_URL", False)
POST_INTERVAL = int(os.getenv("POST_INTERVAL", 5))  # Default 5s

# Global override flag for LED control
external_led_override = None  # None = automatic, True = forced on, False = forced off

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
            light_value = grovepi.analogRead(LIGHT_SENSOR)
            dark, resistance = is_dark(light_value)
            [temp, humidity] = grovepi.dht(TEMP_HUM_SENSOR, 0)  # 0 for blue sensor
            motion = grovepi.digitalRead(PIR_SENSOR)

            if not math.isnan(temp) and not math.isnan(humidity):
                print(f"temp = {temp:.2f} C humidity = {humidity:.2f}%")

            # LED logic
            if external_led_override is True:
                grovepi.digitalWrite(LED_PIN, 1)
            elif external_led_override is False:
                grovepi.digitalWrite(LED_PIN, 0)
            else:
                # Automatic control based on light and motion
                grovepi.digitalWrite(LED_PIN, 1 if dark and motion else 0)

            print(f"light_value = {light_value} resistance = {resistance:.2f}")
            print("movement detected" if motion else "no movement detected")

            # If POST_URL is set, send data to the server
            if POST_URL:
                # Check if it's time to post data
                current_time = time.time()
                if current_time - last_post_time >= POST_INTERVAL:
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
