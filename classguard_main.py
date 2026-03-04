import cv2
from picamera2 import Picamera2
import numpy as np
import time
from datetime import datetime
import os

# ====================== SETUP ======================
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
picam2.configure(config)
picam2.start()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/trainer.yml")
name_map = np.load("trainer/names.npy", allow_pickle=True).item()

# CSV setup
os.makedirs("logs", exist_ok=True)
csv_file = "logs/attendance.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w") as f:
        f.write("timestamp,student_name,attendance,concentration_score,status\n")

present_students = {}
consecutive_low = {}   # for sleeping detection
last_log_time = time.time()

print("🎥 ClassGuard LIVE - Headless Mode")
print("Stand in front of the camera. Press Ctrl+C to stop.\n")

# ====================== MAIN LOOP ======================
try:
    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        total_people = len(faces)
        recognized_now = []
        current_attention = []

        for (x, y, w, h) in faces:
            face_roi = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            label, confidence = recognizer.predict(face_roi)
            name = name_map.get(label, "Unknown") if confidence < 110 else "Unknown"

            if name != "Unknown":
                recognized_now.append(name)
                
                # Initialize sleeping detection counter
                if name not in consecutive_low:
                    consecutive_low[name] = 0
                
                # Eye detection for concentration
                eye_roi = gray[y:y+int(h//2), x:x+w]
                eyes = eye_cascade.detectMultiScale(eye_roi, 1.1, 4)
                score = 0.95 if len(eyes) >= 2 else 0.55 if len(eyes) == 1 else 0.15
                current_attention.append(score)

                # Track consecutive low scores for sleeping detection
                if score < 0.3:
                    consecutive_low[name] += 1
                else:
                    consecutive_low[name] = 0

                status = "Sleeping 😴" if consecutive_low[name] >= 5 else "Attentive 👀"
                print(f"  → {name} | Confidence: {confidence:.1f} | Score: {score:.2f} | {status}")

        # Log every 8 seconds
        if time.time() - last_log_time > 8:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            avg_score = np.mean(current_attention) if current_attention else 0.0

            for name in recognized_now:
                status = "Sleeping 😴" if consecutive_low.get(name, 0) >= 5 else "Attentive 👀"
                present_students[name] = (avg_score, status)

            # Write to CSV
            for name, (score, status) in present_students.items():
                with open(csv_file, "a") as f:
                    f.write(f"{timestamp},{name},Present,{score:.2f},{status}\n")

            # Console Dashboard
            print("\n" + "="*75)
            print(f"📍 {timestamp}")
            print(f"👥 Total People in Classroom: {total_people}")
            print(f"✅ Recognized Students      : {recognized_now or ['None']}")
            print("   Status:")
            for name, (score, status) in present_students.items():
                print(f"      • {name} → {status} ({score:.1%} attention)")
            print(f"📊 Class Average Attention : {avg_score:.1%}")
            print("="*75)

            last_log_time = time.time()

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n\n✅ ClassGuard stopped.")
finally:
    picam2.stop()
    print(f"📁 Logs saved: ~/ClassGuard/logs/attendance.csv")
    print("Ready for SES World Engineering Day 2026!")
