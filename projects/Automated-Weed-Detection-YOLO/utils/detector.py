"""
Automated Weed Detection System Using YOLO - inference wrapper.

Loads the fine-tuned YOLOv8 model (trained by model/train_model.py on
the real crop/weed dataset) and runs detection on an uploaded image,
returning an annotated image plus a structured list of detections.
"""

import base64
import os

import cv2
from ultralytics import YOLO

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "weed_yolo_best.pt")
CONF_THRESHOLD = 0.20
IMG_SIZE = 640

_model = None


def _load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "Trained model not found. Run 'python data/prepare_dataset.py' then "
                "'python model/train_model.py' first."
            )
        _model = YOLO(MODEL_PATH)
    return _model


def detect(image_bytes):
    """Runs weed/crop detection on raw image bytes.

    Returns a dict: {detections: [...], counts: {...}, annotated_image_b64: str}
    """
    model = _load_model()

    import numpy as np

    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not decode image. Please upload a valid JPEG/PNG file.")

    results = model.predict(source=image, conf=CONF_THRESHOLD, imgsz=IMG_SIZE, iou=0.50, max_det=300, augment=False, verbose=False)
    result = results[0]

    detections = []
    counts = {"crop": 0, "weed": 0}
    for box in result.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        confidence = round(float(box.conf[0]), 3)
        x1, y1, x2, y2 = [round(v, 1) for v in box.xyxy[0].tolist()]
        detections.append({"class": label, "confidence": confidence, "box": [x1, y1, x2, y2]})
        counts[label] = counts.get(label, 0) + 1

    annotated_bgr = result.plot()
    success, buffer = cv2.imencode(".png", annotated_bgr)
    if not success:
        raise RuntimeError("Failed to encode annotated image.")
    annotated_b64 = base64.b64encode(buffer).decode("ascii")

    return {
        "detections": detections,
        "counts": counts,
        "total_detections": len(detections),
        "annotated_image_b64": annotated_b64,
    }
