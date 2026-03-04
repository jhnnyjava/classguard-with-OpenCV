import cv2
from picamera2 import Picamera2
import os
import time

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
picam2.configure(config)
picam2.start()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

print("=== ClassGuard Enrollment (Headless) ===")
print("Look straight at the camera.\n")

raw_name = input("Enter student name (e.g. John_Khaemba): ").strip()
name = raw_name.replace(" ", "_")

os.makedirs(f"dataset/{name}", exist_ok=True)
count = 0

print(f"📸 Enrolling {name}...")

while count < 30:
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))
        cv2.imwrite(f"dataset/{name}/{count:02d}.jpg", face)
        count += 1
        print(f"   Captured {count}/30")

    time.sleep(0.15)

picam2.stop()
print(f"\n✅ Enrollment completed for {name}!")
print("Run again for next student, or: python3 train.py")
