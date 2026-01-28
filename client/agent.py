import time
import json
import socket
import threading
import psutil
import requests
import os
import platform
from pynput import mouse, keyboard
from datetime import datetime

# --- CONFIGURATION ---
SERVER_URL = "http://localhost:5000/api/heartbeat"
PC_ID = socket.gethostname()
CHECK_INTERVAL = 5  # Seconds
IDLE_THRESHOLD_SECONDS = 300 # Local check (optional, server decides mostly)

# --- STATE ---
class SystemState:
    def __init__(self):
        self.last_activity_time = time.time()
        self.lock = threading.Lock()

    def update_activity(self):
        with self.lock:
            self.last_activity_time = time.time()

    def get_idle_duration(self):
        with self.lock:
            return time.time() - self.last_activity_time

state = SystemState()

# --- INPUT LISTENERS ---
def on_move(x, y):
    state.update_activity()

def on_click(x, y, button, pressed):
    state.update_activity()

def on_scroll(x, y, dx, dy):
    state.update_activity()

def on_press(key):
    state.update_activity()

def start_listeners():
    # Mouse Listener
    mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
    )
    mouse_listener.start()

    # Keyboard Listener
    keyboard_listener = keyboard.Listener(
        on_press=on_press
    )
    keyboard_listener.start()

# --- SYSTEM MONITORING ---
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def perform_action(action):
    if action == "SLEEP":
        print("Received SLEEP command. Executing...")
        if platform.system() == "Windows":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif platform.system() == "Linux":
            os.system("systemctl suspend")
    elif action == "SHUTDOWN":
        print("Received SHUTDOWN command. Executing...")
        if platform.system() == "Windows":
            os.system("shutdown /s /t 1")
        elif platform.system() == "Linux":
            os.system("shutdown now")
    elif action == "LOCK":
        if platform.system() == "Windows":
            os.system("rundll32.exe user32.dll,LockWorkStation")

# --- MAIN LOOP ---
def main():
    print(f"Starting Agent on {PC_ID}...")
    start_listeners()

    while True:
        try:
            cpu_usage = get_cpu_usage()
            idle_duration = state.get_idle_duration()
            
            payload = {
                "pc_id": PC_ID,
                "cpu_usage": cpu_usage,
                "idle_duration": int(idle_duration),
                "timestamp": datetime.now().isoformat()
            }

            print(f"Sending Heartbeat: {payload}")
            
            try:
                response = requests.post(SERVER_URL, json=payload, timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    action = data.get("action", "NONE")
                    if action != "NONE":
                        print(f"Server ordered action: {action}")
                        perform_action(action)
            except requests.exceptions.ConnectionError:
                print("Server not reachable.")
            
        except Exception as e:
            print(f"Error in main loop: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
