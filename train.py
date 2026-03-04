import cv2
import os
import numpy as np

faces, labels = [], []
label_id = 0
name_map = {}

for name in os.listdir("dataset"):
    if os.path.isdir(f"dataset/{name}"):
        name_map[label_id] = name
        for file in os.listdir(f"dataset/{name}"):
            img = cv2.imread(f"dataset/{name}/{file}", 0)
            if img is not None:
                faces.append(img)
                labels.append(label_id)
        label_id += 1

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))
recognizer.save("trainer/trainer.yml")
np.save("trainer/names.npy", name_map)

print("✅ Model trained successfully!")
print("Ready to run: python3 classguard_main.py")
