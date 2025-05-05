import requests

# Local address to container A (in the same Docker network)
TARGET_URL = "http://sensor_server:5000/led"

def send_command(cmd):
    response = requests.post(TARGET_URL, json={"command": cmd})
    print(response.status_code, response.json())

# Example usage: turn on the LED
send_command("on")

# Turn off the LED
# send_command("off")

# Set to automatic mode
# send_command("auto")
