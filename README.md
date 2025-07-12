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
- Responsive design with modern UI

---

## Project Structure

```
Weather_Dashboard/
├── backend/                # Flask backend (API, WebSocket, MQTT)
│   ├── app.py             # Main Flask application
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Backend container configuration
├── frontend/              # React frontend (UI, Tailwind, ChartJS)
│   ├── src/               # React source code
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Frontend container configuration
├── simulator/             # IoT device simulator
│   ├── simulate_iot_device.py  # MQTT data publisher
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Simulator container configuration
├── mosquitto/             # MQTT broker configuration
│   └── config/            # Mosquitto configuration files
├── docker-compose.yml     # Orchestration for all services
└── README.md              # This file
```

---

## Quick Start (Docker Compose)

### 1. Clone the repository

```bash
git clone <repo-url>
cd Weather_Dashboard
```

### 2. Build and start all services

```bash
docker-compose up --build
```

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend API: [http://localhost:5000](http://localhost:5000)
- Mosquitto MQTT broker: `localhost:1883`

The simulator will automatically start and publish random sensor data every 3 seconds.

### 3. Stopping services

```bash
docker-compose down
```

---

## Details

### Frontend
- React + Tailwind CSS v3 + ChartJS
- Real-time updates via WebSocket (Socket.IO)
- Modern responsive UI with dark theme
- Vite for fast development and building

### Backend
- Python Flask + Flask-SocketIO + Paho-MQTT
- REST API endpoints:
  - `/api/current` (latest readings)
  - `/api/history` (historical data)
- Subscribes to MQTT topics and pushes updates to frontend
- CORS enabled for cross-origin requests

### IoT Device Simulator
- Publishes random temperature (20-30°C) and humidity (40-80%) every 3 seconds to MQTT topics:
  - `iot/sensor/temperature`
  - `iot/sensor/humidity`
- Runs as a service in Docker Compose
- Includes retry mechanism for MQTT connection

### MQTT Broker (Mosquitto)
- Configured for anonymous connections
- Listens on port 1883
- Custom configuration in `mosquitto/config/mosquitto.conf`

---

## Local Development

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

### Running with Docker (Recommended)
```bash
docker-compose up --build
```

### Running Locally
1. Start MQTT broker: `docker run -d --name mosquitto-broker -p 1883:1883 eclipse-mosquitto:2.0.22`
2. Start backend: `cd backend && python app.py`
3. Start frontend: `cd frontend && npm run dev`
4. Start simulator: `cd simulator && python simulate_iot_device.py`

---

## Customization
- To connect to a different MQTT broker, change the `MQTT_BROKER` environment variable in `docker-compose.yml`.
- To run the simulator manually:
  ```bash
  cd simulator
  python simulate_iot_device.py
  ```

---

## Troubleshooting
- If the dashboard shows "WebSocket Status: Disconnected", ensure the backend and MQTT broker are running and accessible.
- For development, you can run frontend and backend separately (see respective directories for details).
- Check Docker logs: `docker-compose logs [service-name]`
- Ensure ports 5173, 5000, and 1883 are available

---

## API Endpoints

### Backend REST API
- `GET /api/current` - Get current sensor readings
- `GET /api/history` - Get historical sensor data

### WebSocket Events
- `sensor_update` - Real-time sensor data updates

### MQTT Topics
- `iot/sensor/temperature` - Temperature readings
- `iot/sensor/humidity` - Humidity readings

---

## License
MIT 