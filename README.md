# IoT Sensor Dashboard

A full-stack real-time dashboard for monitoring IoT sensor data (temperature and humidity) using React, Tailwind CSS, ChartJS, Flask, Flask-SocketIO, MQTT, and Docker Compose.

---

## Features
- Real-time temperature and humidity monitoring
- Historical data graphs (ChartJS)
- WebSocket-powered live updates
- MQTT integration (Mosquitto broker)
- IoT device simulation script
- Fully containerized (Docker Compose)

---

## Project Structure

```
Weather_Dashboard/
├── backend/                # Flask backend (API, WebSocket, MQTT)
├── frontend/               # React frontend (UI, Tailwind, ChartJS)
├── simulate_iot_device.py  # IoT device simulator (publishes MQTT data)
├── docker-compose.yml      # Orchestration for all services
├── README.md               # This file
```

---

## Quick Start (Docker Compose)

### 1. Clone the repository

```
git clone <repo-url>
cd Weather_Dashboard
```

### 2. Build and start all services

```
docker-compose up --build
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:5000](http://localhost:5000)
- Mosquitto MQTT broker: `localhost:1883`

The simulator will automatically start and publish random sensor data.

### 3. Stopping services

```
docker-compose down
```

---

## Details

### Frontend
- React + Tailwind CSS v3 + ChartJS
- Real-time updates via WebSocket (Socket.IO)
- UI matches the provided design

### Backend
- Python Flask + Flask-SocketIO + Paho-MQTT
- REST API endpoints:
  - `/api/current` (latest readings)
  - `/api/history` (historical data)
- Subscribes to MQTT topics and pushes updates to frontend

### IoT Device Simulator
- Publishes random temperature (20-30°C) and humidity (40-80%) every 3 seconds to MQTT topics:
  - `iot/sensor/temperature`
  - `iot/sensor/humidity`
- Runs as a service in Docker Compose

---

## Customization
- To connect to a different MQTT broker, change the `MQTT_BROKER` environment variable in `docker-compose.yml`.
- To run the simulator manually:
  ```
  python simulate_iot_device.py
  ```

---

## Troubleshooting
- If the dashboard shows "WebSocket Status: Disconnected", ensure the backend and MQTT broker are running and accessible.
- For development, you can run frontend and backend separately (see respective directories for details).

---

## License
MIT 