import cv2
import requests
import time
import datetime

# CONFIG
SERVER_URL = "http://localhost:5000/api/presence"
CAMERA_SOURCE = 0 # 0 for Webcam, or RTSP URL like "rtsp://user:pass@ip:port/1"
CHECK_INTERVAL_SECONDS = 5

def detect_presence():
    # Load Face Detector (Haar Cascada)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    cap = cv2.VideoCapture(CAMERA_SOURCE)
    
    if not cap.isOpened():
        print("Cannot open camera")
        return

    print(f"Monitoring Camera Source: {CAMERA_SOURCE}...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        has_presence = len(faces) > 0
        
        # Draw for local debug (optional)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
        # Display (optional - can comment out for headless)
        cv2.imshow('CCTV Monitor', frame)
        
        # Send to Server
        try:
            payload = {"zone": "LAB-1", "presence": 1 if has_presence else 0}
            requests.post(SERVER_URL, json=payload, timeout=1)
            print(f"[{datetime.datetime.now()}] Presence: {has_presence}")
        except Exception as e:
            print(f"Server Error: {e}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        time.sleep(CHECK_INTERVAL_SECONDS)  # Don't overload the server

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_presence()
