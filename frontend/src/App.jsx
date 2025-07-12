import React, { useEffect, useState, useRef } from "react";
import { Line } from "react-chartjs-2";
import { Chart, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend } from "chart.js";
import io from "socket.io-client";

Chart.register(LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend);

const WS_URL = import.meta.env.VITE_WS_URL || "http://localhost:5000";

function formatTime(ts) {
  if (!ts) return "--:--:--";
  const d = new Date(ts);
  return d.toLocaleTimeString();
}

function App() {
  const [current, setCurrent] = useState({ temperature: null, humidity: null, last_update: null });
  const [history, setHistory] = useState({ temperature: [], humidity: [] });
  const [wsStatus, setWsStatus] = useState("disconnected");
  const socketRef = useRef(null);

  useEffect(() => {
    const socket = io(WS_URL);
    socketRef.current = socket;
    setWsStatus("connecting");

    socket.on("connect", () => {
      console.log("WebSocket: Connected!");
      setWsStatus("connected");
    });
    socket.on("disconnect", () => {
      console.log("WebSocket: Disconnected!");
      setWsStatus("disconnected");
    });
    socket.on("connect_error", (error) => {
      console.error("WebSocket: Connection Error!", error);
      setWsStatus("error");
    });

    socket.on("sensor_update", (data) => {
      // THIS IS THE CRITICAL LOG TO CHECK!
      console.log("WebSocket: Received sensor_update data:", data);

      if (data) {
        setCurrent({
          temperature: data.temperature,
          humidity: data.humidity,
          last_update: data.last_update,
        });
        // Ensure history is also an object with temperature and humidity arrays
        setHistory({
          temperature: data.history.temperature || [],
          humidity: data.history.humidity || []
        });
      }
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  // Chart data (will be empty if history arrays are empty)
  const tempData = {
    labels: history.temperature.map((d) => formatTime(d.timestamp)),
    datasets: [
      {
        label: "Temperature (°C)",
        data: history.temperature.map((d) => d.value),
        borderColor: "#3b82f6",
        backgroundColor: "#3b82f6",
        tension: 0.3,
        fill: false,
        pointRadius: 3,
      },
    ],
  };
  const humData = {
    labels: history.humidity.map((d) => formatTime(d.timestamp)),
    datasets: [
      {
        label: "Humidity (%)",
        data: history.humidity.map((d) => d.value),
        borderColor: "#22d3ee",
        backgroundColor: "#22d3ee",
        tension: 0.3,
        fill: false,
        pointRadius: 3,
      },
    ],
  };
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        labels: { color: "#a3e3fa" },
      },
    },
    scales: {
      x: {
        ticks: { color: "#a3e3fa" },
        grid: { color: "#334155" },
      },
      y: {
        ticks: { color: "#a3e3fa" },
        grid: { color: "#334155" },
      },
    },
  };

  // WebSocket status indicator logic remains the same
  let wsColor = "bg-red-600";
  let wsText = "Disconnected";
  let wsDesc = "Connection error";
  if (wsStatus === "connected") {
    wsColor = "bg-green-500";
    wsText = "Connected";
    wsDesc = "";
  } else if (wsStatus === "connecting") {
    wsColor = "bg-yellow-400";
    wsText = "Connecting";
    wsDesc = "Attempting to connect...";
  } else if (wsStatus === "error") {
    wsColor = "bg-red-600";
    wsText = "Disconnected";
    wsDesc = "Connection error";
  }

  return (
    <div className="min-h-screen bg-[#192132] flex flex-col">
      {/* Header */}
      <header className="bg-[#176ca7] px-8 py-4 flex items-center justify-between rounded-t-lg">
        <div className="flex items-center gap-3">
        <img src="/iot-icon.svg" alt="IoT Dashboard Icon" className="w-8 h-8 text-white" />
          <div>
            <div className="text-white text-2xl font-bold">IoT Sensor Dashboard</div>
            <div className="text-blue-100 text-xs">Real-time monitoring of IoT sensor data</div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-6">
        {/* Current Readings */}
        <div className="w-full max-w-5xl flex gap-4 mb-6">
          <div className="flex-1 bg-[#232b3e] rounded-lg p-6 flex flex-col justify-center">
            <div className="text-blue-200 text-lg mb-2">Temperature</div>
            <div className="text-4xl font-bold text-blue-100">{current.temperature !== null ? `${current.temperature}°C` : "--"}</div>
          </div>
          <div className="flex-1 bg-[#1e2e24] rounded-lg p-6 flex flex-col justify-center">
            <div className="text-green-200 text-lg mb-2">Humidity</div>
            <div className="text-4xl font-bold text-green-100">{current.humidity !== null ? `${current.humidity}%` : "--"}</div>
          </div>
          <div className="flex-1 bg-[#353c47] rounded-lg p-6 flex flex-col justify-center">
            <div className="text-gray-300 text-lg mb-2">Last Update</div>
            <div className="text-2xl font-bold text-gray-200">{formatTime(current.last_update)}</div>
          </div>
        </div>
        {/* Graphs */}
        <div className="w-full max-w-5xl flex gap-4">
          <div className="flex-1 bg-[#232b3e] rounded-lg p-6">
            <div className="text-blue-200 text-lg mb-2">Temperature History</div>
            <Line data={tempData} options={chartOptions} height={180} />
          </div>
          <div className="flex-1 bg-[#1e2e24] rounded-lg p-6">
            <div className="text-green-200 text-lg mb-2">Humidity History</div>
            <Line data={humData} options={chartOptions} height={180} />
          </div>
        </div>
      </main>

      {/* WebSocket Status */}
      <div className="fixed left-6 bottom-8 z-50">
        <div className="bg-[#232b3e] rounded-lg shadow-lg px-6 py-3 flex items-center gap-3 border border-[#2e3a4e]">
          <span className={`w-3 h-3 rounded-full ${wsColor} inline-block`}></span>
          <span className="text-gray-200 font-semibold">WebSocket Status: <span className={wsColor === "bg-green-500" ? "text-green-400" : "text-red-400"}>{wsText}</span></span>
        </div>
        {wsDesc && <div className="text-red-400 text-xs ml-8 mt-1">{wsDesc}</div>}
      </div>

      {/* Footer */}
      <footer className="bg-[#232b3e] text-center text-gray-300 py-3 text-lg mt-8 rounded-b-lg">
        IoT Sensor Dashboard - 2025
      </footer>
    </div>
  );
}

export default App;