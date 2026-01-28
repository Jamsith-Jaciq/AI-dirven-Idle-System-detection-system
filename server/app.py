from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os
from database import db, ClientHeartbeat, PresenceLog
from engine import evaluate_client_status

app = Flask(__name__, template_folder='dashboard')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab_monitor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    # Fetch latest status for each PC
    # This is a bit inefficient for rigorous SQL but fine for prototype
    unique_pcs = db.session.query(ClientHeartbeat.pc_id).distinct().all()
    devices = []
    
    for (pc_id,) in unique_pcs:
        latest = ClientHeartbeat.query.filter_by(pc_id=pc_id).order_by(ClientHeartbeat.timestamp.desc()).first()
        if latest:
            status = "ACTIVE"
            if latest.idle_duration > 60: # Simple visual threshold
                status = "IDLE"
            
            devices.append({
                "id": pc_id,
                "status": status,
                "cpu": latest.cpu_usage,
                "idle": latest.idle_duration,
                "last_seen": latest.timestamp
            })
            
    # Get latest presence
    last_presence = PresenceLog.query.order_by(PresenceLog.timestamp.desc()).first()
    presence_status = "Unknown"
    if last_presence:
        presence_status = "Detected" if last_presence.presence_detected else "Empty"
        
    return render_template('index.html', devices=devices, presence=presence_status)

@app.route('/api/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json
    new_beat = ClientHeartbeat(
        pc_id=data['pc_id'],
        cpu_usage=data['cpu_usage'],
        idle_duration=data['idle_duration'],
        timestamp=datetime.fromisoformat(data['timestamp'])
    )
    db.session.add(new_beat)
    db.session.commit()
    
    # Decision Engine
    action = evaluate_client_status(data['pc_id'], new_beat)
    
    return jsonify({"status": "received", "action": action})

@app.route('/api/presence', methods=['POST'])
def presence():
    data = request.json
    new_log = PresenceLog(
        zone_id=data.get('zone', 'DEFAULT_ZONE'),
        presence_detected=bool(data.get('presence')),
        timestamp=datetime.now()
    )
    db.session.add(new_log)
    db.session.commit()
    return jsonify({"status": "updated"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
