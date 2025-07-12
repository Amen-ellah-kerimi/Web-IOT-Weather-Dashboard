# app.py - Backend for IoT Weather Dashboard

# --- CRITICAL: eventlet monkey-patching MUST BE THE ABSOLUTE FIRST THING ---
import eventlet
eventlet.monkey_patch()
# --- END CRITICAL SECTION ---


# Now, import other necessary modules
import os
import time
import random
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt


# --- Flask Application Setup ---
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')


# --- In-Memory Data Storage ---
MAX_HISTORY = 30 # Maximum number of data points to keep in history for each sensor.
# *** START OF CHANGES FOR INITIAL DATA ***
# Initialize history with dummy data for immediate display
history = {
    'temperature': [{'timestamp': int(time.time() * 1000) - i*2000, 'value': round(random.uniform(20.0, 30.0), 1)} for i in range(MAX_HISTORY, 0, -1)],
    'humidity': [{'timestamp': int(time.time() * 1000) - i*2000, 'value': round(random.uniform(40.0, 80.0), 1)} for i in range(MAX_HISTORY, 0, -1)]
}
# Initialize current with the last values from the dummy history
current = {
    'temperature': history['temperature'][-1]['value'] if history['temperature'] else None,
    'humidity': history['humidity'][-1]['value'] if history['humidity'] else None,
    'last_update': int(time.time() * 1000)
}
# *** END OF CHANGES FOR INITIAL DATA ***


# --- MQTT Client Configuration ---
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print(f"MQTT: Connected to broker successfully! Result code: {rc}")
        client.subscribe("iot/sensor/temperature")
        client.subscribe("iot/sensor/humidity")
    else:
        print(f"MQTT: Failed to connect to broker, return code: {rc}. Please check broker status and network.")

def on_message(client, userdata, msg):
    topic = msg.topic
    try:
        value = float(msg.payload.decode())
    except ValueError:
        print(f"MQTT: Error decoding payload for topic '{topic}'. Expected float, got: '{msg.payload.decode()}'")
        return

    timestamp = int(time.time() * 1000)

    if topic.endswith('temperature'):
        current['temperature'] = value
        history['temperature'].append({'timestamp': timestamp, 'value': value})
        if len(history['temperature']) > MAX_HISTORY:
            history['temperature'].pop(0)
    elif topic.endswith('humidity'):
        current['humidity'] = value
        history['humidity'].append({'timestamp': timestamp, 'value': value})
        if len(history['humidity']) > MAX_HISTORY:
            history['humidity'].pop(0)

    current['last_update'] = timestamp

    # Your added print for debugging backend emission
    print(f"Flask-SocketIO: Emitting 'sensor_update' with data: {current}, history: Temp={history.get('temperature')[-1:]}, Hum={history.get('humidity')[-1:]}")

    socketio.emit('sensor_update', {
        'temperature': current['temperature'],
        'humidity': current['humidity'],
        'last_update': current['last_update'],
        'history': history # Send the entire history for charting
    })

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_broker = os.environ.get('MQTT_BROKER', '127.0.0.1') # Use 127.0.0.1 as we found it works
mqtt_port = 1883
mqtt_keepalive = 60

try:
    print(f"MQTT: Attempting to connect to broker at {mqtt_broker}:{mqtt_port}...")
    mqtt_client.connect(mqtt_broker, mqtt_port, mqtt_keepalive)
except Exception as e:
    print(f"MQTT: Error connecting to broker: {e}. Ensure Mosquitto is running and accessible.")

mqtt_client.loop_start()


# --- Flask REST API Endpoints ---
@app.route('/api/current')
def get_current_readings():
    print("API: '/api/current' accessed.")
    return jsonify(current)

@app.route('/api/history')
def get_sensor_history():
    print("API: '/api/history' accessed.")
    return jsonify(history)


# --- Flask-SocketIO WebSocket Event Handlers ---
@socketio.on('connect')
def handle_connect_event():
    print("WebSocket: A client connected! Sending initial data.")
    # When a client connects, send the current (now initialized) data and history
    emit('sensor_update', {
        'temperature': current['temperature'],
        'humidity': current['humidity'],
        'last_update': current['last_update'],
        'history': history
    })

@socketio.on('disconnect')
def handle_disconnect_event():
    print("WebSocket: A client disconnected.")

@socketio.on('message')
def handle_message_event(msg):
    print(f"WebSocket: Received message from client: {msg}")


# --- Main Execution Block ---
if __name__ == '__main__':
    print("Starting Flask-SocketIO server...")
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
    print("Flask-SocketIO server has stopped.")