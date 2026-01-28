# 🧠 AI-Driven Smart Lab Resource Utilization & Idle-Time Detection

> **Network + CCTV Based Intelligent System for Lab Energy Optimization**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red.svg)](https://opencv.org/)

---

## 📋 Overview

This system monitors lab computers to detect **idle resources** using a combination of:
- **System Activity** (Mouse, Keyboard, CPU Usage)
- **Visual Presence Detection** (CCTV / Webcam)

When a system is confirmed idle (no user activity + no physical presence), the server sends automated commands to **sleep/shutdown** the machine, saving energy.

---

## 🏗️ Architecture

```
┌─────────────────────┐     ┌─────────────────────┐
│   PC Agent          │     │   Camera Module     │
│  (Mouse/Key/CPU)    │     │  (Presence Detect)  │
└─────────┬───────────┘     └─────────┬───────────┘
          │                           │
          │     LAN (HTTP/JSON)       │
          └───────────┬───────────────┘
                      ▼
          ┌───────────────────────┐
          │    Central Server     │
          │  ┌─────────────────┐  │
          │  │ Decision Engine │  │
          │  └─────────────────┘  │
          │  ┌─────────────────┐  │
          │  │    Database     │  │
          │  └─────────────────┘  │
          │  ┌─────────────────┐  │
          │  │   Dashboard     │  │
          │  └─────────────────┘  │
          └───────────┬───────────┘
                      │
          ┌───────────▼───────────┐
          │   Network Commands    │
          │  (SLEEP / SHUTDOWN)   │
          └───────────────────────┘
```

---

## 📁 Project Structure

```
Proto-typeR/
├── client/
│   ├── agent.py           # Monitoring agent for lab PCs
│   └── requirements.txt
├── server/
│   ├── app.py             # Flask server (API + Dashboard)
│   ├── database.py        # SQLAlchemy models
│   ├── engine.py          # Decision logic
│   ├── dashboard/
│   │   └── index.html     # Admin dashboard UI
│   └── requirements.txt
├── camera/
│   ├── presence.py        # OpenCV presence detection
│   └── requirements.txt
├── ai/
│   └── model.py           # LSTM model skeleton
└── README.md
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install flask sqlalchemy requests pynput psutil opencv-python numpy
```

Or use individual requirements files:
```bash
pip install -r server/requirements.txt
pip install -r client/requirements.txt
pip install -r camera/requirements.txt
```

### 2. Start the Server

```bash
cd server
python app.py
```
> Server runs at `http://localhost:5000`

### 3. Start Camera Module (Optional)

```bash
cd camera
python presence.py
```
> Opens webcam and sends presence data to server

### 4. Start Client Agent (On Each Lab PC)

```bash
cd client
python agent.py
```
> Monitors activity and receives commands from server

### 5. View Dashboard

Open browser: **http://localhost:5000**

---

## ⚙️ How It Works

### Decision Logic (engine.py)

```
IF
  (No Mouse/Keyboard activity for > 5 mins)
  AND (CPU Usage < 10%)
  AND (No presence detected by camera)
THEN
  → Send SLEEP command to client
```

### Data Flow

| Component | Sends | Receives |
|-----------|-------|----------|
| Client Agent | Heartbeat (CPU, idle time) | Action (SLEEP/NONE) |
| Camera Module | Presence status | - |
| Server | Action commands | Heartbeat + Presence |

---

## 📊 Dashboard Features

- **Real-time PC Status** (Active / Idle)
- **CPU Usage** per machine
- **Idle Duration** tracking
- **CCTV Presence Status**
- **Auto-refresh** every 5 seconds

---

## 🔮 AI Layer (Future Enhancement)

The `ai/model.py` contains a skeleton for:
- **LSTM-based time-series prediction**
- **Idle window forecasting**
- **Usage pattern analysis**

---

## 🛠️ Configuration

### Client Agent (`client/agent.py`)
```python
SERVER_URL = "http://localhost:5000/api/heartbeat"
CHECK_INTERVAL = 5  # seconds
```

### Decision Engine (`server/engine.py`)
```python
IDLE_TIME_THRESHOLD = 300  # 5 minutes
CPU_IDLE_THRESHOLD = 10.0  # percent
```

### Camera Module (`camera/presence.py`)
```python
CAMERA_SOURCE = 0  # 0 for webcam, or RTSP URL
CHECK_INTERVAL_SECONDS = 5
```

---

## 📌 Use Cases

- **College/University Labs**: Auto-shutdown idle PCs after hours
- **Corporate Offices**: Energy optimization for workstations
- **Internet Cafes**: Billing integration with usage detection
- **Server Rooms**: Resource monitoring and alerts

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

---

## 📄 License

This project is for educational purposes.

---

## 👨‍💻 Author

**Jamsith Rilwan**

---

> 💡 *"Idle systems waste energy. Let AI handle it."*
