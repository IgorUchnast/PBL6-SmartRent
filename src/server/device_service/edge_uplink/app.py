import os
import json
import requests
from azure.eventhub import EventHubConsumerClient  # type: ignore

EVENT_HUB_CONN_STR = os.getenv("EVENT_HUB_CONN_STR")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")
TARGET_BASE_URL = os.getenv("TARGET_BASE_URL")

if not EVENT_HUB_CONN_STR or not EVENT_HUB_NAME:
    raise ValueError("Missing EVENT_HUB_CONN_STR or EVENT_HUB_NAME in environment variables")

def send_to_endpoint(sensor_name, value):
    url = f"{TARGET_BASE_URL}/{sensor_name}/data"
    payload = {"value": value}
    try:
        response = requests.post(url, json=payload)
        print(f"[{sensor_name}] → {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error while sending to {url}: {e}")

def update_device_status(device_type, device_id, status):
    if device_type == "lightbulb":
        url = f"{TARGET_BASE_URL}/lightbulbs/{device_id}/status"
        payload = {"lightbulb_status": status}
    elif device_type == "outlet":
        url = f"{TARGET_BASE_URL}/outlets/{device_id}/status"
        payload = {"outlet_status": status}
    else:
        print(f"Unknown device type: {device_type}")
        return
    try:
        response = requests.post(url, json=payload)
        print(f"[{device_type} {device_id}] Status update: {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error while updating {device_type} status for {device_id}: {e}")
    
# Callback function to handle incoming events
def on_event(partition_context, event):
    try:
        device_id = partition_context.partition_id
        body = event.body_as_str(encoding="UTF-8")
        print(f"[{device_id}] → {body}")

        data = json.loads(body)
        for key, value in data.items():
            if isinstance(value, (int, float, str)):
                if key.startswith("lightbulb_"):
                    update_device_status("lightbulb", 1, value)
                elif key.startswith("outlet_"):
                    update_device_status("outlet", 1, value)
                else:
                    # Send sensor data to the target endpoint
                    send_to_endpoint(key, value)
            else:
                print(f"Unsupported data type for {key}: {type(value)}")

        # Update checkpoint to mark the event as processed
        partition_context.update_checkpoint(event)

    except Exception as e:
        print(f"Error processing event: {e}")

if __name__ == "__main__":
    client = EventHubConsumerClient.from_connection_string(
        conn_str=EVENT_HUB_CONN_STR,
        consumer_group="$Default",
        eventhub_name=EVENT_HUB_NAME
    )

    print("Listening for IoT Hub events...")
    with client:
        client.receive(
            on_event=on_event,
            starting_position="@latest",  # only receive new events
            consumer_group="$Default",
        )
