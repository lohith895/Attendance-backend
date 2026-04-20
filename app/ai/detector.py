from ultralytics import YOLO
import cv2

model = YOLO("yolov8n-face.pt")

def detect_faces(image):
    results = model(image)[0]
    faces = []

    for box in results.boxes.xyxy:
        x1, y1, x2, y2 = map(int, box)
        faces.append((image[y1:y2, x1:x2], {
            "x": x1, "y": y1,
            "width": x2 - x1,
            "height": y2 - y1
        }))
    return faces
