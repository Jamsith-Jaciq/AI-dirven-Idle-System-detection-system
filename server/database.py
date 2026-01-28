from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ClientHeartbeat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pc_id = db.Column(db.String(50), nullable=False)
    cpu_usage = db.Column(db.Float, nullable=False)
    idle_duration = db.Column(db.Integer, nullable=False) # Seconds
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class PresenceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.String(50), nullable=False)
    presence_detected = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
