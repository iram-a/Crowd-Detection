import os
from ultralytics import YOLO
import cv2

# Folder paths
input_folder = 'crowd_images'
output_folder = 'annotated_images'
os.makedirs(output_folder, exist_ok=True)

# Load YOLOv8 tiny model (auto downloads if not present)
model = YOLO('yolov8n.pt')

# Define crowding thresholds
def crowd_level(count):
    if count >= 0 and count <= 6:
        return "Green"       # Safe
    elif count >= 7 and count <= 16:
        return "Yellow"      # Moderate
    elif count >= 17:
        return "Red"         # Overcrowded
    else:
        return "Unclassified"

# Process each image in input folder
for img_name in os.listdir(input_folder):
    img_path = os.path.join(input_folder, img_name)
    results = model(img_path)  # Run detection
    count = 0
    for r in results:
        for cls in r.boxes.cls:
            if int(cls) == 0:  # Class 0 is person in COCO dataset
                count += 1
    level = crowd_level(count)
    img_annotated = results[0].plot()
    cv2.putText(img_annotated, f"Count: {count} ({level})", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    out_path = os.path.join(output_folder, f"annotated_{img_name}")
    cv2.imwrite(out_path, img_annotated)
    print(f"{img_name}: Person count = {count}, Level = {level}")

