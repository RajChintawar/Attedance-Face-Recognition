import cv2
import numpy as np
import os
from deepface import DeepFace
from datetime import datetime
import pandas as pd

# Path
path = r"C:\Users\rajch\OneDrive\Desktop\ADIT\images"
images = []
classNames = []
myList = os.listdir(path)
print("[INFO] Found images:", myList)

# Load images and names
for cl in myList:
    img_path = os.path.join(path, cl)
    img = cv2.imread(img_path)

    if img is None:
        print(f"[ERROR] Could not read {cl}")
        continue

    images.append(img)
    classNames.append(os.path.splitext(cl)[0])

print("[INFO] Class Names:", classNames)

# Attendance marking
def markAttendance(name):
    attendance_file = r"C:\Users\rajch\OneDrive\Desktop\ADIT\raj.csv"
    if not os.path.exists(attendance_file):
        with open(attendance_file, 'w') as f:
            f.write("Name,Time\n")

    with open(attendance_file, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%Y-%m-%d %H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
            print(f"[MARKED] {name} at {dtString}")

# Start Webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[ERROR] Cannot open webcam")
    exit()

print("[INFO] Starting webcam...")

# DeepFace requires images to compare with
# We prepare a database dictionary
db = {}
for name, img in zip(classNames, images):
    db[name] = img

while True:
    success, frame = cap.read()
    if not success:
        print("[ERROR] Failed to grab frame")
        break

    # Resize for speed
    frame_small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    try:
        # Find faces in the current frame
        results = DeepFace.find(
            img_path=frame_small,
            db_path=path,
            model_name="Facenet",
            detector_backend="opencv",
            enforce_detection=False,
            distance_metric="cosine",
            silent=True
        )

        if results and isinstance(results, list) and len(results) > 0:
            for result in results[0].itertuples():
                identity = os.path.basename(result.identity)
                name = os.path.splitext(identity)[0].upper()

                # Display on frame
                cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)
                markAttendance(name)

    except Exception as e:
        print(f"[WARNING] DeepFace could not find face: {e}")

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
