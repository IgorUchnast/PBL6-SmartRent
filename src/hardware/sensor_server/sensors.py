import time
import grovepi  # type: ignore
import math
import requests
import os
import tinytuya # type: ignore

# Ports
LIGHT_SENSOR = 0    # A0
TEMP_HUM_SENSOR = 2 # D2
LED_PIN = 4         # D4
PIR_SENSOR = 7      # D7

# Threshold for light resistance (kΩ)
THRESHOLD = 10

POST_URL = "http://localhost:5001/forward"  # URL of the post server
POST_INTERVAL = int(os.getenv("POST_INTERVAL", 5))  # Default 5s
DHT_INTERVAL = int(os.getenv("DHT_INTERVAL", 3))  # Default 3s

# Initialize Tuya outlet
DEVICE_ID = os.getenv("DEVICE_ID")
IP_ADDRESS = os.getenv("IP_ADDRESS", "Auto")  # Default to 'Auto' for automatic IP detection
LOCAL_KEY = os.getenv("LOCAL_KEY")
outlet = tinytuya.OutletDevice(
    dev_id=DEVICE_ID,
    address=IP_ADDRESS,
    local_key=LOCAL_KEY, 
    version=3.3)

# Global override flag for LED control
external_led_override = None  # None = automatic, True = forced on, False = forced off
led_mode = "auto"  # Current mode of the LED
led_state = False  # Current state of the LED

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
    last_dht_time = 0
    temp = None
    humidity = None

    while True:
        try:
            current_time = time.time()
            # Read DHT sensor data every DHT_INTERVAL seconds
            # This is a workaround for the DHT sensor, which may return NaN
            if current_time - last_dht_time >= DHT_INTERVAL:
                # Read DHT sensor data
                temp, humidity = grovepi.dht(TEMP_HUM_SENSOR, 0)  # 0 for blue sensor
                last_dht_time = current_time
            light_value = grovepi.analogRead(LIGHT_SENSOR)
            dark, resistance = is_dark(light_value)
            motion = grovepi.digitalRead(PIR_SENSOR)

            outlet_data = outlet.status()
            dps = outlet_data["dps"]
            outlet_status = dps.get("1")    # True, False
            voltage = dps.get("20") / 10    # V
            current = dps.get("18") / 1000  # A
            power = dps.get("19") / 10      # W
            energy = dps.get("17") / 1000   # kWh

            # print("\nPomiary energii:")
            # print(f"Stan gniazdka: {outlet_status}")
            # print(f"Napięcie: {voltage} V")
            # print(f"Prąd: {current} mA")
            # print(f"Moc: {power} W")
            # print(f"Energia: {energy} kWh")

            # if not math.isnan(temp) and not math.isnan(humidity):
            #     print(f"temp = {temp:.2f} C humidity = {humidity:.2f}%")

            # print(f"light_value = {light_value} resistance = {resistance:.2f}")
            # print("movement detected" if motion else "no movement detected")

            # LED logic
            if external_led_override is True:
                grovepi.digitalWrite(LED_PIN, 1)
                led_mode = "on"
                led_state = True
            elif external_led_override is False:
                grovepi.digitalWrite(LED_PIN, 0)
                led_mode = "off"
                led_state = False
            else:
                # Automatic control based on light and motion
                if dark and motion:
                    grovepi.digitalWrite(LED_PIN, 1)
                    led_state = True
                else:
                    grovepi.digitalWrite(LED_PIN, 0)
                    led_state = False
                led_mode = "auto"

            # Check if it's time to post data
            if current_time - last_post_time >= POST_INTERVAL:
                if math.isfinite(temp) and math.isfinite(humidity):
                    data = {
                        "temperature": temp,
                        "humidity": humidity,
                        "lightbulb_status": led_mode,
                        "outlet_status": "on" if outlet_status else "off",
                        "voltage": voltage,
                        "amperage": current,
                        "power": power,
                        "total": energy,
                    }
                    try:
                        response = requests.post(POST_URL, json=data)
                        print(f"POST status: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        print(f"POST error: {e}")
                        print(data)
                else:
                    print("Invalid sensor data (NaN or inf), skipping POST.")

                last_post_time = current_time

            time.sleep(0.5)

        except Exception as e:
            print(f"Error: {e}")
