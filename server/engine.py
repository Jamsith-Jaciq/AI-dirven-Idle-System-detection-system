from datetime import datetime, timedelta
from database import ClientHeartbeat, PresenceLog

# CONFIG
IDLE_TIME_THRESHOLD = 300 # Seconds (5 minutes)
CPU_IDLE_THRESHOLD = 10.0 # Percent

def evaluate_client_status(pc_id, latest_heartbeat):
    """
    Decides if a client should SLEEP based on:
    1. Client reported idle duration (Mouse/Keyboard)
    2. Client CPU usage
    3. Camera Presence (Global or Zone-based)
    """
    
    # 1. Check Input Inactivity
    if latest_heartbeat.idle_duration < IDLE_TIME_THRESHOLD:
        return "NONE" # Active usage
        
    # 2. Check CPU Usage
    if latest_heartbeat.cpu_usage > CPU_IDLE_THRESHOLD:
        return "NONE" # Background task running
        
    # 3. Check Camera Presence (Simplistic: If ANY camera saw someone in last 1 min, don't sleep)
    # In a real scenario, we map PC_ID to Zone_ID. Here we check global presence for demo.
    last_presence = PresenceLog.query.order_by(PresenceLog.timestamp.desc()).first()
    
    if last_presence:
        time_diff = datetime.utcnow() - last_presence.timestamp
        if time_diff.total_seconds() < 60 and last_presence.presence_detected:
            return "NONE" # Someone is nearby
            
    # If all conditions met:
    return "SLEEP"
