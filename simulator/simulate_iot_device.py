import paho.mqtt.client as mqtt
import time
import json # You'll need this if you decide to publish JSON later
import os
import random

# MQTT Broker settings
MQTT_BROKER = os.getenv('MQTT_BROKER', 'mosquitto') # Use 'mosquitto' for Docker
MQTT_PORT = 1883
TOPIC_TEMP = 'iot/sensor/temperature' # Your existing topic
TOPIC_HUM = 'iot/sensor/humidity' # Your existing topic

# Fix DeprecationWarning by specifying API version
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Simulator: Connected to MQTT Broker!")
    else:
        print(f"Simulator: Failed to connect, return code {rc}")

client.on_connect = on_connect

# Add a retry mechanism for connection
max_retries = 10
retry_delay = 5 # seconds

for i in range(max_retries):
    try:
        print(f"Simulator: Attempting to connect to MQTT broker at {MQTT_BROKER}:{MQTT_PORT} (Attempt {i+1}/{max_retries})...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60) # Keep-alive of 60 seconds
        break # Connection successful, break the loop
    except Exception as e:
        print(f"Simulator: MQTT Connection failed: {e}. Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)
else:
    print("Simulator: Failed to connect to MQTT broker after multiple retries. Exiting.")
    exit(1) # Exit if connection consistently fails

client.loop_start() # Start the loop in a non-blocking way for publishes

print("Simulator: Started sending data...")
while True:
    temp = round(random.uniform(20.0, 30.0), 1)  # Celsius
    hum = round(random.uniform(40.0, 80.0), 1)   # Percent

    # Publish directly as float, no need for JSON for now based on your backend
    try:
        client.publish(TOPIC_TEMP, temp)
        client.publish(TOPIC_HUM, hum)
        print(f"Simulator: Published: {temp}°C (Topic: {TOPIC_TEMP}), {hum}% (Topic: {TOPIC_HUM})")
    except Exception as e:
        print(f"Simulator: Error publishing message: {e}. (This often means connection lost, loop_start should handle reconnect).")
        # The loop_start() handles reconnects, just continue attempting to publish

    time.sleep(3) # Publish every 3 seconds